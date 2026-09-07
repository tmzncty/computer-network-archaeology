# Linux network namespace core merge series

## Scope

This note recovers one explicitly open question: **what exactly was the 2007 Linux core network-namespace merge series, and how should that core integration be separated from later namespace-creation and subsystem-completion work?**

It does not resolve the first iproute2 release containing `ip netns`, first real-world deployment, or the full post-2.6.24 protocol-family completion chronology.

## Multiple clocks, not one feature commit

The surviving primary record supports a staged chronology rather than a single "network namespaces arrived" event.

1. **2007-09-08 — core series posted.** Eric W. Biederman posted `[PATCH 00/16] core network namespace support` against the then-current `net-2.6.24` tree. The cover letter explicitly limits the patchset to the **core of the network stack** so the set remains reviewable.
2. **2007-09-12 to 2007-09-13 — subsystem-tree core integration.** David Miller's replies record application of core-series patches to `net-2.6.24`. Biederman's 2007-09-13 status note says the work was only **partly merged**: Miller had merged the core, but multiple namespace instances still depended on remaining user-interface and subsystem work.
3. **2007-09-26 — separate namespace-creation patch posted.** A later patch adds `CLONE_NEWNET`, `CONFIG_NET_NS`, and the `clone(2)` / `unshare(2)` creation path. Its own message still describes network namespaces as experimental and under development. This patch is not part of the numbered 00/16 series.
4. **2007-10-10 — selected Torvalds-tree anchors.** The mainline history contains exact commits for the basic namespace infrastructure (`5f256becd868bf63b70da8f2769033d6734670e9`), network-device movement (`ce286d327341295f58d89864d746a524287cfdf9`), and the separate clone/unshare path (`9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1`).
5. **2008-01-24 — Linux 2.6.24 release boundary.** The repository already records this stable-release generation as the early operational boundary. The 2007 merge chronology is a substrate/integration clock and does not by itself move that maturity claim back into 2007.

`Applied to net-2.6.24` in a contemporary maintainer reply and a later visible commit in the Torvalds tree are therefore two different timing claims and should not be collapsed.

## Recovered 00/16 series

The contemporary Linux Containers thread preserves the following ordered series:

| Patch | Subject |
|---|---|
| 00/16 | `core network namespace support` |
| 01/16 | `appletalk: In notifier handlers convert the void pointer to a netdevice` |
| 02/16 | `net: Don't implement dev_ifname32 inline` |
| 03/16 | `net: Basic network namespace infrastructure.` |
| 04/16 | `net: Add a network namespace parameter to tasks` |
| 05/16 | `net: Add a network namespace tag to struct net_device` |
| 06/16 | `net: Add a network namespace parameter to struct sock` |
| 07/16 | `net: Make /proc/net per network namespace` |
| 08/16 | `net: Make socket creation namespace safe.` |
| 09/16 | `net: Initialize the network namespace of network devices.` |
| 10/16 | `net: Make packet reception network namespace safe` |
| 11/16 | `net: Make device event notification network namespace safe` |
| 12/16 | `net: Support multiple network namespaces with netlink` |
| 13/16 | `net: Make the device list and device lookups per namespace.` |
| 14/16 | `net: Factor out __dev_alloc_name from dev_alloc_name` |
| 15/16 | `net: Implement network device movement between namespaces` |
| 16/16 | `net: netlink support for moving devices between network namespaces.` |
| 17/16 | `net: Disable netfilter sockopts when not in the initial network namespace` |

The `17/16` patch is a deliberate safety follow-up. Biederman explained during review that keeping netfilter configuration isolated to the initial namespace was required to make the core-networking target complete enough while netfilter itself still lacked multi-namespace support.

This note recovers the **series identity, order, scope, staged acceptance, and selected exact mainline anchors**. It does not claim a full one-to-one Torvalds-tree SHA concordance for every numbered patch.

## Exact mainline anchors

### Basic infrastructure — `5f256becd868bf63b70da8f2769033d6734670e9`

`[NET]: Basic network namespace infrastructure.` introduces the minimal `struct net`, per-network-namespace init/exit registration, namespace lifetime/reference machinery, and a list of network namespaces. This is the direct mainline anchor for the 03/16 substrate.

The wording is important: the structure is explicitly described as a minimal starting point that would grow as global networking state became per-namespace.

### Device movement — `ce286d327341295f58d89864d746a524287cfdf9`

`[NET]: Implement network device movement between namespaces` adds `NETIF_F_NETNS_LOCAL` and `dev_change_net_namespace()`. From the rest of the network stack, a move is modeled as unregistering the device in the source namespace and registering it in the destination namespace. Namespace teardown pushes movable devices back to `init_net`; namespace-local devices such as loopback are not movable.

This is an interface/lifecycle milestone. It is not evidence of first production use.

### Namespace creation — `9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1`

