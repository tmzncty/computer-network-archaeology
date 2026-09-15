# Linux network namespaces, VRF/l3mdev and RPDB: three different ways to split one machine into routing worlds

## Why these mechanisms must not be collapsed

Modern Linux can isolate or partition networking in several ways:

```text
network namespace
VRF device / l3mdev
RPDB + multiple routing tables
```

They overlap operationally, but they are not versions of one feature.

A root-hunting archive must ask what each one isolates and which earlier mechanism it builds on.

For exact VRF/l3mdev patch, commit, tagged-release and product-availability chronology, see [`linux-vrf-l3mdev-mainline-chronology.md`](linux-vrf-l3mdev-mainline-chronology.md). That evidence pins the VRF driver to Linux v4.3, the generalized l3mdev abstraction to v4.4, and the single l3mdev FIB-rule interface to v4.8 without collapsing those three milestones.

## 1. RPDB and multiple FIB tables come first in this lineage

The rtnetlink header introduced in Linux 2.1.68 already contains rule operations:

```text
RTM_NEWRULE
RTM_DELRULE
RTM_GETRULE
```

and reserved routing-table identifiers:

```text
RT_TABLE_DEFAULT
RT_TABLE_MAIN
RT_TABLE_LOCAL
```

This is the early Linux policy-routing world: several route tables can exist, and rules decide which lookup path applies.

The abstraction is still one networking stack:

```text
one network namespace
        ↓
RPDB chooses table/action
        ↓
multiple FIB tables
```

## 2. Network namespaces isolate the networking stack itself

`CLONE_NEWNET` is documented since Linux 2.6.24, with implementation work completed only around 2.6.29.

A network namespace isolates resources including:

- devices;
- IPv4 and IPv6 protocol stacks;
- routing tables;
- firewall rules;
- `/proc/net` view;
- `/sys/class/net` view;
- sockets and port-number space;
- UNIX abstract sockets.

This is a much stronger boundary than choosing another route table.

Conceptually:

```text
machine
 ├── netns A
 │    ├── interfaces
 │    ├── addresses
 │    ├── routes/RPDB
 │    ├── firewall
 │    └── sockets
 └── netns B
      ├── different interfaces
      ├── different routes/RPDB
      └── different sockets
```

Each namespace can then contain its own policy-routing system.

## 3. veth connects namespaces without erasing the isolation boundary

The network-namespace model introduces a useful pair abstraction:

```text
veth-A ===== veth-B
```

with each endpoint placed in a different namespace.

This makes the isolation operationally useful: one can build routers, containers and virtual topologies while keeping separate stacks.

Again, this is not “multiple routing tables with a new command.” It is stack replication/isolation.

## 4. `ip netns` is the userspace administration layer

`ip netns` provides persistent naming and administration of network namespaces.

Typical operations include:

```text
ip netns add NAME
ip netns exec NAME ...
ip link set DEV netns NAME
```

The operational lineage is:

```text
CLONE_NEWNET / namespace kernel mechanism
        ↓
namespace file-descriptor and lifecycle APIs
        ↓
iproute2 namespace administration
```

The underlying namespace is a kernel object; the friendly persistent name is a userspace management convention.

## 5. VRF is not a lightweight network namespace

Linux VRF devices solve a different problem.

Kernel VRF documentation says a VRF device plus `ip rules` provides virtual routing and forwarding domains. A VRF is associated with a routing table.

Example:

```text
ip link add vrf-blue type vrf table 10
```

Interfaces can then be enslaved to the VRF device.

The key boundary is documented explicitly: Linux VRF primarily affects Layer 3 and above. Layer-2 tools do not necessarily need to run separately for each VRF.

So:

```text
network namespace
    = broad network-stack isolation

VRF/l3mdev
    = L3 routing-domain separation inside a namespace
```

They can even be nested operationally:

```text
network namespace
      ↓
VRF devices
      ↓
per-VRF FIB tables
```

The exact upstream chronology is now bounded more tightly: initial VRF driver commit `193125dbd8eb…` is present in Linux v4.3 but not v4.2; the later l3mdev abstraction is a separate generalization milestone.

## 6. Before l3mdev rule: per-VRF iif/oif rules

Early VRF operation needed explicit input/output-interface rules such as:

```text
ip rule add iif vrf-blue table 10
ip rule add oif vrf-blue table 10
```

plus IPv6 equivalents.

The 2016 mainline commit `96c63fa7393d…` documents the scaling consequence directly: the same rule shape had to be repeated per VRF and address family, with the table ID as the principal changing value.

This shows that early VRF support was layered directly on the existing RPDB rule machinery.

## 7. Linux 4.8: l3mdev condenses the rule layer

As of Linux 4.8, the kernel supports an `l3mdev` FIB rule. One rule can direct lookups to the table associated with the L3-master device.

The exact mainline changes are:

