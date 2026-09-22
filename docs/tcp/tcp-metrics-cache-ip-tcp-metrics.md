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

## 1. Linux 2.3.15 makes dynamic TCP destination memory explicit

The surviving Linux **2.3.14 → 2.3.15** patch gives a much tighter origin boundary than the generic statement that old kernels stored TCP metrics in routing state.

In `linux/net/ipv4/tcp_input.c`, the 2.3.15 patch adds:

```text
tcp_update_metrics(struct sock *sk)
tcp_init_metrics(struct sock *sk)
```

The first function is introduced with the comment that it saves metrics learned by the TCP session when the connection finishes successfully. It obtains the socket's `dst_entry` and writes connection-learned values into destination state, subject to metric locks and validity checks:

```text
TCP srtt / mdev / congestion history
        ↓ tcp_update_metrics()
dst->rtt
dst->rttvar
dst->ssthresh
dst->cwnd
```

The same patch calls `tcp_update_metrics()` on successful closing paths.

The second function performs the other half of the memory loop. Its comment says that SYN/SYN-ACK RTT can look too small and instructs the implementation to **“Use per-dst memory to make it more realistic.”** It can raise the new connection's RTT estimate and deviation from stored destination values, apply a locked cwnd clamp, and initialize ssthresh from destination state. The patch calls `tcp_init_metrics()` during connection establishment.

So the recovered 2.3.15 behavior is not merely a structure containing TCP-looking field names:

```text
finished TCP connection
        ↓ save learned metrics
destination / route-cache state
        ↓ reuse per-dst memory
later TCP connection
```

The kernel.org archive dates Linux 2.3.14 to **1999-08-19** and Linux 2.3.15 to **1999-08-25**. Linus Torvalds' contemporary 2.3.15 announcement is also dated 25 August 1999.

### Important boundary: route RTT already existed before 2.3.15

Do not rewrite the result as “Linux invented route RTT metrics in 2.3.15.”

The `route.c` side of the same 2.3.14→2.3.15 diff shows that v2.3.14 route construction already seeded destination RTT from FIB configuration/default state:

```text
rt->u.dst.rtt = fi->fib_rtt ? : TCP_TIMEOUT_INIT;
```

The 2.3.15 generation expands the destination/RTAX metric vocabulary and, crucially, adds the TCP feedback path that writes measurements learned from completed connections and reuses the resulting per-destination memory.

The precise defensible claim is therefore:

> **Linux 2.3.15 is the exact recovered source boundary where the preserved v2.3.14→v2.3.15 diff introduces dynamic TCP-learned destination-metric writeback and per-destination reuse.**

This does not establish the first private prototype, first mailed patch, or first production deployment.

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

This creates a directly evidenced storage transition:

```text
route/destination-resident dynamic TCP metrics
        ↓ responsibility extraction in 2012
routing state        TCP metrics hash/cache
```

This is stronger than a chronological guess: the 2012 commit itself identifies route metrics as the previous storage location. It still does **not** prove that route-cache removal caused this change or that this change caused route-cache removal.

## 3. Timestamp state follows into the new cache

The next transition moves timestamp-related remembered state from `inetpeer` into the TCP metrics cache.

That further consolidates destination-specific TCP memory under the new subsystem.

So the 2012 generation is a **merge of TCP memory responsibilities** at the same time that it is a **split from routing metrics**.

Those two architectural relations should be described with their exact evidence rather than collapsed into a generic “successor” claim.

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

The userspace side can be bounded more precisely than “2012-era iproute2”.

Upstream iproute2 commit:

```text
ea63a69b6d2f230af5471ddfa7b05b369fc49816
iproute2: add support for tcp_metrics
```

was authored by **Julian Anastasov** on **2012-10-03** and committed by **Stephen Hemminger** on **2012-10-08**. It adds `ip/tcp_metrics.c`, wires `tcp_metrics` and `tcpmetrics` into `ip`, and implements `show`, `flush`, and `delete` over the kernel Generic Netlink family.

The immediately preceding iproute2 tag **v3.6.0** was tagged on **2012-10-01**, before that userspace commit existed in the upstream history. An exact contents lookup for `ip/tcp_metrics.c` at `v3.6.0` returns no file.

The next tag **v3.7.0** was tagged on **2012-12-11** and contains `ip/tcp_metrics.c`. Stephen Hemminger's contemporary v3.7.0 release announcement explicitly says the release includes `tcp_metrics` support and lists Anastasov's change.

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

The source header in `tcp_metrics.c` says “August 2012”. That is useful drafting/provenance evidence, but it must not be substituted for the upstream commit date or release date.

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
Linux 2.3.15 per-dst route/cache feedback
   ↓ later evolution
route metrics carrying dynamic TCP memory
   ↓ 2012 extraction
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

The older half of the TCP-metrics ancestry can now be pinned directly to the Linux 2.3.14→2.3.15 source transition rather than left as an undated “old route cache” box.

The 2012 split happens in the broader era when Linux routing lookup architecture is moving away from older per-destination route-cache assumptions. That makes TCP metrics an especially useful artifact: transport state that once piggybacked on route/destination state receives its own lifecycle and hash table.

