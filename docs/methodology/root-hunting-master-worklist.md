# Root-Hunting Master Worklist

This file is the persistent execution list for the repository's **寻根活动 / root-hunting** work. It exists so research does not depend on a chat reminder.

Status vocabulary:

- `[x]` completed to narrative + evidence-bearing structured-record level;
- `[~]` started/substantial, but an explicitly named primary-source/provenance gap remains;
- `[ ]` queued.

## 2026-08-29 Linux operations pass — completed

- [x] `ifconfig` / network-device ioctls → rtnetlink → `ip addr` / `ip link`.
- [x] `/proc/net/tcp` and `/proc/net/tcp6` → `tcp_diag` / `inet_diag` / `sock_diag`.
- [x] `ss -ti` as an operational window into RTO, RTT, MSS, cwnd, ssthresh, PMTU and congestion-control state.
- [x] ARP + IPv6 Neighbor Discovery/NUD → Linux neighbour object → `ip neigh`, with explicit negative lineage: ND is not “ARPv6”.
- [x] classic destination-only routing → Linux RPDB / multiple FIB tables → `ip rule`.
- [x] GNU Zebra/Quagga/FRR ZAPI versions 0–6, field-level revision matrix.

## Kernel/user-space interface archaeology

- [x] BSD PF_ROUTE versus Linux rtnetlink as parallel kernel-routing control families.
- [x] net-tools role migration into iproute2.
- [x] BPF → libpcap → tcpdump.
- [x] `/etc/services`, `/etc/protocols`, netdb, inetd.
- [x] `/etc/hosts`, resolver, NSS, `getaddrinfo`.
- [x] exact major Linux network-device ioctl families used by historical `ifconfig`-style administration, plus the 2.1.68 compatibility bridge translating legacy route ioctls into rtnetlink/FIB operations.
- [x] earliest currently recovered Linux Netlink/rtnetlink design provenance: 2.1.15 character-device + `nlmsghdr` transitional source, 2.1.68 socket/object-model patch, and participant retrospective in RFC 3549.
- [~] first iproute/iproute2 releases and command-syntax diffs. **Confirmed:** Kuznetsov authorship/development lower bound in the 1996 era, Linux 2.2 stable-generation association, object grammar, and surviving INR mirror snapshots from 1999 onward. **Still missing:** proof of the exact first public tarball and exact project-name transition to `iproute2`.
- [x] `ip monitor` / `rtmon` / asynchronous rtnetlink notification lineage, including early `RTMGRP_*` multicast groups and binary event-log replay.
- [x] network namespaces and VRF: CLONE_NEWNET broad stack isolation versus VRF/l3mdev L3 domains; pre-4.8 per-VRF iif/oif rules → Linux 4.8 generic l3mdev FIB rule; explicit composition with RPDB/multiple tables.
- [ ] recover pre-2.1.15 SKIPLINK/Netlink source and exact first AF_NETLINK socket-family merge commit.
- [ ] recover the exact first public iproute/iproute2 source distribution and earliest command-reference document.
- [ ] `ip monitor` event-loss/resync semantics and routing-daemon snapshot+watch patterns from primary implementation sources.
- [~] network namespace merge series, veth merge provenance, and `ip netns` first-release archaeology. **Completed:** exact initial veth mainline commit `e314dbdc1c0dc6a548ecf0afce28ecfd538ff568` and Linux 2.6.24 release boundary; the September 2007 00/16 core network-namespace series plus 17/16 safety follow-up; contemporary partial/core-merge status; exact mainline anchors `5f256becd868bf63b70da8f2769033d6734670e9` (basic infrastructure), `ce286d327341295f58d89864d746a524287cfdf9` (device movement), and separate `9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1` (CLONE_NEWNET clone/unshare). **Still missing:** first iproute2 release containing `ip netns`, optional pre-mainline veth patch-series provenance, and later protocol-family completion only where needed for operational claims.
- [ ] VRF device initial merge commit, netdev discussion, l3mdev rule commit and first real deployments.

## TCP implementation/observability archaeology

