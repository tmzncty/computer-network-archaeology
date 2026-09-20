# TCP metrics cache genealogy: from route-cache memory to a dedicated destination cache and `ip tcp_metrics`

## Why TCP remembers old connections

TCP does not always begin each connection with zero knowledge about a destination.

Linux has historically cached selected measurements from completed connections so later connections to the same destination can reuse path experience such as:

```text
RTT
RTTVAR
cwnd-related information
ssthresh
reordering knowledge
timestamp state
later Fast Open-related state
```

This cache has changed architecture substantially over time.

## 1. Older Linux stores dynamic TCP metrics in routing state

Historical `tcp(7)` documentation describes a behavior controlled by `tcp_no_metrics_save`: by default Linux saves metrics from closing TCP connections in the route cache so future connections can use them for initial conditions.

That design reflects an older architecture where destination routing state and transport-learned destination state were closely coupled.

Conceptually:

```text
route/destination cache entry
      ├── forwarding/path information
      └── TCP learned metrics
```

The advantage is obvious: destination-specific state already has a home.

The downside becomes clearer as routing/cache architecture changes.

## 2. 2012: TCP metrics become their own local cache

Commit:

```text
51c5d0c4b169bf762f09e0d5b283a7f0b2a45739
```

has the decisive message:

```text
tcp: Maintain dynamic metrics in local cache.
```

and says explicitly:

> Computed TCP metrics are no longer maintained in the route metrics.

The new design uses a local hash table of TCP metric blobs.

This is a clean architecture split:

```text
route metrics + TCP dynamic metrics
        ↓ responsibility separation
routing state        TCP metrics hash/cache
```

This is not merely a file rename. It decouples transport memory from route-metric storage.

## 3. Timestamp state follows into the new cache

The next transition moves timestamp-related remembered state from `inetpeer` into the TCP metrics cache.

That further consolidates destination-specific TCP memory under the new subsystem.

So the 2012 generation is a **merge of TCP memory responsibilities** at the same time that it is a **split from routing metrics**.

Those two lineage relations should both be recorded.

## 4. Generic Netlink makes the cache administratively visible

Commit:

```text
d23ff701643a4a725e2c7a8ba2d567d39daa29ea
```

was authored on **2012-09-04** and adds Generic Netlink support for `tcp_metrics`, including:

```text
get one entry
delete one entry
dump entries
flush entries
```

This allows userspace tools to manage a kernel cache that previously existed mainly as hidden transport state.

The operational path becomes:

```text
TCP connection experience
      ↓
kernel tcp_metrics cache
      ↓ Generic Netlink
ip tcp_metrics
      ↓
show / flush / delete / manipulate selected metrics
```

## 5. The first tagged iproute2 release carrying `ip tcp_metrics` is v3.7.0

The userspace side can now be bounded more precisely than “2012-era iproute2”.

Upstream iproute2 commit:

```text
ea63a69b6d2f230af5471ddfa7b05b369fc49816
iproute2: add support for tcp_metrics
```

was authored by **Julian Anastasov** on **2012-10-03** and committed by **Stephen Hemminger** on **2012-10-08**. It adds `ip/tcp_metrics.c`, wires `tcp_metrics` and `tcpmetrics` into `ip`, and implements `show`, `flush`, and `delete` over the kernel Generic Netlink family.

The immediately preceding iproute2 tag **v3.6.0** was tagged on **2012-10-01**, before that userspace commit existed in the upstream history. An exact contents lookup for `ip/tcp_metrics.c` at `v3.6.0` returns no file.

The next tag **v3.7.0** was tagged on **2012-12-11** and contains `ip/tcp_metrics.c`. Stephen Hemminger's contemporary v3.7.0 release announcement is unusually explicit: it says the release “includes support for tcp_metrics” and lists Anastasov's `iproute2: add support for tcp_metrics` change in the release changelog.

Therefore the defensible release boundary is:

```text
iproute2 v3.6.0 (2012-10-01)
        tcp_metrics command absent
            ↓
ea63a69... merged upstream (2012-10-08)
            ↓
iproute2 v3.7.0 (2012-12-11)
        first tagged release carrying ip tcp_metrics
```

This closes the **first tagged-release/source-snapshot** question. It does not establish the first public availability of a development snapshot between tags, the first Linux distribution package carrying the command, or the first production use.

The source header in `tcp_metrics.c` says “August 2012”. That is useful drafting/provenance evidence, but it must not be substituted for the upstream commit date or the release date.

## 6. `ip tcp_metrics` exposes destination memory

The iproute2 command displays cached metrics keyed by destination.

Depending on kernel/tool generation, values can include:

```text
age
cwnd
ssthresh
rtt
rttvar
reordering
source address
timestamp values
Fast Open state
```

This differs from `ss -ti`:

