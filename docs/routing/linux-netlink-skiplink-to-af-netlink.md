# Linux Netlink before `AF_NETLINK`: SKIPLINK, `nlmsghdr`, and the 2.1.68 socket-family transition

This note resolves a narrow provenance gap in the Linux kernel/user-space networking-control history: **what existed before the familiar `AF_NETLINK` socket API, and where does the socket-family form first appear in a public kernel release?**

It deliberately does not treat all things called “Netlink” as one unchanged interface.

## 1. The earliest recovered release is Linux 1.3.31, not 2.1.15

The kernel.org archive dates Linux 1.3.31 to **1995-10-04**. The immediately preceding 1.3.30 archive is dated 1995-09-27.

A release-snapshot history reconstructed from those old source trees gives a useful adjacent comparison:

- Linux 1.3.30 snapshot: no `net/netlink.c`;
- Linux 1.3.31 snapshot: `net/netlink.c` and `include/net/netlink.h` appear.

The 1.3.31 source identifies itself as:

> `SKIPLINK` — a loadable kernel-mode driver providing multiple kernel/user-space bidirectional communication links.

It names **Alan Cox** as author. The implementation is visibly a **character-device interface**, not a socket family: it installs `file_operations`, registers `NET_MAJOR` as `"netlink"`, and exports routines including `netlink_attach`, `netlink_detach`, and `netlink_post` for kernel clients.

Primary anchors:

- kernel.org v1.3 archive: <https://www.kernel.org/pub/linux/kernel/v1.3/>
- reconstructed 1.3.31 source: <https://github.com/tbodt/linux-history/blob/89eabf146605aaef62d9b8714a4128f300467858/net/netlink.c>
- reconstructed 1.3.30→1.3.31 comparison: <https://github.com/tbodt/linux-history/compare/88d15e9d250c95e23194c29888d5ca4f86e37581...89eabf146605aaef62d9b8714a4128f300467858>

### What this proves

It establishes Linux **1.3.31 as the earliest recovered public release boundary in this repository for the Netlink/SKIPLINK kernel-user mechanism**.

### What it does not prove

It does not prove that 1.3.31 was Alan Cox's first private prototype, first mailing-list posting, or first external patch. Those pre-release provenance questions remain open.

## 2. Linux 2.1.15 is a transitional message-layer milestone, not the birth of the socket family

By Linux **2.1.15** the file heading has changed from `SKIPLINK` to `NETLINK`, but the transport is still recognizably the character-device design. It still registers the netlink major device and exposes the old attachment/posting model.

What is new is a higher-level message facility associated in comments with **ANK (Alexey N. Kuznetsov)**. The source describes features including:

- a standard message format;
- loss/overrun detection intended to permit user space to recover by rereading state such as the FIB and device list;
- batching;
- avoiding work when no user process is attached.

That is the important 2.1.15 milestone: the old device transport is being equipped with the message semantics that make later rtnetlink-style state exchange recognizable.

Primary anchor:

- reconstructed Linux 2.1.15 `net/netlink.c`: <https://github.com/tbodt/linux-history/blob/12980ed0feabd39dc13753d9a11a4673dda84ba1/net/netlink.c>

The safe chronology is therefore:

```text
Linux 1.3.31
SKIPLINK / netlink character device
        ↓
Linux 2.1.15
same device-oriented transport + higher-level nlmsg message machinery
        ↓
Linux 2.1.68
AF_NETLINK socket family + rtnetlink object/message model
```

This is stronger than saying “Netlink started in 2.1.15,” and more precise than projecting the modern socket API backward into 1995.

## 3. `AF_NETLINK` appears at the Linux 2.1.68 public-release boundary

The official kernel archive dates:

- Linux 2.1.67: **1997-11-29 19:18**;
- Linux 2.1.68: **1997-11-30 23:15**.

The adjacent source trees show a sharp API boundary.

### Linux 2.1.67

`include/linux/socket.h` has no `AF_NETLINK`/`PF_NETLINK` definitions. Netlink is still outside the normal socket-family namespace.

Source:

- <https://github.com/tbodt/linux-history/blob/c5a4ebcd4431e607667b63c173d5918b518fe3b2/include/linux/socket.h>

### Linux 2.1.68

The final 2.1.68 source adds:

```c
#define AF_NETLINK  16
#define AF_ROUTE    AF_NETLINK /* Alias to emulate 4.4BSD */
#define PF_NETLINK  AF_NETLINK
#define PF_ROUTE    AF_ROUTE
```

and restructures Netlink into a directory containing a socket implementation. `net/netlink/af_netlink.c`:

- accepts `SOCK_RAW` and `SOCK_DGRAM`;
- allocates sockets with `sk_alloc(AF_NETLINK, ...)`;
- binds/connects using `sockaddr_nl` and `AF_NETLINK`;
- names both Alan Cox and Alexey Kuznetsov as authors;
- retains optional `CONFIG_NETLINK_DEV` compatibility through `NL_EMULATE_DEV`.