But chronology is not causality. The evidence collected here does not establish that IPv4 route-cache removal caused the TCP-metrics split, or vice versa. Route-cache removal/FIB lookup history remains an independent excavation.

## 11. Root-hunting graph

```text
Linux 2.3.14
route/FIB state already includes configured/default RTT metric
          ↓ exact source diff, not causal claim
Linux 2.3.15 (1999-08-25)
tcp_update_metrics() + tcp_init_metrics()
TCP-learned per-dst route/cache memory
          ↓ later implementation evolution
route metrics retain computed TCP metrics
          ↓ explicit 2012 storage extraction
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

- Linux 2.3.15 invented route metrics, `dst_entry`, the IPv4 route cache, or RTT configuration;
- every metric added to the 2.3.15 route/destination vocabulary was dynamically learned by TCP;
- every value written by `tcp_update_metrics()` affected future connections identically;
- dynamic `RTAX_CWND` writeback by itself proves an unlocked cached cwnd was directly reused as the next connection's initial cwnd;
- the 2.3.15 source boundary proves the first private prototype, first mailed patch, distribution adoption, operator deployment, or production use;
- `ip tcp_metrics` shows live socket state;
- TCP metrics are the routing table;
- the 2012 change removed all destination memory;
- the 2012 cache split caused, or was caused by, route-cache removal merely because both belong to the same broad architectural era;
- the 2019 ssthresh change disabled the entire metrics cache;
- cached RTT is necessarily the current path RTT;
- the August 2012 source-header date is the iproute2 release date;
- the v3.7.0 release boundary proves the first development snapshot, distribution package, operator deployment, or production use;
- because the kernel Generic Netlink interface predates the userspace merge/release, that chronology alone proves a causal or implementation-lineage edge.

It is remembered, destination-keyed historical state whose storage architecture and field policy both changed over time.

## Primary anchors

- Linux 2.3.15 patch for `linux/net/ipv4/tcp_input.c` — v2.3.14→v2.3.15 addition of `tcp_update_metrics()` and `tcp_init_metrics()`, including the source comment describing “per-dst memory”: <https://ftp.riken.jp/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_net_ipv4_tcp_input.c.html>.
- Linux 2.3.15 patch for `linux/net/ipv4/route.c` — confirms the v2.3.14 baseline already seeded destination RTT from FIB configuration/defaults: <https://ftp.riken.jp/Linux/kernel/v2.3/patch-html/patch-2.3.15/linux_net_ipv4_route.c.html>.
- Linux 2.3.15 destination/RTAX structure patches: `include/net/dst.h` and `include/linux/rtnetlink.h` in the archived patch set.
- kernel.org v2.3 archive index — Linux 2.3.14 dated 1999-08-19 and Linux 2.3.15/patch-2.3.15 dated 1999-08-25: <https://www.kernel.org/pub/linux/kernel/v2.3/>.
- Linus Torvalds, `Linux-2.3.15..`, 1999-08-25 — contemporary release announcement mirror: <https://www.linuxtoday.com/developer/linux-development-kernel-2-3-15-released/>.
- historical/current `tcp(7)` descriptions of `tcp_no_metrics_save`.
- Linux commit [`51c5d0c4b169bf762f09e0d5b283a7f0b2a45739`](https://github.com/torvalds/linux/commit/51c5d0c4b169bf762f09e0d5b283a7f0b2a45739) — computed TCP metrics move out of route metrics into a dedicated local cache in 2012.
- Linux commit `81166dd6fa8eb780b2132d32fbc77eb6ac04e44e` — timestamps move from inetpeer into metrics cache.
- Linux commit [`d23ff701643a4a725e2c7a8ba2d567d39daa29ea`](https://github.com/torvalds/linux/commit/d23ff701643a4a725e2c7a8ba2d567d39daa29ea) — Generic Netlink interface, authored 2012-09-04.
- iproute2 commit [`ea63a69b6d2f230af5471ddfa7b05b369fc49816`](https://github.com/iproute2/iproute2/commit/ea63a69b6d2f230af5471ddfa7b05b369fc49816) — initial `ip tcp_metrics` userspace support; author date 2012-10-03, commit date 2012-10-08.
- iproute2 annotated tags [`v3.6.0`](https://github.com/iproute2/iproute2/releases/tag/v3.6.0) (2012-10-01) and [`v3.7.0`](https://github.com/iproute2/iproute2/releases/tag/v3.7.0) (2012-12-11), plus the v3.7.0 `ip/tcp_metrics.c` source snapshot.
- Stephen Hemminger, `[ANNOUNCE] iproute2 3.7.0`, 2012-12-11 — contemporary release statement that v3.7.0 includes `tcp_metrics` support and lists Anastasov's change.
- `ip-tcp_metrics(8)`.
- Linux commit `65e6d90168f3593df0ae598502bcbf20d78ff0fb` — disable ssthresh metrics saving by default.

Detailed evidence package: [`data/batches/2026-09-22-linux-tcp-route-metrics-origin.md`](../../data/batches/2026-09-22-linux-tcp-route-metrics-origin.md).

Research and initial drafting: **GPT-5.6 Sol (OpenAI), August–September 2026**.
