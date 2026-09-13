# Linux veth: public proposal, interface revisions and upstream provenance

## Scope

This note follows a bounded public record: **the June 2007 veth proposal, July interface-revision reports, an August subsystem-acceptance statement, and the separately dated preserved mainline introduction**. It also asks what the initial source says about its relation to network namespaces.

It does **not** attempt to finish the broader network-namespace merge series or the first-release archaeology of `ip netns`.

## Recovered upstream introduction

The exact mainline introduction is Linux commit:

- `e314dbdc1c0dc6a548ecf0afce28ecfd538ff568`
- subject: `[NET]: Virtual ethernet device driver.`
- author date: 2007-09-25 23:14:46 UTC (Pavel Emelyanov)
- committer date: 2007-10-10 23:47:46 UTC (David S. Miller)
- signed off by Pavel Emelyanov and David S. Miller; Patrick McHardy acked the change; the message also credits Daniel Lezcano for bug fixes.

The commit adds `CONFIG_VETH`, wires `veth.o` into `drivers/net/Makefile`, and introduces `drivers/net/veth.c` as a new driver.

The commit describes `veth` as a link-layer pair of Ethernet devices: traffic sent into one end appears at the peer. It explicitly says the driver's main intended use is communication between network namespaces, while also saying the pair can be used by itself. The `newlink` path was arranged so that peer creation in a separate namespace would be straightforward once the needed namespace support was present in the kernel.

That wording matters historically. It establishes a **contemporary intended-use/composition relationship** between `veth` and network namespaces. It does not establish that one artifact descended from the other.

The two Git timestamps describe this preserved object. Neither dates the first prototype, the first public submission, or the first appearance of the change in Linus's first-parent history. Source: [exact commit metadata and diff](https://github.com/torvalds/linux/commit/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568), `SRC-0269`.

## Recovered public proposal and revision reports

These are distinct document events, not competing dates for a single invention. Dates below follow the original message headers; the saved v3/v4 messages are covers, not complete intermediate patch sets.