The 2.1.67→2.1.68 source transition also introduces the rtnetlink interface as a first-class object/message API (`RTM_NEWLINK`, `RTM_NEWADDR`, `RTM_NEWROUTE`, `RTM_NEWNEIGH`, `RTM_NEWRULE`, multicast groups, attributes, and related structures).

Primary anchors:

- kernel.org v2.1 archive: <https://www.kernel.org/pub/linux/kernel/v2.1/>
- Linux 2.1.68 socket implementation: <https://github.com/tbodt/linux-history/blob/7f563ad63270d13b8412eb7c89d7b7b44f40d0e1/net/netlink/af_netlink.c>

The correct claim is therefore:

> **Linux 2.1.68 is the first adjacent public release recovered here with the `AF_NETLINK` socket family and the new rtnetlink object/message model.**

The old character-device API did not disappear atomically; 2.1.68 carries an explicit device-emulation compatibility path.

## 4. Why there is no honest “1997 merge commit” to cite

The repository's prior worklist asked for an “exact first `AF_NETLINK` socket-family merge commit.” That wording is anachronistic for this period.

Linux 2.1.68 predates Git by years. Repositories such as `tbodt/linux-history` reconstruct old tarball/patch releases as later Git imports. A SHA such as the reconstructed `Import 2.1.68` object is useful for reproducible tree comparison, but it is **not a contemporaneous 1997 integration commit** and must not be presented as one.

For this era, the strongest current boundary is:

1. the official dated kernel tarball/patch archive;
2. adjacent release-tree comparison;
3. surviving contemporary patch/mail artifacts where available.

Recovering the original patch submission or maintainer correspondence remains a separate provenance task.

## 5. Participant attribution supports a real evolution relation

RFC 3549 (July 2003), coauthored by Alexey Kuznetsov, gives unusually direct historical attribution in its acknowledgements: it credits Kuznetsov with extending Netlink to the IP-service delivery model and identifies Alan Cox as the author of the original Netlink character device.

Primary anchor:

- RFC 3549, section 6: <https://www.rfc-editor.org/rfc/rfc3549.html#section-6>

This is stronger evidence than mere chronology for a relation between the two generations.

A candidate lineage statement can therefore be retained with **high certainty**:

```text
Alan Cox Netlink/SKIPLINK character-device mechanism
        ↓ explicit documented extension/generalization
Kuznetsov-era Netlink IP-service / AF_NETLINK+rtnetlink model
```

No structured `LIN-*` edge is minted here because the existing relation vocabulary should first be checked for a term such as `generalized-into` or `extended-into`; encoding this as `successor-of` or `derived-from` would be stronger than the evidence warrants.

## 6. PF_ROUTE comparison: compatibility and conceptual borrowing are not code ancestry

Linux 2.1.68 defines `AF_ROUTE` as an alias of `AF_NETLINK` with the comment `Alias to emulate 4.4BSD`. RFC 3549 also discusses BSD 4.4 routing sockets as an earlier control/forwarding separation model.

These are meaningful historical connections, but they do **not** establish that Linux Netlink is a source-code descendant of BSD PF_ROUTE. The repository should continue to model BSD PF_ROUTE and Linux Netlink/rtnetlink as distinct implementations with overlapping control-plane roles unless stronger direct design/code provenance is found.

## 7. Evidence boundary

This excavation proves, with high confidence:

1. **1995-10-04 / Linux 1.3.31** — earliest recovered released SKIPLINK/Netlink character-device implementation; Alan Cox attribution is in the source.
2. **Linux 2.1.15** — device-oriented Netlink remains, but high-level `nlmsg` message machinery is now present.
3. **1997-11-30 / Linux 2.1.68** — first adjacent public release recovered with `AF_NETLINK`, `PF_NETLINK`, socket operations, and rtnetlink's structured network-object message family.
4. **Compatibility continuity** — 2.1.68 still contains device-emulation support, so the transition is not an instantaneous deletion of the old interface.
5. **Documented historical relation** — RFC 3549 explicitly attributes the original character device to Cox and the IP-service extension to Kuznetsov.

It does **not** prove:

- the date or content of Alan Cox's first private/pre-release SKIPLINK patch;
- the exact mailing-list submission that entered Linux 1.3.31;
- a contemporaneous Git “merge commit” for 2.1.68;
- that PF_ROUTE caused Netlink or that Netlink copied PF_ROUTE code;
- that inclusion in a kernel tarball proves actual production deployment;
- that every modern Netlink semantic was already present in 1.3.31, 2.1.15, or 2.1.68.

## Follow-up targets

- recover the pre-1.3.31 Alan Cox patch/mail thread, if preserved;
- locate contemporary 2.1.68 integration discussion or patch announcement and attribute individual subpatches;
- map 2.1.68 `NETLINK_ROUTE`/rtnetlink message fields into the earliest iproute user-space snapshots;
- preserve the temporary character-device emulation lifetime and the release in which it finally disappears.

Research update: **GPT-5.6 Sol (OpenAI), September 2026**.
