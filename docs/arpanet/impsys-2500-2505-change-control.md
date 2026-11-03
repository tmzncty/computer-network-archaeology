# IMPSYS 2500 → 2505: interface assumptions and change control in 1971

## Scope

This note reconstructs one narrow operational episode in the early ARPANET: the June–August 1971 transition around IMP system versions 2500 and 2505, and what it reveals about Host–IMP interface contracts, undocumented assumptions, software deployment, and the emerging Network Control Center (NCC).

It does **not** attempt to reconstruct the complete IMP software release genealogy or every change between versions 2500 and 2505.

## Why this is a real coverage gap

The repository already documents the 1822 physical interface, later ready-line clarification, and the January 1972 distinction between Report 1822 documentation errors and IMPSYS 2513/2514 timing changes. What was still missing was the earlier operational episode in which a network-wide IMP software change exposed host software assumptions that BBN did not regard as part of the advertised interface.

That episode is unusually valuable because the contemporary documents describe not just a protocol rule, but **how a live packet network learned to manage implementation changes**.

## Primary-source sequence

### 1. 25 June 1971 — IMPSYS 2500 changes Host-up behavior

Bernie Cosell of BBN records in RFC 209 (13 August 1971) that BBN put **IMP system Version 2500** into the network on **25 June 1971**.

The release corrected a problem in which Hosts could receive spurious `Destination Dead` (Type 7) messages. The fix made an IMP refuse messages from its Host for about **30 seconds after the Host indicated that it intended to come alive**.

This is a concrete implementation/deployment fact, not merely a proposal: RFC 209 says the new version was put up in the network on that date.

### 2. The change broke NCPs that depended on an undocumented timing assumption

RFC 209 says a number of NCPs imposed an upper bound on how long an IMP could take to accept a message. When the new approximately 30-second delay exceeded that locally assumed bound, those NCPs declared the IMP inoperative and shut themselves down.

The historical significance is not simply “a timeout bug.” The failure crossed an administrative and implementation boundary:

- BBN believed Version 2500 changed **no advertised property** of the Host–IMP interface;
- some Host implementations had nevertheless inferred stronger timing behavior from experience;
- the live network therefore contained dependencies that were real operationally but absent from the written contract.

RFC 209 explicitly says BBN wanted future Hosts to assume that anything not guaranteed by Report 1822 did not exist, and to report problems rather than code around observed IMP behavior.

This is strong contemporary evidence for an early form of **specification-first interoperability discipline**.

### 3. Report 1822 was acknowledged to be incomplete

RFC 209 is unusually candid: while asking the community to treat BBN Report 1822 as complete and correct, BBN states that it understood the report was actually **neither**.

The proposed remedy was institutional as much as technical: discrepancies should be escalated to the NCC/BBN so that either the IMP system or Report 1822 could be fixed.

Therefore the safe historical claim is not that 1822 already formed a perfect stable standard. Rather, BBN was trying to make the written specification the normative boundary precisely because implementation-derived assumptions had caused failures.

### 4. 16–20 August 1971 — IMPSYS 2505 and explicit change notification

RFC 213, dated 20 August 1971, says BBN installed **Version 2505 during the week of 16 August**.

It identifies three principal changes:

1. supported Hosts per IMP increased from **three to four**;
2. Host-handling routines gathered more accurate and more extensive usage statistics and reported them to the NCC;
3. the 10-second Host `round trip` statistic changed its time unit from **100 microseconds to 800 microseconds**.

The first item is especially useful hardware/operations evidence: despite a substantial internal IMP change, BBN identified the external effects as a new **status light 8 for Host 4** plus longer 10-second and snapshot statistics. RFC 213 says no direct Host effect was anticipated.

This provides a firm lower bound: four-Host support was installed in the network by the week of 16 August 1971 according to BBN's own change notice. It does not prove that every physical IMP chassis already had every possible Host interface populated.

### 5. September 1971 — monitoring becomes more centralized at the NCC

RFC 218 (8 September 1971) documents a further change to IMP status reporting intended to expand BBN's NCC role.

It says textual status reports were to be removed because a **binary version sent directly to the NCC** had already superseded them. It also says the status reports remaining with the statistics program on **fake host 3** would no longer be alterable by `PARAMETER CHANGE` parameters, specifically to prevent Hosts from inadvertently interfering with NCC operation.

This is direct evidence of an operational architecture in which monitoring/control responsibility was being centralized and insulated from ordinary Host-side parameter changes.