```text
ss -ti
  → current live socket/control-block state

ip tcp_metrics
  → remembered destination state across connections
```

A historian should not merge those two observability surfaces.

## 7. Cached experience can become stale or harmful

Caching is a bet that the next connection sees something like the previous path.

Modern networks weaken that assumption:

- NAT can map many users behind one visible address;
- load balancing can change backend/path;
- wireless/mobile paths change rapidly;
- congestion conditions vary;
- short loss-based flows can leave misleading ssthresh values.

This becomes explicit in 2019.

## 8. 2019: ssthresh caching is disabled by default

Commit:

```text
65e6d90168f3593df0ae598502bcbf20d78ff0fb
```

introduces:

```text
net.ipv4.tcp_no_ssthresh_metrics_save
```

with default behavior disabling ssthresh caching while retaining other TCP metrics such as RTT and cwnd.

The commit message explains that dynamic networks, NAT sharing and short flows can make cached ssthresh harmful and prematurely terminate slow start on later flows.

This creates a subtle survival pattern:

```text
TCP destination metrics cache survives
        ↓
one historically cached field becomes opt-in/disabled by default
```

The cache is not simply removed.

## 9. Architecture and policy change independently

Two very different historical changes occur:

### storage architecture

```text
route metrics
   ↓ 2012 split
TCP-specific local metrics cache
```

### caching policy

```text
save broad learned state
   ↓ operational experience
stop saving ssthresh by default
```

Do not conflate them.

A subsystem can survive while individual fields change policy.

## 10. Relation to route-cache history

The 2012 split happens in the broader era when Linux routing lookup architecture is moving away from older per-destination route-cache assumptions.

This makes TCP metrics an especially useful artifact: transport state that once piggybacked on route state receives its own lifecycle, hash table and user-facing control path.

A future excavation should connect this directly to the route-cache removal/FIB lookup history rather than asserting causal details without the relevant commits.

## 11. Root-hunting graph

```text
TCP learns RTT/cwnd/ssthresh/path state
          ↓
old destination/route metrics storage
          ↓ 2012
TCP-specific local metrics cache
          ├── timestamp memory consolidated here
          ↓
Generic Netlink tcp_metrics interface
          ↓
iproute2 commit ea63a69... (2012-10-08)
          ↓ release membership, not causal lineage
iproute2 v3.7.0 (2012-12-11)
          ↓
ip tcp_metrics

policy branch:
cached ssthresh
    ↓ 2019 operational reassessment
not saved by default
```

## 12. Negative claims

Do not state:

- `ip tcp_metrics` shows live socket state;
- TCP metrics are the routing table;
- the 2012 change removed all destination memory;
- the 2019 ssthresh change disabled the entire metrics cache;
- cached RTT is necessarily the current path RTT;
- the August 2012 source-header date is the iproute2 release date;
- the v3.7.0 release boundary proves the first development snapshot, distribution package, operator deployment, or production use;
- because the kernel Generic Netlink interface predates the userspace merge/release, that chronology alone proves a causal or implementation-lineage edge.

It is remembered, destination-keyed historical state.

## Primary anchors

- historical/current `tcp(7)` descriptions of `tcp_no_metrics_save`.
- Linux commit `51c5d0c4b169bf762f09e0d5b283a7f0b2a45739` — dynamic metrics move to local cache.
- Linux commit `81166dd6fa8eb780b2132d32fbc77eb6ac04e44e` — timestamps move from inetpeer into metrics cache.
- Linux commit [`d23ff701643a4a725e2c7a8ba2d567d39daa29ea`](https://github.com/torvalds/linux/commit/d23ff701643a4a725e2c7a8ba2d567d39daa29ea) — Generic Netlink interface, authored 2012-09-04.
- iproute2 commit [`ea63a69b6d2f230af5471ddfa7b05b369fc49816`](https://github.com/iproute2/iproute2/commit/ea63a69b6d2f230af5471ddfa7b05b369fc49816) — initial `ip tcp_metrics` userspace support; author date 2012-10-03, commit date 2012-10-08.
- iproute2 annotated tags [`v3.6.0`](https://github.com/iproute2/iproute2/releases/tag/v3.6.0) (2012-10-01) and [`v3.7.0`](https://github.com/iproute2/iproute2/releases/tag/v3.7.0) (2012-12-11), plus the v3.7.0 `ip/tcp_metrics.c` source snapshot.
- Stephen Hemminger, `[ANNOUNCE] iproute2 3.7.0`, 2012-12-11 — contemporary release statement that v3.7.0 includes `tcp_metrics` support and lists Anastasov's change.
- `ip-tcp_metrics(8)`.
- Linux commit `65e6d90168f3593df0ae598502bcbf20d78ff0fb` — disable ssthresh metrics saving by default.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), August–September 2026**.
