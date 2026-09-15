# Linux VRF → l3mdev: mainline chronology, rule scaling, and deployment boundary

## Scope

This note narrows one open item from the root-hunting worklist: the Linux VRF device's initial upstream history, the later l3mdev abstraction, and the Linux 4.8 FIB-rule simplification.

It does **not** treat VRF, network namespaces, and policy routing as successive versions of one feature. The broader architectural distinction remains in [`network-namespaces-vrf-l3mdev-rpdb.md`](network-namespaces-vrf-l3mdev-rpdb.md).

The evidence recovered here supports three different clocks:

1. public proposal/review;
2. mainline implementation and tagged-release presence;
3. vendor product availability.

Those clocks must not be collapsed into a single "VRF appeared in Linux" date.

## 1. Public proposal: 4 February 2015

David Ahern's `[RFC PATCH 00/29] net: VRF support`, dated **2015-02-04**, explicitly framed the problem as different from network namespaces.

The RFC said that Linux VRF support had been requested for years, that an older out-of-tree patch had existed, and that networking vendors were carrying custom solutions. It argued that namespaces were a poor fit for the scale of routing VRFs and proposed a model in which VRFs could be nested inside a network namespace.

Evidence:

- RFC cover: <https://lwn.net/Articles/632522/>
- Message-ID: `<1423100070-31848-1-git-send-email-dsahern@gmail.com>`
- archived date: 2015-02-04

### What this proves

- a public upstream design discussion existed by 4 February 2015;
- the proposal was motivated in part by a claimed scale mismatch between netns and large VRF counts;
- the author explicitly distinguished VRF from netns rather than presenting VRF as a renamed namespace feature.

### What this does not prove

- that this was the first Linux VRF implementation of any kind;
- the exact code ancestry or release identity of the earlier out-of-tree patch mentioned in the RFC;
- that any production network was already running this upstream proposal.

## 2. Device model revision: 27 July 2015

The later `[PATCH net-next 13/16] net: Introduce VRF device driver - v2`, dated **2015-07-27**, gives a much more concrete implementation model.

It describes VRF-lite routing domains as:

- a VRF **master netdevice**;
- an associated routing table;
- routed interfaces enslaved to that master;
- ordinary FIB rules binding the VRF device to the table;
- forwarded traffic using the VRF device as the input interface for rule lookup.

The example interface was already recognizable as the modern operational model:

```text
ip link add vrf1 type vrf table 5
ip rule add iif vrf1 table 5
ip rule add oif vrf1 table 5
ip link set eth1 master vrf1
```

The patch also says the driver "borrows heavily from IPvlan and teaming drivers"; the later merged source header says it is "Based on dummy, team and ipvlan drivers."

Evidence:

- v2 patch: <https://www.mail-archive.com/netdev%40vger.kernel.org/msg71870.html>
- netdev day index: <https://lists.openwall.net/netdev/2015/07/27/>

### Lineage interpretation

This is strong evidence for **implementation borrowing / design ancestry** from dummy, team, and ipvlan code patterns. It is **not** evidence that VRF is a successor to, replacement for, or protocol descendant of those drivers.

No structured `LIN-*` edge is added in this slice because the repository's current lineage vocabulary should not turn a source-level "based on / borrows from" statement into a stronger whole-artifact descent claim.

## 3. Initial mainline VRF commit: 13–14 August 2015

The exact initial mainline commit is:

```text
193125dbd8eb292d88feb201f030889b488b0a02
net: Introduce VRF device driver
```

Author date: **2015-08-13 20:59:10 UTC**  
Committer date: **2015-08-14 05:43:22 UTC**

Canonical commit:

<https://github.com/torvalds/linux/commit/193125dbd8eb292d88feb201f030889b488b0a02>

The commit adds:

- `CONFIG_NET_VRF`, labelled `Virtual Routing and Forwarding (Lite)`;
- `drivers/net/vrf.c`;
- the master-device + associated-table model;
- explicit dependence on `IP_MULTIPLE_TABLES` and `IPV6_MULTIPLE_TABLES`.

The commit message gives the same operational grammar as the July patch: create a VRF master, associate it with a table, enslave routed interfaces, and use ordinary FIB-rule processing.

The merged file header preserves the narrower code-ancestry statement:

```text
Based on dummy, team and ipvlan drivers
```

### Tagged-release boundary

A tag comparison gives a clean bounded result:

