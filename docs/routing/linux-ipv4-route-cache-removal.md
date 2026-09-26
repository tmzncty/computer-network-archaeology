# Linux IPv4 route-cache removal: from global hash to FIB-attached reuse

## Scope

Linux 3.6 is often summarized as the release that removed the IPv4 route cache. That shorthand is only accurate for the older global cache organized around `rt_hash_table`. It should not be read as “Linux stopped reusing route results.”

The July 2012 redesign removed the global, traffic-populated route hash and redistributed its useful responsibilities:

```text
Linux 3.5
global IPv4 rt_hash_table route cache
        |
        | July 2012 redesign
        v
Linux 3.6
FIB / fib_info nexthops
    ├── cached input rtable
    ├── per-CPU cached output rtable
    └── destination-specific FIB nexthop exceptions
          ├── PMTU
          └── redirect gateway
```

## 1. The old global cache is explicitly removed

Mainline commit:

```text
89aef8921bfbac22f00e04f8450f6e447db13e42
ipv4: Delete routing cache.
```

was committed on **2012-07-20**.

The commit explains that the old IPv4 cache had unpredictable performance because its state depended heavily on observed traffic patterns rather than only on routing-table contents. The patch removes central cache machinery from `net/ipv4/route.c`, including `rt_hash_table`, hash-chain traversal, cache insertion, expiry and garbage-collection paths.

The narrow defensible claim is therefore:

> **The 2012 work deliberately removes the old global IPv4 route hash cache.**

It does not establish that all later route lookups are uncached.

## 2. The contemporary cover letter describes the replacement plan

David S. Miller's **[PATCH 00/15] Kill the routing cache**, dated **2012-07-18**, describes the series sequence directly:

1. remove the routing cache and initially build a new `rtable` per lookup;
2. simplify `rtable`;
3. make preconstructed routes legal to cache in FIB nexthops;
4. account for nexthop exceptions and adjust `rt_gateway` semantics;
5. cache precomputed input and output routes in FIB nexthops.

Primary source:

- <https://www.spinics.net/lists/netdev/msg205115.html>

This matters because the final FIB-attached caches are part of the documented redesign rather than an unrelated later feature.

## 3. Destination-specific state moves into FIB nexthop exceptions

Commit:

```text
4895c771c7f006b4b90f9d6b1d2210939ba57b38
ipv4: Add FIB nexthop exceptions.
```

was committed on **2012-07-17**.

Its message says that subnetted route entries still need persistent storage for destination-specific learned values such as Path MTU and redirects. It introduces `struct fib_nh_exception`, attached to a FIB nexthop, with destination, PMTU, redirect-gateway and lifetime state.

The architectural split becomes:

```text
ordinary reusable route
    → FIB-nexthop route cache

destination-specific deviation
    → FIB nexthop exception
```

This does not make nexthop exceptions the old `rt_hash_table` under a new name.

## 4. Representation changes make prefixed route reuse safe

Commit:

```text
f8126f1d5136be1ca1a3536d43ad7a710b5620f8
ipv4: Adjust semantics of rt->rt_gateway.
```

was committed on **2012-07-20**.

It explicitly says the change is needed “in order to allow prefixed routes.” The new interpretation is:

- `rt_gateway == 0`: destination is on-link;
- `rt_gateway != 0`: route uses that gateway.

This helps a reusable route object describe a family of destinations rather than implicitly one host.

## 5. Input and output routes are cached at FIB nexthops

Output-side commit:

```text
f2bb4bedf35d5167a073dcdddf16543f351ef3ae
ipv4: Cache output routes in fib_info nexthops.
```

committed **2012-07-20**, says an output route without a nexthop exception can be cached in its FIB-info nexthop. Exception lookup happens before deciding whether generic reuse is valid.

Input-side commit:

```text
d2d68ba9fe8b38eb03124b3176a013bb8aa2b5e5
ipv4: Cache input routes in fib_info nexthops.
```

committed **2012-07-20**, defines a separate input reuse policy and excludes cases such as DIRECTSRC and nonzero `itag`.

Input and output caching are therefore related but not identical mechanisms.

## 6. Output caching becomes per-CPU before 3.6 final

Eric Dumazet's commit:

```text
d26b3a7c4b3b26319f18bb645de93eba8f4bdcd5
ipv4: percpu nh_rth_output cache
```

was committed **2012-07-31**.

The patch moves output-route reuse to per-CPU storage to reduce shared-reference contention. Its stated 24-process UDP test improved from 5.24 seconds to 2.06 seconds on the author's 24-CPU machine; Linux 3.5 was reported at 6.60 seconds. These are patch-specific measurements, not universal performance claims.

A 2012-07-26 follow-up, **ipv4: Fix input route performance regression**, likewise says that route-cache removal had lost a no-reference input fast path and restores it when a lookup hits a route cached in a FIB nexthop:

- <https://lists.openwall.net/netdev/2012/07/26/62>

## 7. Adjacent release trees show a sharp v3.5 → v3.6 boundary

At tag **v3.5**, `net/ipv4/route.c` still contains:

- `rt_hash_table`;
- central hash-chain lookup and insertion;
- expiry / garbage-collection machinery;
- a full cache-flush path.

The v3.5 `include/net/ip_fib.h` does not contain the later `fib_nh_exception`, `nh_rth_input` or `nh_pcpu_rth_output` fields.

At tag **v3.6**, `include/net/ip_fib.h` contains:

```c
struct fib_nh_exception { ... };
struct rtable __rcu * __percpu *nh_pcpu_rth_output;
struct rtable __rcu *nh_rth_input;
struct fnhe_hash_bucket *nh_exceptions;
```

The v3.6 route code performs FIB lookups, checks destination exceptions, reuses `nh_rth_input` where legal, and uses the per-CPU output route cache otherwise.

Linus Torvalds announced **Linux 3.6 final on 2012-09-30**:

- <https://lwn.net/Articles/518196/>

The safe release claim is:

> **Linux 3.6 is the first adjacent released snapshot in this excavation where the old global IPv4 `rt_hash_table` cache is gone and the replacement FIB-nexthop route reuse plus exception architecture is present.**

This is a source/release boundary, not a first-deployment claim.

## Lineage assessment

The evidence supports a high-certainty composite architectural transition:

```text
global IPv4 rt_hash_table route cache
    -- explicit removal / responsibility redistribution -->
FIB-attached reusable rtable caches
    + FIB nexthop exceptions
```

A single structured `replaced-by` edge would currently be too coarse because it could imply that the FIB itself was introduced in 2012 or that the exception table is a one-for-one code descendant of the old cache. Preserve the relation in narrative form unless the graph gains a safer composite relation.

## Explicit negative claims

This evidence does **not** establish that:

- Linux 3.6 eliminated all IPv4 route caching;
- every IPv4 lookup after 3.6 performs a full uncached FIB traversal;
- FIB nexthop exceptions are simply renamed old route-cache entries;
- the FIB trie originated in Linux 3.6;
- route-cache removal caused the contemporaneous TCP-metrics split, or vice versa;
- the patch benchmarks generalize to every workload;
- v3.6 inclusion proves the first production deployment;
- the 2012 design is identical to current Linux routing internals.

## Remaining work

This closes the 2012 removal/replacement transition, but not the entire “modern lookup architecture” history. Follow-up work should trace later movement of cached routes and exception storage through `fib_nh_common`, standalone nexthop objects, and subsequent lifetime/lookup changes. Linux FIB trie/hash generations remain a separate worklist item.

Research update: **GPT-5.6 Sol (OpenAI), September 2026**.