`[NET]: Add network namespace clone & unshare support.` adds `CLONE_NEWNET`, the `CONFIG_NET_NS` gate, `copy_net_ns()`, and wiring through `fork`/`nsproxy` for `clone` and `unshare` creation. The original patch was posted after the 00/16 series and explicitly calls the feature experimental and under development.

That makes the creation API a **separate integration stage**, not patch 18 of the original core series and not evidence that the September 8 core submission was already a complete user-visible implementation.

## Safety fences are historical evidence, not footnotes

The core series deliberately prevented unconverted code from behaving as if it were namespace-safe:

- **10/16 packet reception:** receive handlers were made to drop packets outside the initial namespace until the corresponding network stacks had been converted.
- **12/16 Netlink:** each Netlink socket acquired a namespace, but existing Netlink protocols initially remained available only in the initial namespace; clients in another namespace received `-ECONNREFUSED` until that protocol was converted.
- **17/16 netfilter:** netfilter socket-option configuration remained restricted to the initial namespace until netfilter gained multi-namespace support.

These fences are direct negative evidence against describing the core merge as "the whole Linux network stack became independently namespaced in 2.6.24." The engineering strategy was incremental conversion with explicit containment of unsupported paths.

## Evidence table

| Claim | Primary evidence | Locator | Certainty |
|---|---|---|---|
| The 00/16 set targeted `net-2.6.24` and only the core network stack | `SRC-0271` | cover-letter opening scope statement and thread | confirmed |
| The work was only partly merged; the core was merged before multiple instances were enabled | `SRC-0272` | opening paragraphs | confirmed |
| `struct net` and per-netns lifecycle infrastructure have an exact mainline anchor | `SRC-0273` | commit message; `include/net/net_namespace.h`; `net/core/net_namespace.c` | confirmed |
| `CLONE_NEWNET` / clone / unshare arrived in a separate later integration patch | `SRC-0274` | commit message and `sched.h`/`fork.c`/`nsproxy.c`/`net/Kconfig`/`net_namespace.c` diff | confirmed |
| Netlink initially retained an init-namespace-only safety boundary | `SRC-0275` | 12/16 opening explanation | confirmed |
| Device movement and the namespace-local device flag have an exact mainline anchor | `SRC-0276` | commit message; loopback/netdevice/dev.c diff | confirmed |

## Lineage decision

**No `LIN-*` record is created.**

The recovered material describes staged revisions and components within `ART-0231` itself. It does not establish a descent relationship between two distinct artifacts. It also does not justify a causal lineage edge between network namespaces and veth: the separately documented veth evidence supports contemporary intended composition, not "A caused B" or "B derived from A."

## What this evidence does **not** prove

1. It does not prove that Linux 2.6.24 provided complete namespace isolation for every networking protocol and control plane; the packet, Netlink, and netfilter safety fences prove that important paths were intentionally still restricted.
2. It does not prove a first production deployment or adoption date.
3. It does not prove that `ip netns` existed in the first iproute2 release contemporaneous with the kernel core merge; that userspace release boundary remains a separate open question.
4. It does not prove that the core infrastructure commit alone made network namespaces operationally mature.
5. It does not prove a causal or derived-from relationship between network namespaces and veth merely because their 2007 development overlapped and they were designed to compose.
6. It does not claim that every 01/16..17/16 patch has been mapped here to an exact full Torvalds-tree SHA; only selected anchor commits have been independently pinned.
7. Maintainer replies saying a patch was applied to `net-2.6.24` establish subsystem-tree acceptance at that point, not the same timestamp as incorporation into Linus Torvalds's tree or a stable release.

## Remaining gap

The parent work item is now narrower:

- recover the first iproute2 source release containing `ip netns`;
- optionally recover pre-mainline veth patch-series/prototype evidence;
- if a later operational study needs it, trace protocol-family completion beyond the 2.6.24 core staging without retroactively treating the core merge as full-stack completion.

## Primary source locations

- Core 00/16 cover/thread: `https://forum.openvz.org/index.php?goto=20023&rev=19978%3A19977%3A19969%3A19972&t=msg&th=3866`
- Contemporary series index: `https://www.spinics.net/lists/linux-containers/thrd50.html`
- 2007-09-13 status: `https://lists.openvz.org/pipermail/devel/2007-September/041006.html`
- 12/16 Netlink safety boundary: `https://lists.openvz.org/pipermail/devel/2007-September/040800.html`
- Clone/unshare original patch: `https://lists.openwall.net/netdev/2007/09/26/56`
- Mainline basic infrastructure: `https://github.com/torvalds/linux/commit/5f256becd868bf63b70da8f2769033d6734670e9`
- Mainline device movement: `https://github.com/torvalds/linux/commit/ce286d327341295f58d89864d746a524287cfdf9`
- Mainline clone/unshare: `https://github.com/torvalds/linux/commit/9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1`

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
