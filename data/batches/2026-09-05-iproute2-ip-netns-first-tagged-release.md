# Batch: iproute2 `ip netns` first tagged-release provenance — 2026-09-05

This batch advances one explicitly open part of the network-namespace worklist: **`ip netns` first-release archaeology**.

It closes the first **tagged release/source snapshot** boundary, not the Linux kernel network-namespace merge series or the stronger first-public-tarball question.

## Narrative excavation

- `docs/routing/iproute2-ip-netns-first-tagged-release.md`

## Structured sources

- `SRC-0286` — 2008 iproute2 `IFLA_NET_NS_PID` / `ip link set DEVICE netns PID` commit.
- `SRC-0287` — 2011 processless named-network-namespace introduction commit.
- `SRC-0288` — adjacent `v2.6.39` → `v3.0.0` tagged-release/source-tree boundary.

## Structured artifact

- `ART-0250` — iproute2 `ip netns` named network-namespace command family.

## Recovered facts

1. A PID-selected userspace namespace-control interface existed in iproute2 by 2008-06-23: `ip link set DEVICE netns PID`.
2. The named/processless `ip netns` command family was introduced upstream by commit `0dc34c7713bb7055378fe5cbc720d63d0db572a1` on 2011-07-13.
3. That commit adds `add`, `delete`, `monitor`, `list`, `exec`, and named `ip link ... netns NAME` support.
4. It persists namespace handles under `/var/run/netns/<NAME>` and supports namespace-specific configuration under `/etc/netns/<name>`.
5. `v2.6.39` does not contain `ip/ipnetns.c`; `v3.0.0` does, and the introduction commit is an ancestor of the v3.0.0 tag.
6. Therefore **v3.0.0 is the first tagged iproute2 release/source snapshot containing the named `ip netns` command family**.

## Lineage decision

**No `LIN-*` record is created.**

The 2008 PID-selected interface is a chronological predecessor, but the recovered sources do not explicitly establish implementation descent or causal influence into the 2011 named/processless command family. `ART-0250` records only a functional `administers` relationship to `ART-0231`.

## Explicit negative claims

This batch does **not** prove:

- exact completion/maturity of the kernel network-namespace subsystem;
- first production deployment or first user adoption;
- first Linux distribution package containing the command;
- original public tarball publication date/channel for v3.0.0;
- that the 2008 PID interface caused or was the code ancestor of the 2011 named interface;
- that a userspace release date can be substituted for kernel merge chronology.

## Remaining work in the parent item (as recorded on 2026-09-05)

- recover the exact kernel network-namespace subsystem merge series and component chronology;
- optionally recover pre-mainline veth patch-series history;
- if needed, recover a contemporary v3.0.0 announcement or original distribution artifact to support the stronger public-distribution claim.

## Integration follow-up — 2026-09-08

The [companion core batch](2026-09-05-linux-netns-core-merge-series.md) and [study](../../docs/routing/linux-network-namespace-core-merge-series.md) now recover the September 2007 series identity/order, contemporary partial-merge status and selected exact mainline anchors using `SRC-0271..0276`. The original scope and negative claims above remain valid for this userspace batch. A full numbered-patch Torvalds-tree SHA concordance, later protocol-family completion where needed, optional pre-mainline veth evidence, and first-public-v3.0.0-distribution provenance remain open; combining the studies does not establish maturity, deployment or causal lineage.

### Qualified source-ID migration

This subsection records the first migration as incorporated in PR #12 head `8a1637dc7ed5054db8b544838cbb6305f9cde92a`; its integrated IDs below are historical, not the current userspace IDs after the second migration.

Parallel PRs #11 and #12 assigned different sources to the same three IDs. This integration keeps the six kernel identities from #11 at `473dd0e761079f217c6ddee8c9c930095ad50615` and moves only the three userspace identities below. Every old ID in this table is qualified by **original PR #12 head `d60fa218d928adb112d6914b299431223a286c5e`**, not a global alias. Original commits remain unchanged; apart from the root ID and record path, source metadata, extracted claims and access/review dates are preserved.

| Original #12 ID | Integrated ID | Unchanged source identity / canonical location |
|---|---|---|
| `SRC-0271` | `SRC-0277` | PID interface, commit [`e2613dc8605e56dbc53890ebbae263f93610bd41`](https://github.com/iproute2/iproute2/commit/e2613dc8605e56dbc53890ebbae263f93610bd41) |
| `SRC-0272` | `SRC-0278` | Processless/named introduction, commit [`0dc34c7713bb7055378fe5cbc720d63d0db572a1`](https://github.com/iproute2/iproute2/commit/0dc34c7713bb7055378fe5cbc720d63d0db572a1) |
| `SRC-0273` | `SRC-0279` | Adjacent v2.6.39 → v3.0.0 tagged-tree/ancestry boundary, [`v3.0.0/ip/ipnetns.c`](https://github.com/iproute2/iproute2/blob/v3.0.0/ip/ipnetns.c) |

### Second qualified migration after RFC source adoption — 2026-09-08

Main `a02d581c86c77b2baca14d46e5741748c616e883` now uses `SRC-0277..0279` for RFC 270/271/331, while the three iproute2 identities at PR #12 head `8a1637dc7ed5054db8b544838cbb6305f9cde92a` still use those same numbers. This second migration applies only to that exact userspace slice; it neither renames the RFC sources nor changes the earlier migration table.

| ID at #12 `8a1637dc...` | Current userspace ID | Unchanged source identity |
|---|---|---|
| `SRC-0277` | `SRC-0286` | PID interface, git `e2613dc8605e56dbc53890ebbae263f93610bd41` |
| `SRC-0278` | `SRC-0287` | Processless/named introduction, git `0dc34c7713bb7055378fe5cbc720d63d0db572a1` |
| `SRC-0279` | `SRC-0288` | Adjacent v2.6.39 → v3.0.0 tagged-tree/ancestry boundary |

The 2026-09-08 08:52 UTC snapshot of main and all four open PR heads (#11, #12, #14, #20) contains 276 distinct source IDs through `SRC-0285`, including both source JSON and the fully parsed quoted CSV ledger. `SRC-0286..0288` were unused; `SRC-0280..0285` belong to the open veth PR #20 and are not reassigned. Allocation must be rechecked at merge time. All metadata, original primary-source locations, claims, access/review dates and negative boundaries remain unchanged apart from root IDs and current typed citations. Three discovery-ledger rows are appended without rewriting existing rows. The old IDs in both tables are commit-qualified historical mappings, never global aliases.

Research-branch validation does not prove conflict-free main/all-open integration. Combining with main or veth still requires retaining each study's queue/worklist entries, the RFC identities, the kernel sources and both userspace artifact links.

Companion links are navigation; the original direct primary-source locations and evidence limits remain authoritative.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
