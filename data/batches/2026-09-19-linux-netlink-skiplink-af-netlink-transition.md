# Research batch — Linux SKIPLINK / Netlink character device → AF_NETLINK transition

Date: 2026-09-19  
Scope: one open root-hunting slice only — recover pre-2.1.15 Netlink/SKIPLINK source and bound the first released `AF_NETLINK` socket-family transition without inventing a Git-era merge commit for pre-Git Linux.

## Why this slice was selected

The root-hunting worklist still explicitly asked for “pre-2.1.15 SKIPLINK/Netlink source and exact first AF_NETLINK socket-family merge commit.” Existing repository coverage started its concrete Netlink chronology at Linux 2.1.15. That left both the earlier character-device implementation and the actual 1997 socket-family release boundary under-specified.

## New facts recovered

### F1 — Linux 1.3.31 is the earliest recovered released SKIPLINK/Netlink boundary

- Official archive date: **1995-10-04**.
- Immediately preceding Linux 1.3.30 archive date: 1995-09-27.
- Evidence:
  - <https://www.kernel.org/pub/linux/kernel/v1.3/>
  - reconstructed 1.3.31 tree: <https://github.com/tbodt/linux-history/blob/89eabf146605aaef62d9b8714a4128f300467858/net/netlink.c>
  - reconstructed 1.3.30→1.3.31 comparison: <https://github.com/tbodt/linux-history/compare/88d15e9d250c95e23194c29888d5ca4f86e37581...89eabf146605aaef62d9b8714a4128f300467858>
- Finding: `net/netlink.c` and `include/net/netlink.h` are added at the 1.3.31 release boundary; the source identifies itself as `SKIPLINK`, names Alan Cox as author, and implements a character-device mechanism using `file_operations`, `register_chrdev`, `netlink_attach`, `netlink_detach`, and `netlink_post`.
- Certainty: **high** for adjacent released-source presence.
- Negative boundary: not proof of Cox's first private prototype or first public patch posting.

### F2 — Linux 2.1.15 is a message-layer transition, still on the character-device transport

- Reconstructed release snapshot: `12980ed0feabd39dc13753d9a11a4673dda84ba1` (`Import 2.1.15`, archival reconstruction only).
- Evidence: <https://github.com/tbodt/linux-history/blob/12980ed0feabd39dc13753d9a11a4673dda84ba1/net/netlink.c>
- Finding: the heading is now `NETLINK`, but the source still registers the Netlink major character device and retains `netlink_attach`/`netlink_post` semantics.
- New high-level code comments associated with ANK describe a standard message format, overrun/loss awareness, state resynchronization by rereading FIB/device lists, and batching.
- Certainty: **high**.
- Negative boundary: Linux 2.1.15 must not be described as the first `AF_NETLINK` socket-family release.

### F3 — `AF_NETLINK` is absent in Linux 2.1.67

- Reconstructed snapshot: `c5a4ebcd4431e607667b63c173d5918b518fe3b2`.
- Evidence: <https://github.com/tbodt/linux-history/blob/c5a4ebcd4431e607667b63c173d5918b518fe3b2/include/linux/socket.h>
- Finding: supported address families stop at `pseudo_AF_KEY` before `AF_MAX`; no `AF_NETLINK`, `PF_NETLINK`, or `AF_ROUTE` alias exists.
- Certainty: **high**.

### F4 — Linux 2.1.68 is the recovered public-release boundary for AF_NETLINK + rtnetlink

- Official archive date: **1997-11-30 23:15**; Linux 2.1.67 is dated 1997-11-29 19:18.
- Evidence:
  - <https://www.kernel.org/pub/linux/kernel/v2.1/>
  - reconstructed 2.1.68 source: <https://github.com/tbodt/linux-history/blob/7f563ad63270d13b8412eb7c89d7b7b44f40d0e1/net/netlink/af_netlink.c>
- Adjacent tree finding: final 2.1.68 adds `AF_NETLINK 16`, `PF_NETLINK`, and `AF_ROUTE`/`PF_ROUTE` aliases; Netlink is restructured around a socket implementation accepting `SOCK_RAW`/`SOCK_DGRAM` and allocating with `sk_alloc(AF_NETLINK, ...)`.
- The same transition creates the structured rtnetlink network-object message family (`RTM_*` link/address/route/neighbour/rule objects and multicast groups).
- Certainty: **high** for the public release/tree boundary.