- Linux **v4.2** does not contain `drivers/net/vrf.c`;
- Linux **v4.3** does contain it.

Therefore **v4.3 is the first Linux tagged release in this adjacent-tag check that contains the mainline VRF driver**.

This is a source-tree/release boundary, not a first-deployment claim.

## 4. Generalization into l3mdev: September 2015 → Linux 4.4

The next important change is not a second VRF implementation. It is a generalization of VRF-specific hooks into a reusable Layer-3-master abstraction.

The netdev cover `[PATCH net-next 00/11] net: L3 master device`, dated **2015-09-24**, says directly:

- the VRF device is essentially a Layer-3 master associated with a routing table;
- the series generalizes VRF into `l3mdev`;
- VRF is converted to use l3mdev operations;
- direct VRF-specific references are removed as the series progresses.

Evidence:

- series cover: <https://lwn.net/Articles/658471/>
- patch 01/11: <https://lists.openwall.net/netdev/2015/09/25/3>

The exact initial l3mdev mainline commit is:

```text
1b69c6d0ae90b7f1a4f61d5c8209d5cb7a55f849
net: Introduce L3 Master device abstraction
```

Author date: **2015-09-30 03:07:11 UTC**  
Committer date: **2015-09-30 03:40:32 UTC**

Canonical commit:

<https://github.com/torvalds/linux/commit/1b69c6d0ae90b7f1a4f61d5c8209d5cb7a55f849>

It adds `include/net/l3mdev.h`, `net/l3mdev/`, `CONFIG_NET_L3_MASTER_DEV`, and `l3mdev_ops` hooks for FIB-table and route handling.

### Tagged-release boundary

Adjacent tags again give a bounded result:

- Linux **v4.3** does not contain `include/net/l3mdev.h`;
- Linux **v4.4** does contain it.

Therefore **v4.4 is the first adjacent tagged release checked here that contains the l3mdev abstraction**.

### Lineage interpretation

Here the evidence is stronger than mere chronology: the patch-series cover explicitly says it **generalizes the VRF into L3 master device, l3mdev**, and the series converts the VRF driver to use the abstraction.

This supports a high-certainty conceptual/implementation relation:

```text
VRF-specific master-device plumbing
          ↓ explicitly generalized into
l3mdev reusable L3-master abstraction
```

It still does not mean that `l3mdev` is a new routing protocol or that every l3mdev user is descended from VRF at the product level.

## 5. The scaling problem in the original rule plumbing

Early VRF operation relied on ordinary RPDB rules: one input-interface rule and one output-interface rule, per address family, per VRF.

The exact mainline commit that changes this is:

```text
96c63fa7393d0a346acfe5a91e0c7d4c7782641b
net: Add l3mdev rule
```

Author date: **2016-06-08 17:55:39 UTC**  
Committer date: **2016-06-08 18:36:02 UTC**

Canonical commit:

<https://github.com/torvalds/linux/commit/96c63fa7393d0a346acfe5a91e0c7d4c7782641b>

The commit message is unusually explicit about motivation. With N VRFs, the old model accumulated repeated `iif`/`oif` rules whose main difference was table ID. Since the table ID can be obtained from the L3 master device, the new `l3mdev` rule allows those repeated rules to be consolidated into **one rule per address family**.

The UAPI change adds:

```text
FRA_L3MDEV
```

and the commit explicitly preserves the ability for administrators to insert higher-priority per-VRF rules.

The immediately following commit is:

```text
1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0
net: vrf: Add l3mdev rules on first device create
```

It installs the IPv4 and IPv6 l3mdev rules when the first VRF device is created, with default preference **1000**, while allowing the user to replace the default rule.

Canonical commit:

<https://github.com/torvalds/linux/commit/1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0>

### Tagged-release boundary

The public UAPI header provides a direct adjacent-tag test:

- Linux **v4.7** has no `FRA_L3MDEV`;
- Linux **v4.8** has `FRA_L3MDEV`.

Therefore the single-rule l3mdev FIB-rule interface is bounded to **v4.8** in the stable tagged source tree.

### What this does not prove

- VRF itself did not first appear in 4.8; the driver was already present in 4.3;
- l3mdev itself did not first appear in 4.8; the abstraction was already present in 4.4;
- the rule simplification does not replace RPDB. It is implemented **inside the FIB-rule/RPDB machinery**, and higher-priority policy rules continue to coexist with it.

## 6. Userspace chronology: interface existed before the rule simplification

