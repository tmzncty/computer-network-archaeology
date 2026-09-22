# Batch: Linux TCP dynamic route-metrics origin — 2026-09-22

This batch closes the oldest still-open half of the TCP-metrics archaeology: **when does surviving Linux source first show a completed TCP connection writing learned destination metrics into routing/destination state so that later connections can reuse them?**

The answer is bounded narrowly to an exact source transition: **Linux 2.3.14 → 2.3.15 (August 1999)**. It does not claim that Linux 2.3.15 invented route metrics in general, the IPv4 route cache in general, or every metric later exposed through `ip tcp_metrics`.

## Why this slice was selected

The repository already covers:

- route/destination storage before the 2012 split;
- the 2012 dedicated TCP metrics cache;
- timestamp-state migration;
- the Generic Netlink `tcp_metrics` interface;
- the first tagged iproute2 release carrying `ip tcp_metrics` (v3.7.0);
- the 2019 default-policy change for cached ssthresh.

After the merged first-release work, the remaining explicit worklist gap was the **earliest route-cache implementation ancestry**. No open PR currently overlaps this slice.

## Primary evidence

### E1 — Linux 2.3.15 adds the TCP writeback path itself

Primary source:

- Linux 2.3.15 HTML patch, `linux/net/ipv4/tcp_input.c`
- <https://ftp.riken.jp/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_net_ipv4_tcp_input.c.html>
- Header identifies the original file as `v2.3.14/linux/net/ipv4/tcp_input.c`.

The 2.3.15 diff **adds** `tcp_update_metrics(struct sock *sk)` with the comment:

> Save metrics learned by this TCP session.

The function obtains the socket destination with `__sk_dst_get(sk)` and, subject to metric locks and validity checks, writes connection-learned values into destination state:

- `dst->rtt` from `tp->srtt`;
- `dst->rttvar` from the connection deviation estimate;
- `dst->ssthresh` from congestion-control history;
- `dst->cwnd` from congestion-window history.

The same patch calls `tcp_update_metrics(sk)` when a successful connection reaches the relevant closing paths, including the `TCP_LAST_ACK` → `TCP_CLOSE` path shown near the end of the patch.

**Certainty:** high for the 2.3.14 → 2.3.15 introduction boundary of this recovered writeback path, because the source is presented as an addition in the version-to-version diff.

**Does not prove:** that Linux 2.3.15 invented route metrics, that no private/pre-mainline version existed before 2.3.15, or that every field written here was later reused identically.

### E2 — Linux 2.3.15 also adds the corresponding per-destination read/reuse path

The same `tcp_input.c` patch adds `tcp_init_metrics(struct sock *sk)`.

Its own comment explains the design intent: the RTT from SYN/SYN-ACK can look unrealistically small, so the code should **“Use per-dst memory to make it more realistic.”**

The function reads destination state back into the new TCP control block:

- a larger stored `dst->rtt` can raise `tp->srtt`;
- stored `dst->rttvar` can raise `tp->mdev`;
- a locked `RTAX_CWND` can set `snd_cwnd_clamp`;
- stored `dst->ssthresh` initializes `snd_ssthresh`, bounded by the clamp.

The same patch invokes `tcp_init_metrics(sk)` when the SYN/ACK processing path establishes the connection.

This makes the historical behavior stronger than “the route object happened to contain TCP-looking fields.” The 2.3.15 source contains both halves of cross-connection memory:

```text
finished TCP connection
        ↓ tcp_update_metrics()
destination / route-cache state
        ↓ tcp_init_metrics()
later TCP connection initial state
```

**Certainty:** high.

**Does not prove:** that every saved value affected every subsequent connection, or that the cache key and route-cache lifetime were stable across all later kernels.

### E3 — the same version expands destination and RTAX metric vocabulary

The Linux 2.3.15 patch set also changes the destination/route metric structures and routing API vocabulary in the same release generation.

Relevant primary patch locations:

- `include/net/dst.h` in the 2.3.15 patch set:
  <https://www.nic.funet.fi/pub/unix/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_include_net_dst.h.html>
