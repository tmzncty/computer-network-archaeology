# Batch: iproute2 `ip netns` first tagged-release provenance — 2026-09-05

This batch advances one explicitly open part of the network-namespace worklist: **`ip netns` first-release archaeology**.

It closes the first **tagged release/source snapshot** boundary, not the Linux kernel network-namespace merge series or the stronger first-public-tarball question.

## Narrative excavation

- `docs/routing/iproute2-ip-netns-first-tagged-release.md`

## Structured sources

- `SRC-0271` — 2008 iproute2 `IFLA_NET_NS_PID` / `ip link set DEVICE netns PID` commit.
- `SRC-0272` — 2011 processless named-network-namespace introduction commit.
- `SRC-0273` — adjacent `v2.6.39` → `v3.0.0` tagged-release/source-tree boundary.

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

## Remaining work in the parent item

- recover the exact kernel network-namespace subsystem merge series and component chronology;
- optionally recover pre-mainline veth patch-series history;
- if needed, recover a contemporary v3.0.0 announcement or original distribution artifact to support the stronger public-distribution claim.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