A contemporary iproute2 RFC dated **2015-07-06** already proposed creation of a VRF device with a table binding, based on `iplink_vlan` implementation patterns:

<https://www.spinics.net/lists/netdev/msg334796.html>

iproute2 **4.3.0** release notes later list David Ahern's `add support for VRF device` change:

<https://lwn.net/Articles/662996/>

This matters because it prevents another false linear history. The recognizable userspace object model did not wait for the 4.8 l3mdev-rule optimization.

## 7. Product availability is a separate clock

Cumulus Linux 3.0 was publicly released in **June 2016** with VRF listed as a product feature for multi-tenant Layer-3 Clos designs. Contemporary reporting also states that Cumulus had worked with the kernel community on VRF and added hardware support to the product.

Useful period evidence:

- LWN Cumulus Linux 3.0 release item: <https://lwn.net/Articles/688697/>
- The Register launch report, 2016-06-01: <https://www.theregister.com/2016/06/01/cumulus_linux_30_nos_now_in_the_wild/>
- Cumulus-hosted June 2016 presentation preserved on SlideShare: <https://www.slideshare.net/CumulusNetworks/operationalizing-vrf-in-the-data-center>

The June presentation gives a particularly useful implementation snapshot: Cumulus Linux 3.0 is shown with a 4.1-based kernel and VRF enabled, while upstream feature chronology is listed separately (4.3 basic IPv4 VRF, 4.4 basic IPv6, 4.8 FIB rule, etc.). That strongly indicates a vendor-maintained/backported product implementation rather than a simple identity between the product's kernel version and the contemporary upstream tag.

### Deployment boundary

The evidence recovered here establishes an **available shipping/vendor-supported product lower bound** by June 2016. It does **not** establish the first customer production deployment, first switch actually carrying VRF traffic, or first site-level cutover.

Those operational claims remain open and require a customer case study, configuration archive, support record, presentation with a named deployed network, or equivalent period evidence.

## 8. Evidence-strength matrix

| Claim | Evidence | Certainty |
| --- | --- | --- |
| public upstream VRF discussion existed by 2015-02-04 | dated RFC cover | high |
| VRF device model used master device + table + enslaved interfaces by July 2015 | complete v2 patch | high |
| initial mainline VRF commit is `193125db…` | Torvalds-tree commit object/diff | high |
| first adjacent tagged source-tree presence is v4.3 | v4.2 absence + v4.3 presence | high |
| l3mdev was an explicit generalization of VRF-specific plumbing | patch-series cover + mainline commit | high |
| first adjacent tagged l3mdev presence is v4.4 | v4.3 absence + v4.4 presence | high |
| `FRA_L3MDEV` consolidated repeated VRF rules | commit message + UAPI diff | high |
| automatic first-VRF rules default to preference 1000 | immediate follow-up commit | high |
| first adjacent tagged `FRA_L3MDEV` presence is v4.8 | v4.7/v4.8 UAPI comparison | high |
| Cumulus Linux 3.0 shipped with VRF support | period release reporting + vendor presentation | high for product availability |
| first real customer deployment | not recovered | unknown |
| specific ancestry from the older out-of-tree VRF patch to the merged driver | not recovered | unknown |

## 9. Negative claims to preserve

Do **not** write any of the following from this evidence:

- "network namespaces evolved into VRF";
- "because netns predates VRF, netns caused VRF";
- "VRF first appeared in Linux 4.8";
- "l3mdev replaced policy routing";
- "VRF is derived from team/ipvlan/dummy as a whole feature" merely because code was borrowed from those drivers;
- "Cumulus Linux 3.0 proves the first production deployment";
- "Cumulus Linux 3.0's 4.1 kernel is identical to upstream Linux 4.1 with respect to VRF";
- "Cumulus authorship/copyright proves every upstream VRF change first existed in a named Cumulus product release."

## 10. Remaining excavation targets

1. recover and identify the older out-of-tree VRF patch mentioned in the February 2015 RFC;
2. recover the complete RFC→v2→merged patch-series concordance, not just the driver patch and cover messages;
3. find the exact iproute2 merge commit and first tagged release carrying `ip link ... type vrf` if a stricter userspace release boundary is desired;
4. recover the earliest named customer/site deployment of the Linux VRF device model;
5. only after endpoint records and relation vocabulary are checked, decide whether the explicit VRF→l3mdev generalization merits a structured `LIN-*` edge.

Research update: 2026-09-15.
