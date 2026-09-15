# Research batch — Linux VRF / l3mdev mainline chronology

Date: 2026-09-15  
Scope: one open root-hunting slice only — initial Linux VRF merge, l3mdev generalization, l3mdev FIB rule, and product/deployment boundary.

## Why this slice was selected

The root-hunting worklist still called for the VRF initial merge commit, netdev discussion, l3mdev-rule commit, and deployment evidence. Existing narrative coverage described the architecture but did not pin the exact mainline commits or distinguish upstream tag presence from vendor product availability.

## New facts recovered

### F1 — first recovered public RFC in this lineage

- Date: 2015-02-04.
- Object: `[RFC PATCH 00/29] net: VRF support` by David Ahern.
- Evidence: <https://lwn.net/Articles/632522/>
- Finding: the proposal explicitly argues that network namespaces and VRFs are different operational abstractions and cites scaling concerns for large VRF counts.
- Certainty: high for the existence/content of this public RFC; **not** claimed as the first Linux VRF work ever.

### F2 — concrete VRF-device design before merge

- Date: 2015-07-27.
- Object: `[PATCH net-next 13/16] net: Introduce VRF device driver - v2`.
- Evidence: <https://www.mail-archive.com/netdev%40vger.kernel.org/msg71870.html>
- Finding: VRF-lite is implemented as master device + associated routing table + enslaved routed interfaces + ordinary FIB rules. The patch says the driver borrows heavily from IPvlan and teaming; the merged source later says it is based on dummy, team and ipvlan drivers.
- Certainty: high for implementation borrowing; insufficient for a whole-artifact successor/derived-from edge.

### F3 — initial mainline VRF commit

- Commit: `193125dbd8eb292d88feb201f030889b488b0a02`.
- Title: `net: Introduce VRF device driver`.
- Author date: 2015-08-13T20:59:10Z.
- Committer date: 2015-08-14T05:43:22Z.
- Evidence: <https://github.com/torvalds/linux/commit/193125dbd8eb292d88feb201f030889b488b0a02>
- Concrete changes: `CONFIG_NET_VRF`, `drivers/net/vrf.c`, table-bound VRF master model.
- Adjacent tag check: absent in v4.2, present in v4.3.
- Conclusion: Linux v4.3 is the first adjacent tagged release checked here containing the merged VRF driver.
- Certainty: high.

### F4 — explicit VRF → l3mdev generalization

- Public series: `[PATCH net-next 00/11] net: L3 master device`, dated 2015-09-24.
- Evidence: <https://lwn.net/Articles/658471/> and <https://lists.openwall.net/netdev/2015/09/25/3>.
- Mainline commit: `1b69c6d0ae90b7f1a4f61d5c8209d5cb7a55f849`, `net: Introduce L3 Master device abstraction`.
- Author date: 2015-09-30T03:07:11Z.
- Committer date: 2015-09-30T03:40:32Z.
- Evidence: <https://github.com/torvalds/linux/commit/1b69c6d0ae90b7f1a4f61d5c8209d5cb7a55f849>
- Adjacent tag check: `include/net/l3mdev.h` absent in v4.3, present in v4.4.
- Conclusion: the source itself calls the work a generalization of VRF into l3mdev; v4.4 is the first adjacent tagged source-tree presence checked here.
- Certainty: high.

### F5 — l3mdev FIB rule solves repeated-rule scaling

- Mainline commit: `96c63fa7393d0a346acfe5a91e0c7d4c7782641b`, `net: Add l3mdev rule`.
- Date: 2016-06-08.
- Evidence: <https://github.com/torvalds/linux/commit/96c63fa7393d0a346acfe5a91e0c7d4c7782641b>
- Finding: old VRF setup required one `iif` and one `oif` rule per address family per VRF; new `FRA_L3MDEV` lets lookup obtain table ID from the L3 master and reduces the base rules to one per address family.
- The commit explicitly says higher-priority per-VRF rules can coexist.
- Certainty: high.

### F6 — automatic rule installation follows immediately

