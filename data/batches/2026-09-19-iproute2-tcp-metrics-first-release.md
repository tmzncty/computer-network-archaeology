# Batch: iproute2 `ip tcp_metrics` first tagged release — 2026-09-19

This batch advances one explicitly open TCP archaeology item: **recover the exact first iproute2 release carrying `tcp_metrics`**.

The result is deliberately bounded to the upstream commit and tagged-release/source-snapshot boundary. It does not claim first development-snapshot availability, distribution packaging, or production deployment.

## Why this slice was selected

The master root-hunting worklist already records the kernel-side history — pre-2012 route-metrics storage, the 2012 dedicated TCP metrics cache, timestamp migration, Generic Netlink exposure, userspace administration semantics, and the 2019 ssthresh policy change — but still names the **exact first iproute2 release carrying `tcp_metrics`** as missing.

The existing narrative also already identifies the kernel Generic Netlink interface. Therefore this run avoids repeating kernel-cache archaeology and asks only: **when did the corresponding iproute2 command enter upstream, and what is the first tagged release that contains it?**

## Primary evidence

### E1 — kernel Generic Netlink interface predates the iproute2 merge

- Linux commit: `d23ff701643a4a725e2c7a8ba2d567d39daa29ea`
- Subject: `tcp: add generic netlink support for tcp_metrics`
- Author date: **2012-09-04**
- Committer date: **2012-09-05**
- Canonical location: <https://github.com/torvalds/linux/commit/d23ff701643a4a725e2c7a8ba2d567d39daa29ea>
- Exact implementation evidence: introduces `TCP_METRICS_GENL_NAME`, Generic Netlink operations, and get/delete/dump/flush support.

**Certainty:** high.

**Does not prove:** that iproute2 support was released at the same time, that the userspace implementation was causally derived only after this commit, or that any operator used the interface immediately.

### E2 — exact upstream iproute2 introduction commit

- iproute2 commit: `ea63a69b6d2f230af5471ddfa7b05b369fc49816`
- Subject: `iproute2: add support for tcp_metrics`
- Author: **Julian Anastasov**
- Author date: **2012-10-03 12:07:39 UTC**
- Committer: **Stephen Hemminger**
- Committer date: **2012-10-08 17:23:07 UTC**
- Canonical location: <https://github.com/iproute2/iproute2/commit/ea63a69b6d2f230af5471ddfa7b05b369fc49816>

The commit adds `ip/tcp_metrics.c`, adds the copied UAPI header `include/linux/tcp_metrics.h`, builds the new object, and registers both `tcpmetrics` and `tcp_metrics` as `ip` objects. The command implements `show`, `flush`, and `delete` through Generic Netlink.

The source header says `Julian Anastasov <ja@ssi.bg>, August 2012`. Treat that as source-drafting/provenance evidence only; the preserved upstream author/committer timestamps are October 2012.

**Certainty:** high.

**Does not prove:** first private draft, first public patch posting, first executable distributed to users, or first production use.

### E3 — immediately preceding tag v3.6.0 predates the introduction commit

- Annotated tag: `v3.6.0`
- Tagger: **Stephen Hemminger**
- Tag date: **2012-10-01 15:39:41 UTC**
- Tag object SHA: `8a1b549d97b3dab53f2ece94d5fb9c220bdc5aa3`
- Tagged commit: `808ed6e10a4af30807b0ac1db4c91a2e5d0403ec`
- Canonical tag reference: <https://github.com/iproute2/iproute2/tree/v3.6.0>

The v3.6.0 tag is seven days earlier than the upstream tcp_metrics commit's committer timestamp. An exact GitHub contents lookup for `ip/tcp_metrics.c?ref=v3.6.0` returns `404 Not Found`.

A contemporary v3.6.0 announcement dated **2012-10-01** describes that release's new bridge-forwarding-table support and explicitly asks contributors to submit changes for features entering the 3.7 merge window.

**Certainty:** high that v3.6.0 does not contain the command.

**Does not prove:** that nobody had a private or untagged tcp_metrics userspace implementation by this date.