### F5 — the old device path overlaps with the new socket implementation

- Evidence: the Linux 2.1.68 `af_netlink.c` source contains `CONFIG_NETLINK_DEV` / `NL_EMULATE_DEV` compatibility code.
- Finding: the migration was not an atomic “delete old API, introduce new API” event; device emulation coexisted with AF_NETLINK.
- Certainty: **high**.

### F6 — RFC 3549 supplies explicit participant attribution for the evolution

- Document: RFC 3549, *Linux Netlink as an IP Services Protocol*, July 2003.
- Locator: section 6, Acknowledgements.
- Evidence: <https://www.rfc-editor.org/rfc/rfc3549.html#section-6>
- Finding: the RFC credits Alexey Kuznetsov with extending Netlink to the IP-service delivery model and states that the original Netlink character device was written by Alan Cox.
- Certainty: **high** for the attribution and documented extension relation.
- Negative boundary: this does not prove line-by-line source descent or assign every intermediate patch to either person.

### F7 — “first AF_NETLINK merge commit” is an anachronistic research target for 1997

- Linux 2.1.68 predates Git.
- The `tbodt/linux-history` SHAs used above are later reconstructed import commits for reproducible tree comparison.
- Finding: those SHAs must not be presented as contemporaneous 1997 integration commits. The defensible current object is the dated **release/patch transition** plus any surviving contemporary mail/patch artifact recovered later.
- Certainty: **high**.

## Candidate lineage relation

### Alan Cox character-device Netlink → Kuznetsov-era Netlink IP-service/socket model

- Relation intended: explicit extension/generalization, not merely chronological succession.
- Evidence: RFC 3549 section 6 plus adjacent kernel source generations.
- Certainty: **high** that the later IP-service model is described by participants as an extension of Netlink and that Cox wrote the original character device.
- Structured edge decision: **not minted in this batch**. Existing lineage vocabulary should be checked before encoding this as `successor-of`, `derived-from`, or another stronger relation. Prefer an eventual term such as `extended-into` / `generalized-into` if supported by schema policy.

## PF_ROUTE boundary

Linux 2.1.68 defines `AF_ROUTE` as an `AF_NETLINK` alias “to emulate 4.4BSD”; RFC 3549 also discusses BSD routing sockets as prior control/forwarding separation work.

This supports historical comparison and compatibility intent, but **does not prove source-code descent or a direct PF_ROUTE → Netlink implementation lineage**. Keep the existing repository model of BSD PF_ROUTE and Linux rtnetlink as distinct control-interface families unless stronger provenance is found.

## Explicit non-proofs

This batch does not prove:

1. the date/content of the first private or posted SKIPLINK patch before Linux 1.3.31;
2. that Linux 1.3.31 was the first real deployment of Netlink;
3. that Linux 2.1.15 introduced the socket family;
4. a contemporaneous 1997 Git merge SHA for Linux 2.1.68;
5. that PF_ROUTE caused Netlink or supplied its source code;
6. that character-device compatibility disappeared in Linux 2.1.68;
7. that every modern Netlink/rtnetlink semantic was already stable in these releases.

## Files added / proposed

Added in this batch:

- `docs/routing/linux-netlink-skiplink-to-af-netlink.md`
- `data/batches/2026-09-19-linux-netlink-skiplink-af-netlink-transition.md`

Recommended follow-up edits at merge/reconciliation time:

- update `docs/methodology/root-hunting-master-worklist.md` so the old “exact merge commit” wording becomes a pre-Git release/patch provenance target;
- cross-link the new chronology from `docs/routing/route-routed-pfroute-netlink-iproute2.md`;
- add structured source/artifact/lineage rows only after confirming current ID reservations and relation vocabulary.

## Remaining work

- recover an Alan Cox pre-1.3.31 submission/mail artifact;
- recover contemporary 2.1.68 integration discussion and individual subpatch attribution;
- map the 2.1.68 rtnetlink UAPI into the earliest iproute source snapshot;
- determine the release boundary at which `/dev/netlink` emulation is finally removed.