It does not establish the complete NCC architecture, staffing model, or all telemetry formats.

## Reconstructed operational sequence

```text
25 Jun 1971
IMPSYS 2500 deployed
    |
    | fixes spurious Destination Dead behavior
    | introduces ~30 s post-Host-up acceptance delay
    v
some NCPs fail because they assumed an undocumented shorter bound
    |
    v
BBN: treat Report 1822 as normative; report discrepancies to NCC
    |
    v
week of 16 Aug 1971
IMPSYS 2505 installed
    | four-Host support + richer NCC statistics
    v
Sep 1971
status reporting further centralized/insulated at NCC
```

The arrows above are chronological/operational transitions documented by BBN. They are **not** claims that the Version 2500 incident caused every later NCC or 2505 design change.

## Evidence table

| Claim | Source | Locator | Certainty |
|---|---|---|---|
| IMPSYS 2500 was put into the network on 25 June 1971 | RFC 209 | opening paragraph | high |
| Version 2500 imposed about a 30-second post-Host-up refusal interval | RFC 209 | opening paragraph | high |
| multiple NCPs failed because of locally imposed acceptance-time limits | RFC 209 | opening paragraph | high |
| BBN regarded the affected timing assumption as not advertised | RFC 209 | second paragraph | high |
| BBN asked Hosts to rely only on properties guaranteed by Report 1822 | RFC 209 | second paragraph | high |
| BBN acknowledged Report 1822 was not actually complete/correct | RFC 209 | second paragraph | high |
| IMPSYS 2505 was installed during week of 16 August 1971 | RFC 213 | opening paragraph | high |
| 2505 raised supported Hosts from 3 to 4 | RFC 213 | item 1 | high |
| 2505 increased Host-use statistics reported to NCC | RFC 213 | item 2 | high |
| Host round-trip statistic unit changed 100 µs → 800 µs | RFC 213 | item 3 | high |
| binary IMP status reporting to NCC had superseded text reporting by September | RFC 218 | first/second paragraphs | high |
| remaining fake-host-3 status reporting was insulated from Host parameter changes | RFC 218 | final paragraph | high |

## Lineage / relation assessment

Candidate relations, if the repository later models software revisions and operational practices explicitly:

- `IMPSYS-2505 successor-version-of IMPSYS-2500` — **medium certainty**. The version numbers and deployment chronology support succession in the IMP software line, but the three RFCs do not enumerate all intervening builds or state that 2505 directly derives from 2500.
- `IMPSYS-2500 implements Host-IMP-interface` — **high certainty** in context, but the precise Report 1822 edition in force on 25 June should be recovered before attaching a revision-specific edge.
- `IMPSYS-2505 reports-statistics-to NCC` — **high certainty**, explicit in RFC 213.
- `IMP-status-binary-reporting feeds NCC` — **high certainty**, explicit in RFC 218.
- `Version-2500 incident caused NCC centralization` — **not established** and should not be encoded.

No new causal lineage edge is created merely because the documents occur in sequence.

## What this evidence explicitly does not prove

1. It does not provide a complete IMPSYS 2500→2505 commit/release history or show that there were no intervening versions.
2. It does not prove the exact Report 1822 revision deployed at every site on 25 June 1971.
3. It does not identify which NCP implementations/sites failed under the Version 2500 timing change.
4. It does not prove that every IMP had four physically populated Host ports immediately after Version 2505 was installed; it establishes system support for four Hosts.
5. It does not prove that the June incident caused the August 2505 changes or the September NCC reporting changes.
6. It does not reconstruct the binary status-report format or the complete meaning of fake host 3.
7. It does not show that BBN's desired specification discipline was immediately obeyed by every Host implementor.

## Sources

- Bernie Cosell (BBN), RFC 209, *Host/IMP Interface Documentation*, 13 August 1971. https://www.rfc-editor.org/rfc/rfc209.html
- Bernie Cosell (BBN), RFC 213, *IMP System Change Notification*, 20 August 1971. https://www.rfc-editor.org/rfc/rfc213.html
- Bernie Cosell (BBN), RFC 218, *Changing the IMP Status Reporting Facility*, 8 September 1971. https://www.rfc-editor.org/rfc/rfc218.html

These are contemporary Network Working Group records authored at BBN during the operational period discussed. Later summaries are not needed for the core claims above.

Research and drafting: **OpenAI, 3 November 2026**.