```text
96c63fa7393d0a346acfe5a91e0c7d4c7782641b
net: Add l3mdev rule

1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0
net: vrf: Add l3mdev rules on first device create
```

The first VRF device creates default IPv4 and IPv6 l3mdev rules at preference 1000, and administrators can replace or outrank the defaults.

So the architecture changes from:

```text
one iif/oif rule per VRF
```

to:

```text
single l3mdev rule
      ↓
VRF device identity
      ↓
associated FIB table
```

This is a real simplification of policy-routing plumbing, not a new routing protocol. A direct adjacent-tag check finds no `FRA_L3MDEV` in v4.7 and finds it in v4.8.

## 8. iproute2 gains VRF support in stages

The userspace chronology also needs more precision than a single version number.

A public iproute2 RFC dated 2015-07-06 already proposed `ip link` support for creating a VRF device and setting its table binding. iproute2 4.3.0 release notes list David Ahern's `add support for VRF device` change. That is the device-management layer used by commands such as:

```text
ip link add vrf-blue type vrf table 10
```

Kernel VRF documentation separately notes later `vrf` keyword support in iproute2 4.7. That later convenience vocabulary should not be back-projected as the first appearance of all VRF userspace support.

So the safer chronology is:

```text
2015 public iproute2 VRF-device patch
        ↓
iproute2 4.3.0 includes VRF device support
        ↓
later first-class VRF convenience vocabulary expands
```

The operational interface becomes clearer without changing the fundamental routing-domain concept.

## 9. PBR can override VRF defaults

Linux VRF documentation explicitly says higher-priority policy-routing rules may take precedence over the VRF device rules.

This is crucial for genealogy:

```text
VRF does not replace RPDB
VRF consumes/integrates with RPDB
```

The RPDB remains an underlying selection engine.

## 10. Why modern systems combine all three

A containerized router or multi-tenant host might use:

```text
network namespace
   ↓ isolate device/stack/socket world
VRF
   ↓ split L3 routing domains within that namespace
RPDB rules
   ↓ override/select special traffic paths
multiple FIB tables
```

These are composable mechanisms from different historical layers.

## 11. Root-hunting lineage

```text
Linux 2.1/2.2 policy routing
RPDB + multiple FIB tables
        │
        ├───────────────┐
        ↓               │
network namespaces      │
2.6.24→2.6.29           │
stack isolation         │
        │               │
        └─ can contain ─┤
                        ↓
                     VRF device
                     Linux 4.3
                        ↓
               generalized into
                     l3mdev
                     Linux 4.4
                        ↓
              per-VRF iif/oif rules
                        ↓
                 Linux 4.8
              FRA_L3MDEV rule
```

Do not rewrite this as a false linear chain:

```text
RPDB → netns → VRF
```

They solve different scopes and coexist. The VRF→l3mdev relation is exceptional here because the contemporary patch series explicitly describes that generalization; the netns/VRF relationship does not have equivalent descent evidence.

## Evidence anchors

- exact VRF/l3mdev chronology: [`linux-vrf-l3mdev-mainline-chronology.md`](linux-vrf-l3mdev-mainline-chronology.md)
- `network_namespaces(7)`: https://man7.org/linux/man-pages/man7/network_namespaces.7.html
- `clone(2)` / `CLONE_NEWNET`: https://man7.org/linux/man-pages/man2/clone.2.html
- historical CLONE_NEWNET documentation discussion: https://lkml.iu.edu/0811.2/02085.html
- Linux VRF documentation: https://docs.kernel.org/networking/vrf.html
- older VRF documentation preserving 4.7/4.8 transition: https://kernel.org/doc/html/v5.12/networking/vrf.html
- initial VRF commit `193125db…`: https://github.com/torvalds/linux/commit/193125dbd8eb292d88feb201f030889b488b0a02
- initial l3mdev commit `1b69c6d0…`: https://github.com/torvalds/linux/commit/1b69c6d0ae90b7f1a4f61d5c8209d5cb7a55f849
- l3mdev FIB-rule commit `96c63fa7…`: https://github.com/torvalds/linux/commit/96c63fa7393d0a346acfe5a91e0c7d4c7782641b
- automatic rule-install commit `1aa6c4f6…`: https://github.com/torvalds/linux/commit/1aa6c4f6b8cd84b8b36ebf43c6861ca87eab4da0
- 2015 iproute2 VRF RFC: https://www.spinics.net/lists/netdev/msg334796.html
- iproute2 4.3.0 release summary: https://lwn.net/Articles/662996/
- `ip-netns(8)`: https://man7.org/linux/man-pages/man8/ip-netns.8.html
- Linux 2.1.68 `rtnetlink.h`: https://www.nic.funet.fi/pub/Linux/kernel/v2.1/patch-html/patch-2.1.68/linux_include_linux_rtnetlink.h.html

Research and initial drafting: **GPT-5.6 Sol (OpenAI), August 2026**. Exact VRF/l3mdev chronology updated 2026-09-15.