- `include/linux/rtnetlink.h` in the 2.3.15 patch set:
  <https://ftp.riken.jp/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_include_linux_rtnetlink.h.html>

The destination structure gains richer metric fields including `rttvar`, `ssthresh`, `cwnd`, and `advmss`. The route-metric enumeration correspondingly gains `RTAX_RTTVAR`, `RTAX_SSTHRESH`, `RTAX_CWND`, and `RTAX_ADVMSS`.

This is supporting context for E1/E2. The decisive evidence for TCP-learned cross-connection memory remains the explicit read/write code in `tcp_input.c`.

**Certainty:** high for same-version structural/API expansion.

**Does not prove:** that every RTAX item was dynamically learned by TCP, or that these metric names first existed as concepts in networking at this point.

### E4 — v2.3.14 already had route RTT configuration; therefore 2.3.15 is not the origin of all route metrics

Primary source:

- Linux 2.3.15 HTML patch, `linux/net/ipv4/route.c`
- <https://ftp.riken.jp/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_net_ipv4_route.c.html>

The diff is explicitly against `v2.3.14/linux/net/ipv4/route.c`. In removed v2.3.14 lines, route construction already copied FIB-derived values such as:

```text
rt->u.dst.window = fi->fib_window ? : 0;
rt->u.dst.rtt    = fi->fib_rtt ? : TCP_TIMEOUT_INIT;
```

Linux 2.3.15 replaces the individual assignments with a broader metric-array copy and additional defaults.

This gives an important negative boundary:

- **before 2.3.15**, routing/destination state already had an RTT metric that could be seeded from route configuration/defaults;
- **in 2.3.15**, the recovered TCP code begins writing measurements learned by completed connections back into destination state and reusing that per-destination memory.

Therefore the claim is **not** “RTAX_RTT or route metrics were invented in 2.3.15.” The defensible claim is that **the surviving 2.3.14→2.3.15 diff directly introduces the recovered dynamic TCP destination-metrics feedback path**.

**Certainty:** high.

### E5 — Linux 2.3.15 was publicly released on 25 August 1999

Primary distribution artifact:

- kernel.org v2.3 directory index: <https://www.kernel.org/pub/linux/kernel/v2.3/>
- `linux-2.3.14.tar.*`: **19-Aug-1999 00:17**
- `linux-2.3.15.tar.*`: **25-Aug-1999 23:16**
- `patch-2.3.15.*`: **25-Aug-1999 23:16**

Contemporary announcement mirror:

- Linus Torvalds, `Linux-2.3.15..`, dated **Wed, 25 Aug 1999 16:36:10 -0700**
- <https://www.linuxtoday.com/developer/linux-development-kernel-2-3-15-released/>

The announcement says the patch set takes the development series to 2.3.15. The source-file timestamps inside generated patch pages are not substituted for the release publication date.

**Certainty:** high for the public release date and adjacent release boundary.

**Does not prove:** first operator installation, first distribution packaging, or first production traffic using the mechanism.

### E6 — the 2012 split explicitly identifies the old storage as route metrics

Primary source:

- Linux commit `51c5d0c4b169bf762f09e0d5b283a7f0b2a45739`
- subject: `tcp: Maintain dynamic metrics in local cache.`
- author date: **2012-07-10**
- <https://github.com/torvalds/linux/commit/51c5d0c4b169bf762f09e0d5b283a7f0b2a45739>

Its commit message states that computed TCP metrics are **no longer maintained in the route metrics** and introduces a local hash table of TCP dynamic-metrics blobs.

This is strong primary evidence that the 2012 cache is a storage-architecture extraction/continuation from the older route-metric mechanism rather than an unrelated feature merely appearing later.

**Certainty:** high for the storage migration.

**Does not prove:** that the 1999 code remained unchanged through 2012, that the 2012 split was caused by route-cache removal, or that the dedicated cache caused the later route-cache-removal work.

## Recovered chronology