- Mainline commit: `1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0`, `net: vrf: Add l3mdev rules on first device create`.
- Parent: `96c63fa7393d0a346acfe5a91e0c7d4c7782641b`.
- Date: 2016-06-08.
- Evidence: <https://github.com/torvalds/linux/commit/1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0>
- Finding: first VRF creation installs IPv4/IPv6 l3mdev rules at default preference 1000; user replacement remains possible.
- Certainty: high.

### F7 — Linux 4.8 is the tagged boundary for `FRA_L3MDEV`, not for VRF itself

- Linux v4.7 UAPI `include/uapi/linux/fib_rules.h`: no `FRA_L3MDEV`.
- Linux v4.8 same file: `FRA_L3MDEV` present.
- Finding: the l3mdev-rule interface lands in the v4.8 tagged tree.
- Negative boundary: VRF driver and l3mdev abstraction are older (v4.3 and v4.4 respectively).
- Certainty: high.

### F8 — vendor shipping lower bound, not first customer deployment

- Cumulus Linux 3.0 was publicly available in June 2016 with VRF advertised for multi-tenant Layer-3 Clos networks.
- Period sources:
  - <https://lwn.net/Articles/688697/>
  - <https://www.theregister.com/2016/06/01/cumulus_linux_30_nos_now_in_the_wild/>
  - <https://www.slideshare.net/CumulusNetworks/operationalizing-vrf-in-the-data-center>
- The June 2016 Cumulus presentation shows Cumulus Linux 3.0 with a 4.1-based kernel and VRF enabled while separately listing upstream VRF feature milestones beginning at 4.3. This is evidence of a vendor implementation/backport boundary, not source identity with upstream 4.1.
- Certainty: high for product availability; unknown for first customer production deployment.

## Candidate lineage relations

### Candidate A — VRF-specific plumbing → l3mdev abstraction

- Relation: explicit generalization.
- Evidence: 2015-09-24 series cover says the series "generalizes the VRF into L3 master device, l3mdev" and converts VRF to use the new operations.
- Certainty: high.
- Structured edge decision: **not minted in this batch**. Before creating `LIN-*`, confirm suitable endpoint artifacts and relation vocabulary so `generalizes` is not mistranslated into a stronger `derived-from` or `successor` claim.

### Candidate B — dummy/team/ipvlan patterns → VRF driver implementation

- Relation: source/design borrowing.
- Evidence: v2 patch and merged file header.
- Certainty: high for borrowing statement.
- Structured edge decision: **not minted** because this does not establish whole-artifact descent, replacement, or causal priority.

## Explicit non-proofs

This batch does not prove:

1. that the February 2015 RFC was the first Linux VRF implementation;
2. that the older out-of-tree patch mentioned there directly became the merged driver;
3. that network namespaces caused or evolved into VRF;
4. that dummy, team, or ipvlan is a product-level predecessor of VRF;
5. that l3mdev replaced RPDB/policy routing;
6. that Linux 4.8 introduced VRF itself;
7. that Cumulus Linux 3.0's Linux 4.1 base is identical to upstream 4.1 for VRF;
8. that product availability in June 2016 establishes the first production customer deployment.

## Files added / proposed

Added in this batch:

- `docs/routing/linux-vrf-l3mdev-mainline-chronology.md`
- `data/batches/2026-09-15-linux-vrf-l3mdev-mainline-chronology.md`

Recommended follow-up edits:

- cross-link this chronology from `docs/routing/network-namespaces-vrf-l3mdev-rpdb.md`;
- mark the root-hunting VRF task partial rather than complete because first named real-world deployment and older out-of-tree provenance remain unresolved;
- add source/artifact/lineage structured records only after checking current ID reservations and edge vocabulary at merge time.

## Remaining work

- identify the older out-of-tree VRF implementation cited by the 2015 RFC;
- recover a named production/customer deployment with period evidence;
- exact iproute2 merge/tag archaeology for the first `type vrf` user interface;
- evaluate whether repository lineage schema can express explicit `generalized-into` and `implementation-borrowing` without overclaiming.