| Date / kind of evidence | What the original message establishes | Locator |
| --- | --- | --- |
| 2007-06-06 — public proposal | Pavel Emelianov describes paired link-layer devices, intended namespace use and a different interface from etun. He specifically credits Eric W. Biederman's patch for the **ethtool interface**, not the whole driver. | [Proposal](https://lists.openwall.net/netdev/2007/06/06/30), `<4666CEAA.8010903@openvz.org>`, opening description and paragraph beginning “Eric, since ethtool interface…”; `SRC-0280`. |
| 2007-06-06 — review suggestion | Patrick McHardy objects to a dedicated `VETH_INFO_MAC` because a generic MAC attribute exists, and asks about single-device creation followed by an enslave operation. | [Review](https://lists.openwall.net/netdev/2007/06/06/35), `<4666D296.2000002@trash.net>`, paragraph beginning “The rtnl_link codes looks fine”; `SRC-0281`. |
| 2007-07-11 — v2.1 resubmission | The opening says the netlink **NEWLINK** interface is now in the netdev tree and resubmits veth for inclusion. The description contrasts etun's sysfs interface; the accompanying complete patch still uses dedicated MAC attributes and a string-valued peer name. | [v2.1](https://lists.openwall.net/netdev/2007/07/11/40), `<4694A363.2070406@openvz.org>`, opening, `veth_newlink`, `veth_policy` and `include/net/veth.h`; `SRC-0282`. |
| 2007-07-12 — v3 cover | The author reports making a generic link-creation routine for veth, other drivers creating several devices, and `rtnl_newlink()` reuse. This cover does not itself name or contain the helper's implementation. | [v3 cover](https://lists.openwall.net/netdev/2007/07/12/38), `<4695F0BF.1000305@openvz.org>`, “Changes from v.2.1”; `SRC-0283`. |
| 2007-07-19 — v4 cover | The author reports reserving `struct ifinfomsg` space in the `IFLA_INFO_DATA` part, “not used yet”, and retains the generic-routine changelog and McHardy acknowledgement. | [v4 cover](https://lists.openwall.net/netdev/2007/07/19/45), `<469F2DE7.9090407@openvz.org>`, “Changes from v.3” and “Changes from v.2.1”; `SRC-0284`. |
| 2007-08-08 local / 2007-08-09 UTC — subsystem statement | David Miller says “I've added it to my net-2.6.24”. The header is **8 August 22:18:27 −0700 = 9 August 05:18:27 UTC**, explaining the archive's August 9 URL. | [Acceptance reply](https://lists.openwall.net/netdev/2007/08/09/24), `<20070808.221827.05602119.davem@davemloft.net>`, Date header and final reply sentence; `SRC-0285`. |

The August reply is a statement about **Miller's subsystem tree**. It does not identify that tree's exact object or prove equality with the later September/October commit. It is neither a Linus merge-date record nor a deployment report. The June/July sources establish public discussion by 6 June, not that this was the earliest proposal or prototype. The original messages spell some author names differently; Message-IDs and exact URLs disambiguate the cited documents.

## What changed in the actual interface

Compare the complete [June proposal](https://lists.openwall.net/netdev/2007/06/06/30) and [July v2.1 patch](https://lists.openwall.net/netdev/2007/07/11/40) with the complete four-file introduction diff, not merely with the cover-message summaries. The endpoints show concrete changes; the missing v3/v4 subpatches still prevent a complete intermediate patch concordance.

| Property | June / July v2.1 patches | Preserved `e314dbdc` source |
| --- | --- | --- |
| MAC address input | `VETH_INFO_MAC` and `VETH_INFO_PEER_MAC` are dedicated binary attributes. | Those enum names disappear. `veth_validate` checks generic `IFLA_ADDRESS`; both endpoints use that attribute or a random-address fallback. [Driver lines 293–302, 352–369](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/drivers/net/veth.c#L293). |
| Peer attribute | `VETH_INFO_PEER` is a `NLA_STRING` peer name and has implicit enum value **2**, after `UNSPEC` and `MAC`. | The same name has enum value **1**. Its payload has an `ifinfomsg` prefix followed by generic IFLA attributes; the name comes from `IFLA_IFNAME`. This is **not an unchanged ABI**. [Header lines 4–9](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/include/net/veth.h#L4), [driver lines 315–348](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/drivers/net/veth.c#L315). |
| Peer creation | `alloc_netdev` plus manual copying of link fields, marked “in sync with rtnl_newlink”. | `rtnl_create_link(ifname, &veth_link_ops, tbp)` creates the peer. This proves the final driver's helper use, not the helper's own introduction commit. [Driver line 348](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/drivers/net/veth.c#L348). |
| Reserved header | The v4 cover reports unused `ifinfomsg` space broadly within `IFLA_INFO_DATA`. | The precise location is the **head of `VETH_INFO_PEER`**. The parser skips `sizeof(struct ifinfomsg)` because its contents are not useful yet; do not place that prefix at the head of all `IFLA_INFO_DATA`. [Driver lines 317–331](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/drivers/net/veth.c#L317). |
| Narrow ethtool credit | The June prose expressly credits Biederman's ethtool interface; both early patches expose `peer_ifindex`. | The final file retains that specific credit and the peer-index readout. This supports property-level attribution, not whole-driver etun/OpenVZ descent or byte-identical ethtool code. [Driver header and lines 48/93](https://github.com/torvalds/linux/blob/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568/drivers/net/veth.c#L7). |

The record also preserves a rejected or unrealized option: McHardy's June question about creating one device and binding it later is **not** the final driver's pair-creation design. The final `veth_newlink` registers the peer, then the local device, and ties them together. Review suggestions are not automatically implementation facts; this comparison does not assign every final change to one review message.

**Transcription boundary:** the contemporary prose, including the final commit message, contains `RTM_NRELINK`. That spelling is a typo, not a separate API. When explaining the netlink path, use `RTM_NEWLINK` / NEWLINK based on the July opening and actual `newlink` code; preserve and identify the original spelling if quoting it. No kernel execution or namespace-deployment experiment is claimed by this source comparison.

## Stable-release boundary

A direct adjacent-tag check gives a clean lower bound:

- `drivers/net/veth.c` is absent from the Linux `v2.6.23` tag;
- `drivers/net/veth.c` is present in the Linux `v2.6.24` tag.

The `v2.6.24` file identifies itself as `drivers/net/veth.c`, carries 2007 OpenVZ / SWsoft Inc copyright, names Pavel Emelianov as author, and reports driver version `1.0`.

Therefore **Linux 2.6.24 is the first stable mainline release containing this `veth` driver**. This is a release-content claim, not a first-deployment claim.

## Evidence table

| Claim | Primary evidence | Locator | Certainty |
|---|---|---|---|
| Exact mainline introduction | Linux commit `e314dbdc1c0dc6a548ecf0afce28ecfd538ff568` | commit message + Kconfig/Makefile/new `drivers/net/veth.c` diff | confirmed |
| Pair semantics are part of the initial implementation | same commit | commit message; `veth_xmit`; Kconfig help | confirmed |
| Network namespaces were a stated main use | same commit | commit message | confirmed |
| Peer creation was shaped for future separate-namespace creation | same commit | commit message + `veth_newlink` diff | confirmed |
| OpenVZ/SWsoft/Pavel authorship provenance appears in released source | Linux `v2.6.24` `drivers/net/veth.c` | file header | confirmed |
| First stable mainline release containing the file is 2.6.24 | adjacent `v2.6.23` / `v2.6.24` tag check | `drivers/net/veth.c` path | confirmed |

## What this evidence does **not** prove

1. It does not prove the date of the first production or user deployment of `veth`.
2. It does not prove when network namespaces as a whole became complete or operationally mature.
3. It does not prove the first iproute2 release containing `ip netns`.
4. The OpenVZ/SWsoft copyright and author affiliation do not, by themselves, prove that Linux mainline `veth` was architecturally derived from one specific earlier OpenVZ virtual-networking implementation.
5. The fact that the veth commit discusses network namespaces does not justify a lineage edge saying “network namespaces caused veth” or “veth descended from network namespaces.” The source supports intended composition/use, not descent.
6. The commit's timing does not establish first public discussion, first prototype, or first out-of-tree patch. The recovered June–August messages narrow the public record, but an earliest-event claim and complete intermediate patch history remain unproved.
7. The August subsystem statement does not establish Linus's first-parent integration date, an identical September/October object, or deployment.

## Lineage decision

**No lineage-ledger edge is added in this batch.**

`ART-0249` is related to `ART-0231` (Linux network namespace) by an explicitly documented functional/composition relationship: the initial veth commit says namespace communication is a main use and anticipates separate-namespace peer creation. That is not enough evidence for `derived-from`, `successor`, `influenced`, or another descent relation.

## Remaining gap

The parent worklist item remains only partially complete. Still needed:

- exact network-namespace subsystem merge series and component chronology;
- first iproute2 release / source snapshot containing `ip netns`;
- complete intermediate veth subpatches, earlier prototype evidence and specific OpenVZ implementation provenance sufficient to test stronger lineage claims; the public proposal/revision/acceptance slice above is now recovered, not the whole history.

The separate network-namespace and `ip netns` research packages must be retained when combined with this note. This veth supplement neither redoes their excavation nor marks their release, maturity or deployment questions resolved.

## Primary source locations

- Linux commit `e314dbdc1c0dc6a548ecf0afce28ecfd538ff568`: `https://github.com/torvalds/linux/commit/e314dbdc1c0dc6a548ecf0afce28ecfd538ff568`
- Linux v2.6.24 source: `https://github.com/torvalds/linux/blob/v2.6.24/drivers/net/veth.c`
- Linux v2.6.23 tree used for the adjacent-tag absence check: `https://github.com/torvalds/linux/tree/v2.6.23/drivers/net`

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