```text
Linux 2.3.14 — 1999-08-19
    route/dst state already has configured/default RTT-style metrics
    no tcp_update_metrics()/tcp_init_metrics() pair in the recovered diff baseline
            ↓
Linux 2.3.15 — 1999-08-25
    adds tcp_update_metrics(): completed TCP sessions write RTT/RTTVAR/
    ssthresh/cwnd information into destination state
    adds tcp_init_metrics(): later TCP sessions consume per-dst memory
    expands destination/RTAX metric vocabulary
            ↓
... later route-cache / destination-metric evolution ...
            ↓
Linux 2012 commit 51c5d0c...
    “Computed TCP metrics are no longer maintained in the route metrics”
    dedicated local tcp_metrics hash/cache
            ↓
2012 Generic Netlink administration
            ↓
iproute2 v3.7.0
    first tagged release carrying ip tcp_metrics
```

## Facts to add to the repository

1. The exact recovered source boundary for Linux dynamic TCP destination-memory is **v2.3.14 → v2.3.15**.
2. Linux 2.3.15 introduces both `tcp_update_metrics()` and `tcp_init_metrics()` in the preserved diff, making the save/reuse loop explicit.
3. The source itself calls the reuse mechanism **per-dst memory**.
4. v2.3.14 already had route/FIB-seeded RTT state, so the 2.3.15 claim must be limited to **dynamic TCP-learned writeback/reuse**, not route metrics in general.
5. Linux 2.3.15 was publicly released on **1999-08-25** according to kernel.org artifacts and the contemporary release announcement.
6. The 2012 dedicated cache commit explicitly says computed TCP metrics cease being maintained in route metrics, giving a direct storage-migration bridge from the older design.

## Lineage assessment

A defensible relation now exists at the architectural level:

```text
route/destination-resident dynamic TCP metrics
    -- storage extraction / responsibility migration -->
dedicated tcp_metrics local cache (2012)
```

**Certainty: high**, because the 2012 commit explicitly says the metrics are “no longer maintained in the route metrics.”

However, do **not** mint a generic `derived-from` or `successor` edge merely because those labels are available. If the repository's structured lineage vocabulary cannot represent a storage/responsibility extraction without strengthening the claim, preserve this relation in narrative/batch form instead.

The 2.3.14 → 2.3.15 change itself is a source-version introduction boundary, not a claim that v2.3.14 “caused” v2.3.15.

## Explicit negative claims

This evidence does **not** establish that:

- Linux 2.3.15 invented route metrics, `dst_entry`, the IPv4 route cache, or RTT configuration;
- every route metric added in 2.3.15 was a TCP-learned metric;
- every value written by `tcp_update_metrics()` affected future connections in exactly the same way;
- `RTAX_CWND` dynamic writeback necessarily meant an unlocked cached cwnd was directly used as an initial cwnd in this exact implementation;
- the 2.3.15 code was the first private prototype or first mailed patch;
- 25 August 1999 was the first production deployment date;
- the 1999 mechanism directly caused the 2012 cache split;
- the 2012 cache split directly caused, or was caused by, IPv4 route-cache removal;
- a later dedicated `tcp_metrics` cache is simply the old route cache under a new filename.

## Repository changes for this batch

- expand `docs/tcp/tcp-metrics-cache-ip-tcp-metrics.md` with the exact 2.3.14→2.3.15 source boundary, read/write mechanics, release date, and negative boundaries;
- update `docs/methodology/root-hunting-master-worklist.md` to close the now-resolved TCP-metrics origin and iproute2-release gaps;
- retain this batch as the evidence package and locator record.

## Remaining adjacent questions

These are deliberately outside this batch:

- exact authorship/review provenance of the pre-git 2.3.15 TCP-metrics patch beyond what can be safely inferred from file revision metadata;
- every intermediate change to the destination-metric implementation between 1999 and 2012;
- the independent history and causality of IPv4 route-cache removal;
- first named operational deployment of this mechanism.

Those questions may be useful future excavations, but they are not required to close the repository's currently named “earliest route-cache implementation ancestry” gap.
