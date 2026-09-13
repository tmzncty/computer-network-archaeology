# BBN Report 1822 correction vs. IMPSYS 2514 timing change — January 1972

## Scope

This excavation resolves one narrow revision problem in the Host–IMP record: **why do January 1972 sources appear to say both that a 40-second timeout was an erroneous Report 1822 value and that IMPSYS 2513 really did use a delay of slightly over 40 seconds?**

The answer is that the sources discuss **two different, unsynchronized timing conditions**.

This note does not reconstruct every BBN Report 1822 revision, every IMP software release, or the exact cutover time at every ARPANET site.

## Primary-source sequence

### 1. RFC 270 — 1 January 1972: a Report 1822 documentation correction

RFC 270 was issued by A. McKenzie of BBN after errors were found in BBN Report 1822 (NIC 7958) while RFC 271 was being prepared.

It instructs readers to replace page 25 and delete the first two lines of page 26. The corrected text changes two points under the stated Host–IMP conditions:

- the Host is **not** marked dead;
- the timeout is **30 seconds, not 40 seconds**.

Most importantly for revision archaeology, RFC 270 explicitly says these are errors in previous versions of Report 1822, **not changes to the IMP system**. It states that the relevant timeout had always been 30 seconds and that the Host had never been marked dead under those conditions.

This is therefore evidence about **document/version drift** between Report 1822 text and the implemented interface behavior. It is not evidence that every timer inside the IMP was always 30 seconds.

### 2. RFC 271 — 3 January 1972: a real IMPSYS 2513 → 2514 implementation change

Two days later, Bernard Cosell's RFC 271 announced IMPSYS version 2514 and scheduled field installation for **13 January 1972 between noon and 1 PM EST**.

The document identifies two problems in version 2513, both involving the delay after a Host comes up and before its IMP will accept the **second packet from that Host**:

1. the delay had been lengthened to slightly over 40 seconds;
2. an ambiguity could extend it to roughly 75 seconds.

For 2514, the delay was backed down to 30 seconds, as in IMP systems before 2513, and the ambiguity was removed.

This is a genuine implementation-version change. But it is **not the same timer** corrected in RFC 270.

### 3. RFC 271's footnote separates the timers explicitly

RFC 271 itself provides the decisive reconciliation.

During the Host-up waiting period, the Host must already be able to accept traffic from the network. If a message remains on the Host's output queue for 30 seconds without being taken, the IMP may drop its Ready line for one quarter second to clear the interface. RFC 271 cites RFC 270 for this behavior.

It then states that the timeout periods for:

- the **Host queue**, and
- the **delay when the Host comes alive**

are **not synchronized**.

Thus the two January sources are compatible:

| Timing condition | Direction / condition | January 1972 evidence | Historical conclusion |
|---|---|---|---|
| Host output-queue/interface-clearing timeout | IMP has a message queued for the Host and the Host does not take it | RFC 270; RFC 271 footnote | Report 1822's 40-second/dead-Host wording was erroneous; relevant implemented timeout was 30 seconds |
| Host-up second-packet acceptance delay | Host has just come alive; IMP limits acceptance from Host | RFC 271 | IMPSYS 2513 really used slightly over 40 seconds and could reach about 75 seconds; 2514 restored 30 seconds and removed ambiguity |

The asymmetry also matters operationally: while the IMP temporarily limits how much it accepts **from** the newly alive Host, the Host is expected to accept network traffic **to** it immediately.

## Deployment clock: scheduled date vs. confirmed operational lower bound

RFC 271 gives **13 January 1972** as the planned field-installation date for IMPSYS 2514. A schedule is not automatically a completed-deployment fact.

RFC 331, dated **19 April 1972**, supplies a later contemporary lower bound. While announcing the planned experimental IMPSYS 2600 cutover, BBN-NET says that if problems occurred, the **current system, IMPSYS 2514**, would be reloaded.

Therefore the safe deployment statement is:

> IMPSYS 2514 was scheduled for network-wide field installation on 13 January 1972, and contemporary BBN evidence confirms that it was the current IMP system by 19 April 1972.

The surviving evidence used here does **not** prove that every IMP site completed the 2514 cutover successfully during the one-hour window on 13 January.

RFC 331 also documents the operational style of later IMP software transitions: site personnel were asked to load a mailed IMPLOD tape during a coordinated cutover window. That is useful operational context, but it should not be projected backward as proof that every detail of the 2514 rollout was identical.

## Evidence table

| Claim | Primary evidence | Locator | Certainty |
|---|---|---|---|
| Report 1822 page 25/26 contained a 40-second/dead-Host error | RFC 270 | opening paragraph | confirmed |
| RFC 270 describes a documentation correction, not an IMP-system change | RFC 270 | second paragraph | confirmed |
| IMPSYS 2513 had a separate Host-up delay slightly over 40 seconds, with ambiguity to about 75 seconds | RFC 271 | page 1, version-2513 problem description | confirmed |
| IMPSYS 2514 restored that Host-up delay to 30 seconds and removed the ambiguity | RFC 271 | page 1 | confirmed |
| Host queue timeout and Host-up delay are distinct and unsynchronized | RFC 271 | page 2 footnote | confirmed |
| A Host must accept network traffic immediately while coming alive | RFC 271 | page 2 Host-alive summary | confirmed |
| 13 January 1972 is a scheduled 2514 field-installation date | RFC 271 | opening paragraph | confirmed as schedule only |
| IMPSYS 2514 was operational/current by 19 April 1972 | RFC 331 | opening paragraph | confirmed lower bound |

## Lineage decision

**No `LIN-*` edge is created.**

The evidence shows:

- a correction to one version of BBN Report 1822;
- an adjacent IMP software release change;
- an explicit cross-reference between the relevant interface behaviors.

It does **not** establish a descent, successor, influence, or causal lineage relation between two distinct artifacts merely because RFC 270 and RFC 271 were written together and published two days apart. The correct representation here is claim-level source evidence attached to the existing Host–IMP interface (`ART-0008`) and IMP (`ART-0006`) records.

## What this evidence does **not** prove

1. It does not prove that every timer in the IMP was 30 seconds before January 1972.
2. It does not prove that the RFC 270 queue timeout and the RFC 271 Host-up delay were the same mechanism; RFC 271 explicitly says the two timing periods are not synchronized.
3. It does not prove the exact installation time of IMPSYS 2514 at every ARPANET site.
4. It does not prove that the 13 January 1972 scheduled rollout completed without delay or rollback.
5. It does not reconstruct a complete 1969→1976 BBN Report 1822 revision genealogy.
6. It does not establish that a Report 1822 textual error caused the IMPSYS 2513 timing behavior, or vice versa.
7. It does not justify deriving one artifact from another solely from chronological adjacency.

## Structured records

- `SRC-0277` — RFC 270, Report 1822 correction notice.
- `SRC-0278` — RFC 271, IMPSYS 2514 field-change notification and timer distinction.
- `SRC-0279` — RFC 331, contemporary confirmation that IMPSYS 2514 was the current system by 19 April 1972.

These records deliberately use existing artifact IDs `ART-0008` and `ART-0006`; this batch does not mint a new artifact or lineage edge for what is fundamentally revision-specific evidence about already cataloged objects.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