### E4 — v3.7.0 contains the command and its release announcement names it

- Annotated tag: `v3.7.0`
- Tagger: **Stephen Hemminger**
- Tag date: **2012-12-11 17:52:55 UTC**
- Tag object SHA: `6b3359f3ea1ad435af437687b7b9cdf93b2ae6d7`
- Tagged commit: `6abef21b3e74c27766737214a96fc20d5e3c0b0c`
- Source snapshot: <https://github.com/iproute2/iproute2/blob/v3.7.0/ip/tcp_metrics.c>
- Contemporary release announcement: <https://lkml.rescloud.iu.edu/hypermail/linux/kernel/1212.1/01361.html>

The tagged source contains `ip/tcp_metrics.c`. Hemminger's **2012-12-11** `[ANNOUNCE] iproute2 3.7.0` says the release includes `tcp_metrics` support and lists `Julian Anastasov (1): iproute2: add support for tcp_metrics` in the release changes. The announcement also publishes the `iproute2-3.7.0.tar.gz` package location.

**Certainty:** high.

**Does not prove:** first distribution-package adoption, first operator deployment, or that every v3.7.0 downstream build enabled/used the command.

## Recovered chronology

```text
2012-09-04  Linux d23ff701... authored:
            Generic Netlink tcp_metrics interface

2012-10-01  iproute2 v3.6.0 tagged
            no ip/tcp_metrics.c

2012-10-03  iproute2 ea63a69... author timestamp
2012-10-08  iproute2 ea63a69... committed upstream
            adds ip tcp_metrics/tcpmetrics

2012-12-11  iproute2 v3.7.0 tagged and announced
            release announcement explicitly says it includes tcp_metrics
```

## Safe conclusion

**iproute2 v3.7.0 is the first tagged upstream iproute2 release/source snapshot carrying `ip tcp_metrics`.**

The proof is not merely chronological: the previous v3.6.0 tag predates the introduction commit and lacks the source file, while v3.7.0 contains the source file and its contemporary release announcement explicitly names the feature.

## Lineage decision

**No `LIN-*` edge is created.**

There is a clear protocol/interface relationship between the kernel Generic Netlink family and the iproute2 client, but the question closed here is release membership, not a lineage relation. Merely observing that the kernel commit predates the userspace commit does not justify `derived-from`, `successor-of`, or another causal ancestry edge.

If the repository later adds a relation vocabulary for “administers/uses UAPI exposed by”, that can be modeled separately from code lineage.

## Explicit non-proofs

This batch does **not** prove:

1. that v3.7.0 was the first moment the source was publicly visible in upstream git;
2. the date of the first mailing-list posting of Anastasov's userspace patch;
3. first Linux distribution packaging of `ip tcp_metrics`;
4. first production/operator use;
5. first operational need for the command;
6. that the kernel Generic Netlink commit caused the userspace design merely because it came first in preserved commit chronology;
7. that the August 2012 source-header date is a release date;
8. that closing this userspace release boundary closes the older route-cache implementation ancestry gap.

## Repository integration

Updated in this batch:

- `docs/tcp/tcp-metrics-cache-ip-tcp-metrics.md` — adds the exact upstream commit and v3.6.0 → v3.7.0 release boundary, plus negative claims.
- `data/batches/2026-09-19-iproute2-tcp-metrics-first-release.md` — preserves the research package and evidence limits.

Recommended reconciliation after merge:

- update `docs/methodology/root-hunting-master-worklist.md` so the TCP-metrics item retains only the **earliest route-cache implementation ancestry** gap;
- if structured-source IDs are allocated, record the introduction commit, v3.6.0 boundary, v3.7.0 boundary, and contemporary release announcement without minting a lineage edge.

## Remaining parent-task gap

The older half remains open: trace **TCP destination metrics before the 2012 dedicated cache split** far enough back to identify the earliest route-cache implementation ancestry and version boundaries. That is a separate archaeology question and should not be inferred from the 2012 userspace release evidence.

Research and drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