- [x] RFC 793 → RFC 9293 base-standard continuity.
- [x] Nagle versus Jacobson congestion work kept as different branches.
- [x] Window Scale/Timestamps and SACK option branches.
- [x] `/proc/net/tcp` → diag interfaces → `ss`.
- [x] `ss -i/-t -i` observable metrics map.
- [~] Tahoe / Reno / NewReno / SACK recovery version-by-version. **Completed:** RFC-level recovery genealogy and explicit NewReno-vs-SACK parallel-branch model. **Still missing:** period 4.3BSD Tahoe/Reno source distributions and function-level source diff.
- [x] BIC → CUBIC Linux implementation genealogy, including Linux v2.6.13 BIC source, the CUBIC 2.0 replacement/rework commit, the 2006 default switch, and later CUBIC 2.3/HyStart evolution.
- [x] CUBIC RFC standardization versus Linux code history: implementation/deployment clock is explicitly separated from RFC 8312 Experimental and RFC 9438 Standards Track document history.
- [~] BBR generations and pacing observability. **Completed:** 2016 mainline BBR merge/model, current mainline source, Google BBRv3 branch identity, pacing/delivery-rate observability linkage and explicit negative claim that current mainline is not simply “BBRv3”. **Still missing:** exact BBRv2→v3 branch/commit chronology and deployment timeline.
- [~] `tcp_info` struct field/version genealogy by Linux release. **Completed:** Linux 2.4-era provenance bound, v2.6.12 early struct snapshot, 2014 pacing fields, 2016 delivery-rate/app-limited fields. **Still missing:** exact pre-git introduction patch and exhaustive every-field release matrix.
- [~] TCP metrics cache and `ip tcp_metrics` history. **Completed:** pre-2012 route-metrics role → 2012 dedicated cache, timestamp migration, Generic Netlink exposure, userspace administration semantics and 2019 ssthresh-cache policy change. **Still missing:** earliest route-cache implementation ancestry and exact first iproute2 release carrying `tcp_metrics`.
- [ ] packet captures paired with `ss -ti` output and RFC-variable concordance.
- [ ] recover Tahoe and Reno BSD source snapshots and build a loss-recovery code diff.
- [ ] trace NewReno implementation adoption in BSD/Linux before and after the RFC lineage.
- [ ] map Linux SACK scoreboard/recovery generations through RFC 3517, RFC 6675, PRR and RACK.
- [ ] reconstruct BBRv1→v2→v3 branch history from commit/patch-series evidence and preserve mainline-versus-Google-branch state per date.
- [ ] machine-generate a complete `struct tcp_info` field-addition table from kernel history, including field, units, commit, release and `ss` rendering.
- [ ] trace TCP destination metrics before the 2012 dedicated cache split and recover the first `ip tcp_metrics` userspace release.

## Neighbour/address-resolution archaeology

- [x] ARP and Proxy ARP.
- [x] IPv6 ND/NUD distinction from ARP.
- [x] Linux unified neighbour object and `ip neigh`.
- [ ] NUD state transitions mapped to Linux neighbour timer/code paths.
- [ ] IPv4 ARP cache state handling versus IPv6 NUD state handling in shared neighbour core.
- [ ] gratuitous ARP / unsolicited NA operational branches.
- [ ] proxy neighbour / proxy ARP / ND proxy comparison.
- [ ] MAC randomization and locally-administered-address interaction with neighbour caches.

## Routing-policy/FIB archaeology

- [x] `route(8)`, `routed`, RIP and PF_ROUTE history.
- [x] GateD multiprotocol routing role.
- [x] GNU Zebra → Quagga → FRRouting real fork chain.
- [x] Linux rtnetlink/iproute2 route control.
- [x] Linux RPDB / `ip rule` / multiple tables.
- [ ] Linux FIB trie/hash implementation generations.
- [ ] policy-routing introduction commits and early HOWTO/deployment evidence.
- [ ] source routing, fwmark routing, VRF/l3mdev and namespaces as RPDB branches.
- [ ] `ip route get` lookup behavior genealogy.
- [ ] route cache removal and modern lookup architecture.

## Zebra / routing-suite internals

- [x] GateD role versus Zebra architecture kept separate from code ancestry.
- [x] GNU Zebra → Quagga fork.
- [x] Quagga → FRRouting fork.
- [x] ZAPI v0→v6 header/command revision matrix.
- [ ] earliest GNU Zebra/Zserv source snapshot and message layouts.
- [ ] exact Quagga 0.98/0.99 transition commits for ZAPI v0→v1.
- [ ] v1→v2 command/layout diff.
- [ ] v2→v3 VRF-ID introduction diff.
- [ ] v3→v4 marker 255→254 fork boundary.
- [ ] v4→v5 16→32-bit VRF ID diff.
- [ ] v5→v6 route-command consolidation diff.
- [ ] current FRR ZAPI beyond v6 and dataplane API separation.

## Number/registry archaeology

- [x] EtherType registry.
- [x] IP Protocol/Next Header registry.
- [x] service/port registry.
- [x] Assigned Numbers RFC snapshots → online IANA.
- [x] ASN 16→32-bit and private/documentation ranges.
- [x] IEEE OUI/MA-L/MA-M/MA-S.
- [x] IPv4 special-purpose/private/documentation/shared address spaces.
- [ ] `/etc/services` snapshot diffs against Assigned Numbers RFCs.
- [ ] `/etc/protocols` snapshot diffs.
- [ ] surviving historical values still compiled into kernels/dissectors.

## Packet-capture concordance

- [ ] create reproducible present-day capture fixtures for IPv4/TCP/UDP/ICMP/ARP/DNS/SMTP.
- [ ] annotate each byte/field with earliest recognizable standard ancestor.
- [ ] run period-appropriate tcpdump where surviving source builds permit it.
- [ ] compare modern dissector output with historical protocol diagrams.

## Rule

When a new excavation is proposed, add it here immediately. A chat message is not the task database. The repository is.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), August 2026**.
