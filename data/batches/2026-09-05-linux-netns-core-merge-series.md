# Batch: Linux network namespace core merge series — 2026-09-05

This batch advances one explicitly open part of the network-namespace worklist: **the exact 2007 core merge-series chronology and its evidence boundaries**.

It does not claim completion of `ip netns` first-release archaeology, first deployment, or the full protocol-family completion history.

## Narrative excavation

- `docs/routing/linux-network-namespace-core-merge-series.md`

## Structured sources

- `SRC-0271` — Eric W. Biederman's 2007-09-08 `[PATCH 00/16] core network namespace support` cover/thread.
- `SRC-0272` — Biederman's 2007-09-13 `Network Namespace status` contemporary merge-status note.
- `SRC-0273` — Linux commit `5f256becd868bf63b70da8f2769033d6734670e9`, basic network-namespace infrastructure.
- `SRC-0274` — Linux commit `9dd776b6d7b0b85966b6ddd03e2b2aae59012ab1`, separate clone/unshare/`CLONE_NEWNET` integration.
- `SRC-0275` — 12/16 Netlink conversion with explicit initial-namespace-only / `-ECONNREFUSED` boundary.
- `SRC-0276` — Linux commit `ce286d327341295f58d89864d746a524287cfdf9`, network-device movement and `NETIF_F_NETNS_LOCAL`.

## Structured artifact update

- `ART-0231` — preserves the existing 2008 early operational/release boundary, while adding the recovered 2007 staged core-integration history and primary-source support.

No new artifact ID is consumed.

## Recovered facts

1. The 2007-09-08 series was explicitly built against `net-2.6.24` and deliberately limited to the **core network stack**.
2. The thread recovers the ordered 00/16 through 16/16 series plus the deliberate 17/16 netfilter safety follow-up.
3. A 2007-09-13 participant status note says the work was only partly merged: David Miller had merged the core, while multiple instances still depended on remaining UI/subsystem work.
4. Exact Torvalds-tree anchor `5f256bec...` introduces the minimal `struct net` and per-namespace lifecycle infrastructure.
5. Exact Torvalds-tree anchor `ce286d32...` implements network-device movement and a namespace-local-device flag.
6. A separate post-series patch, exact mainline anchor `9dd776b6...`, adds `CLONE_NEWNET`, `CONFIG_NET_NS`, and clone/unshare namespace creation while still describing the feature as experimental and under development.
7. Core-series safety fences deliberately kept unconverted paths out of non-initial namespaces: packet reception could be dropped, existing Netlink protocols returned `-ECONNREFUSED`, and netfilter configuration remained init-namespace-only.

## Integration-clock decision

The evidence requires at least three distinct clocks:

- patch-series submission and subsystem-tree acceptance;
- Torvalds-tree mainline incorporation of selected components;
- stable-release / operational-maturity boundary.

These clocks must not be collapsed into one date.

## Lineage decision

**No `LIN-*` record is created.**

The recovered evidence documents internal staged integration of `ART-0231`, not descent between separate artifacts. It also provides no basis for a network-namespace → veth or veth → network-namespace causal lineage edge.

## Explicit negative claims

This batch does **not** prove:

- complete protocol/control-plane namespace isolation in Linux 2.6.24;
- first production deployment or adoption;
- first iproute2 release containing `ip netns`;
- that the 2007 basic-infrastructure commit alone represents operational maturity;
- a causal or derived-from relationship between network namespaces and veth;
- a full exact Torvalds-tree SHA concordance for every numbered 01/16..17/16 patch;
- that `Applied to net-2.6.24` and Torvalds-tree/stable-release timestamps are the same event.

## Remaining work in the parent item

- recover the first iproute2 source release containing `ip netns`;
- optionally recover pre-mainline veth patch-series/prototype evidence;
- trace later protocol-family completion only where needed for operational claims.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
