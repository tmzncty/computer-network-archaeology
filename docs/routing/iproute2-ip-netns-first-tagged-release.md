# iproute2 `ip netns` first tagged-release provenance

## Scope

This note answers one narrow question left open by the network-namespace worklist: **when did the named/processless `ip netns` command family enter iproute2, and what is the first tagged release snapshot that contains it?**

It does not attempt to finish the Linux kernel network-namespace merge series, recover the first independently distributed iproute2 tarball, or establish first real-world deployment.

## Earlier PID-selected namespace administration

An earlier upstream iproute2 commit, `e2613dc8605e56dbc53890ebbae263f93610bd41` (2008-06-23), added:

`ip link set DEVICE netns PID`

The commit states that `IFLA_NET_NS_PID` moves a network device into the network namespace associated with the target process PID. The patch updates `iplink.c`, the command reference and the `ip(8)` man page.

This is important as an interface-history lower bound: iproute2 could already select a target network namespace by process identity in 2008. It is **not** evidence, by itself, that the later named `ip netns` design descended from this patch.

## Named/processless command family

The exact upstream introduction of the named/processless command family is commit:

- `0dc34c7713bb7055378fe5cbc720d63d0db572a1`
- subject: `iproute2: Add processless network namespace support`
- committed: 2011-07-13
- author: Eric W. Biederman

The commit explicitly adds:

- `ip netns add NAME`
- `ip netns delete NAME`
- `ip netns monitor`
- `ip netns list`
- `ip netns exec NAME cmd ...`
- `ip link set DEV netns NAME`

It also adds `ipnetns.o` to the build and `netns` to the top-level `ip` object dispatcher.

The implementation establishes a persistent userspace naming convention. Namespace file descriptors are opened from `/var/run/netns/<NAME>`. Namespace-specific configuration may be placed below `/etc/netns/<name>`. `ip netns exec` enters the selected network namespace, creates a mount namespace, remounts `/sys`, and bind-mounts namespace-specific configuration into ordinary `/etc` locations for programs that are not themselves namespace-aware.

`ip netns add` creates the named path, calls `unshare(CLONE_NEWNET)`, and bind-mounts `/proc/self/ns/net` onto the path. `ip netns monitor` watches the namespace directory with inotify.

## Tagged-release boundary

The adjacent tagged-release boundary is clean:

- the `v2.6.39` tag is dated 2011-06-29 and its `ip/` tree does **not** contain `ipnetns.c`;
- the processless-netns introduction commit is after `v2.6.39`;
- the `v3.0.0` tag commit is dated 2011-10-10;
- `0dc34c7713bb7055378fe5cbc720d63d0db572a1` is an ancestor of the `v3.0.0` tag;
- `v3.0.0` contains `ip/ipnetns.c` with the named command implementation.

The repository's release-tag sequence has `v2.6.39` immediately before `v3.0.0`. Therefore **iproute2 v3.0.0 is the first tagged release/source snapshot containing the named `ip netns` command family**.

This is deliberately phrased as a tagged-release/source-content claim. The currently recovered evidence does not establish the original publication channel or date of an independently distributed `v3.0.0` tarball.

## Evidence table

| Claim | Primary evidence | Locator | Certainty |
|---|---|---|---|
| PID-selected device move existed by 2008 | commit `e2613dc8605e56dbc53890ebbae263f93610bd41` | commit message; `ip/iplink.c`; `doc/ip-cref.tex`; `man/man8/ip.8` | confirmed |
| Named/processless `ip netns` command family entered upstream on 2011-07-13 | commit `0dc34c7713bb7055378fe5cbc720d63d0db572a1` | commit message; `ip/ip.c`; new `ip/ipnetns.c` | confirmed |
| Persistent names use `/var/run/netns/<NAME>` | same commit | commit message; `NETNS_RUN_DIR`; `get_netns_fd`; `netns_add` | confirmed |
| Per-netns userspace configuration uses `/etc/netns/<name>` | same commit | commit message; `NETNS_ETC_DIR`; `bind_etc` | confirmed |
| `v2.6.39` does not contain `ip/ipnetns.c` | `v2.6.39` tagged tree | `ip/` directory listing | confirmed |
| `v3.0.0` contains the implementation | `v3.0.0` tagged tree | `ip/ipnetns.c`; `ip/ip.c` | confirmed |
| First tagged release snapshot containing `ip netns` is v3.0.0 | adjacent tag + ancestry comparison | `v2.6.39` → intro commit → `v3.0.0` | confirmed |

## Lineage decision

**No `LIN-*` record is created in this batch.**

Two relationships are evidence-bearing but are not descent claims:

1. `ART-0250` **administers** `ART-0231` (Linux network namespaces).
2. The 2008 `netns PID` interface is a chronological predecessor to the 2011 named/processless command family.

The sources do not say that the 2011 design was derived from the 2008 patch. Chronology plus similar vocabulary is insufficient for a `derived-from`, `successor`, or `influenced` edge.

## What this evidence does **not** prove

1. It does not prove when Linux network namespaces as a kernel subsystem became complete or mature.
2. It does not prove the first real-world or production use of `ip netns`.
3. It does not prove the first distribution-package version in Debian, Fedora, Ubuntu, RHEL or another operating system.
4. It does not prove the original public tarball publication date/channel for iproute2 v3.0.0; that stronger distribution-history question remains open.
5. It does not prove that the 2008 PID-selected interface caused or was the implementation ancestor of the 2011 named/processless interface.
6. It does not make the network-namespace kernel merge series complete merely because a userspace command reached a tagged release.

## Remaining gap

The parent worklist item is still partial. Remaining:

- recover the exact Linux network-namespace subsystem merge series and component chronology;
- optionally recover pre-mainline veth patch-series provenance;
- if the stronger distribution claim is needed, recover a contemporary v3.0.0 announcement or original distribution artifact.

## Primary source locations

- PID-selected interface commit: `https://github.com/iproute2/iproute2/commit/e2613dc8605e56dbc53890ebbae263f93610bd41`
- named/processless interface commit: `https://github.com/iproute2/iproute2/commit/0dc34c7713bb7055378fe5cbc720d63d0db572a1`
- v2.6.39 tagged `ip/` tree: `https://github.com/iproute2/iproute2/tree/v2.6.39/ip`
- v3.0.0 `ip/ipnetns.c`: `https://github.com/iproute2/iproute2/blob/v3.0.0/ip/ipnetns.c`

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
