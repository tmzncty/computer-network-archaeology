# Ledger synchronization queue

This compact live queue tracks the structured-record frontier. Older inventories live in `data/batches/` and the archived queue.

## Current structured frontier

### Artifacts

Recent ranges include:

- `ART-0175..0213` — registries, Unix/Linux implementation layers, resolver/routing suites, NSS/net-tools and GNU Zebra→Quagga→FRRouting;
- `ART-0214..0224` — ifconfig/rtnetlink, proc/socket diagnostics, ss/TCP observability, Linux neighbour/ND and RPDB/ip rule;
- `ART-0225..0233` — legacy ioctl control, transitional Netlink/rtnetlink, iproute/rtmon/ip monitor, network namespaces and VRF/l3mdev;
- `ART-0234..0238` — Tahoe/Reno/NewReno/SACK and RFC 6675 loss-recovery branches;
- `ART-0239..0241` — Linux BIC→CUBIC implementation and CUBIC RFC standardization lineage;
- `ART-0242..0243` — mainline BBR and Google BBRv3 development branch;
- `ART-0244..0246` — TCP_INFO base observability plus pacing- and delivery-rate extensions;
- `ART-0247..0248` — dedicated Linux TCP metrics cache and `ip tcp_metrics` administration;
- `ART-0249` — initial Linux veth pair driver mainline implementation and stable-release boundary;
- `ART-0250` — iproute2 named/processless `ip netns` command family and first tagged-release boundary.

**Next unreserved artifact ID: `ART-0251`**, subject to merge-time verification.

### Sources

- `SRC-0166..0247` — prior registry/Unix/Linux/routing/operations/Netlink/iproute/netns/VRF evidence;
- `SRC-0248..0251` — Tahoe/Reno/NewReno/SACK recovery RFC evidence;
- `SRC-0252..0257` — Linux BIC/CUBIC source and commits plus RFC 8312/9438;
- `SRC-0258..0260` — mainline BBR merge/current source and Google BBRv3 branch source;
- `SRC-0261..0263` — early TCP_INFO snapshot and pacing/delivery-rate field additions;
- `SRC-0264..0268` — dedicated tcp_metrics cache, timestamp consolidation, Generic Netlink/userspace administration and ssthresh-cache policy;
- `SRC-0269..0270` — initial veth mainline commit and Linux v2.6.24 released source snapshot;
- `SRC-0271..0273` — PID-selected netns administration, named/processless `ip netns` introduction, and v2.6.39→v3.0.0 tagged-release boundary.

**Next unreserved source ID: `SRC-0274`**, subject to verification.

### Lineages

- `LIN-0125..0187` — prior registry, Unix/Linux implementation, routing-suite, operations, neighbour/RPDB/ZAPI and Netlink/iproute/netns/VRF lineages;
- `LIN-0188..0191` — Tahoe→Reno→NewReno plus SACK-based recovery and explicit NewReno/SACK coexistence;
- `LIN-0192..0194` — BIC→CUBIC implementation succession and CUBIC implementation-vs-RFC standards clock;
- `LIN-0195` — mainline BBR → Google BBRv3 development-branch relationship with explicit mainline negative claim;
- `LIN-0196..0197` — TCP_INFO append-style pacing and delivery-rate observability evolution;
- `LIN-0198..0200` — route-metrics→dedicated tcp_metrics split, `ip tcp_metrics` operational exposure, and TCP_INFO/tcp_metrics state-plane distinction.

**Next unreserved lineage ID: `LIN-0201`**, subject to verification.

## Persistent task authority

Use `docs/methodology/root-hunting-master-worklist.md`. New work must be added there when discovered; chat reminders are not the task database.

## Latest batch manifests

- `data/batches/2026-08-29-linux-operations-roots.md`
- `data/batches/2026-08-29-netlink-iproute-netns-vrf.md`
- `data/batches/2026-08-29-tcp-recovery-congestion-observability.md`
- `data/batches/2026-09-01-veth-upstream-provenance.md`
- `data/batches/2026-09-05-iproute2-ip-netns-first-tagged-release.md`

## Current narrative frontier

Latest additions:

- `docs/tcp/tcp-tahoe-reno-newreno-sack-recovery.md`
- `docs/tcp/linux-bic-cubic-implementation-genealogy.md`
- `docs/tcp/cubic-paper-linux-rfc-standardization.md`
- `docs/tcp/bbr-generations-pacing-observability.md`
- `docs/tcp/linux-tcp-info-field-genealogy.md`
- `docs/tcp/tcp-metrics-cache-ip-tcp-metrics.md`
- `docs/routing/linux-veth-upstream-provenance.md`
- `docs/routing/iproute2-ip-netns-first-tagged-release.md`

## Flat-ledger merge checklist

Before changing the three flat CSV ledgers:

1. fetch complete latest CSV blobs;
2. verify actual highest IDs and concurrent additions;
3. validate queued JSON records against schemas;
4. preserve reserved gaps;
5. append/promote without altering existing rows;
6. validate CSV quoting and column counts;
7. verify every structured ID is discoverable from flat ledgers;
8. synchronize human-readable indexes;
9. archive completed queue state before clearing it.

This queue is archival hygiene, not a second master database.
