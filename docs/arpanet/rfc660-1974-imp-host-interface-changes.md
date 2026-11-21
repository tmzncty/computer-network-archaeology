# October 1974 proposed IMP/Host interface changes (RFC 660)

## Object and status

**Object:** BBN-NET IMP software and the Host–IMP interface described in BBN Report 1822, as modified by the **planned** changes announced by D. Walden in RFC 660, *Some Changes to the IMP and the IMP/Host Interface* (October 1974). The RFC says the changes **will** be made “in the next few weeks”; it is a contemporary change notice, **not** evidence of a particular deployment date, installed IMPSYS version, or site acceptance.

Primary source: [RFC 660](https://www.rfc-editor.org/rfc/rfc660.html), pp. 1–2 (NIC 31202). The repository's earlier 1971 IMPSYS 2500/2505 work covers different behavior and should not be collapsed into this change.

## Four separately stated changes

1. **Message-number scope and resource allocation** (p. 1, section a): Walden says that since 1972 there had been **four outstanding messages between any pair of IMPs**, shared across all Host pairs attached to those IMPs. This could make one Host pair interfere with another. The planned change assigns a separate message-number sequence to each **Host pair**. These sequences are allocated dynamically from a limited pool; exhaustion is described as causing time multiplexing and reduced speed, not preventing Host communication. This is an explicit before/after property comparison, not a guess from dates.
2. **Administrative Host-pair access control** (p. 1, section b): described as being added **on ARPA instructions**. Permission bits in the IMP are checked when Host pairs resume communication after approximately two minutes of inactivity. Denial returns **Destination Dead, sub-code 3**; the initial default is to allow all Host pairs. The RFC does not document an actual denial event or the subsequent policy configuration.
3. **Outstanding-message window** (p. 2, section c): after separating Host-pair sequences, the window is planned to grow from **four to eight per Host pair**, which Walden says can improve throughput in some cases. This is not a measured throughput result or evidence of universal doubling.
4. **Special type-3 single-packet path** (p. 2, section d): source Host messages of new **type 3** bypass normal ordered/error-controlled message sequencing and enter IMP store-and-forward; multipacket type-3 messages are discarded. At the destination IMP, the packet bypasses reassembly and reaches the Host output queue as type 3. Packets may arrive out of order, be dropped for insufficient resources, and receive **no source-to-destination retransmission, reassembly, RFNM or incomplete-transmission notices**. NCC is to regulate which Hosts can use the mechanism because unrestricted use could degrade service for others.

Walden characterizes the changes as backward-compatible, subject to possible minor timing exceptions (p. 1). He asks readers to file RFC 660 with their copy of **BBN Report 1822 until it is updated** (p. 2). This explicitly makes the RFC an interim interface amendment, not proof that a revised edition of Report 1822 had already been issued.

## Evidence-bearing relationships

| Proposed relation | Certainty | Basis | What it does **not** establish |
| --- | --- | --- | --- |
| RFC 660 **announces amendments to** the Host–IMP interface in BBN Report 1822 | **high** | RFC 660 p. 1 opening; p. 2 closing | Not a dated 1822 revision or proof of rollout |
| IMP message-number accounting **planned change from** IMP-pair shared window **to** Host-pair sequence and eight outstanding messages | **high (proposal)** | RFC 660 pp. 1–2, a/c | Not a specific software build or measured throughput |
| IMP Host-pair permission checks **requested by** ARPA | **high (reported instruction)** | RFC 660 p. 1, b | Not evidence that any particular Host was blocked |
| IMP/Host type-3 special message path **planned alongside** normal ordered/RFNM path | **high (proposal)** | RFC 660 p. 2, d | Not evidence of deployed datagram services or ancestry of IP/UDP |

No `derived-from`, `influenced`, or `replaced-by` edge is justified here. In particular, the type-3 facility resembles later unreliable packet service in *behavior* but RFC 660 alone does not document influence on any later protocol.

## Open archival questions

- Find an actual BBN IMPSYS release notice, Report 1822 edition, source listing, or NCC change log verifying which of the four planned changes shipped, and on what date.
- Recover the exact bit-level encoding of the new Host–IMP type 3 and Destination Dead sub-code 3 in the appropriate 1822 revision.
- Find evidence of authorized Host deployments, experiments, or administrative access denials; do not infer them from the notice.
- Compare the 1972 four-message IMP-pair statement against contemporaneous BBN documentation before assigning a precise first-release date.

## Source locator

D. Walden (BBN-NET), *Some Changes to the IMP and the IMP/Host Interface*, RFC 660, NIC 31202, October 1974, [RFC Editor transcription](https://www.rfc-editor.org/rfc/rfc660.html), p. 1 sections a–b and p. 2 sections c–d and closing note.
