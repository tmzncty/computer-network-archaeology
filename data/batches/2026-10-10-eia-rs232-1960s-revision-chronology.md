# Batch: EIA RS-232 1960s revision chronology — 2026-10-10

## Research question

What revision sequence for EIA RS-232 can be supported without importing later folklore about connectors and electrical deltas into the 1960s editions?

## Existing gap

`ROADMAP.md` still lists **EIA RS-232 revisions** as uncovered under 1960s terminals and access. Repository search before this batch found no RS-232-specific research narrative.

## Narrative excavation

- `docs/interfaces/eia-rs232-1960s-revision-chronology.md`

## Sources

### S1 — National Bureau of Standards standards survey

*Interface Standards for Automated Coal Mining Equipment*, RS-232-C entry, p. 17 in the GovInfo PDF.

URL: https://www.govinfo.gov/content/pkg/GOVPUB-C13-eb9a42c57ad9d661ec3bb231207d0919/pdf/GOVPUB-C13-eb9a42c57ad9d661ec3bb231207d0919.pdf

Specific evidence:

- identifies EIA RS 232-C as August 1969;
- gives the title *Interface Between Data Terminal Equipment and Data Communication Equipment Employing Serial Binary Data Interchange*;
- names EIA Subcommittee TR-30.2 as maintenance authority;
- lists RS 232 (May 1960), RS 232-A (October 1963), RS 232-B (October 1965), and RS 232-C (August 1969);
- summarizes the four-part scope of RS-232-C;
- reports commercial acceptance and contemporary relationships to V.24/V.28/V.31 and RS-422/423.

Evidence strength: **high** for revision dates, 1969 title/scope, maintenance authority, and what the NBS survey reported about implementation status; **not sufficient** for clause-by-clause deltas among A/B/C.

### S2 — Electronics, 14 September 1978

World Radio History scan:
https://www.worldradiohistory.com/Archive-Electronics/70s/78/Electronics-1978-09-14.pdf

Specific evidence: describes RS-232-C as the most widely used DTE/DCE interface and characterizes the intended envelope as less than 50 feet and below 20 kilobaud.

Evidence strength: **medium-high** for late-1970s engineering practice; **low/none** for 1960s first deployment chronology.

## Newly recovered facts

1. A defensible 1960s standards-document spine is: May 1960 RS-232 → October 1963 RS-232-A → October 1965 RS-232-B → August 1969 RS-232-C.
2. The 1969 edition's scope explicitly spans electrical, mechanical, circuit-functional, and selected system-configuration interface characteristics.
3. EIA Subcommittee TR-30.2 is identified by the NBS survey as maintenance authority for RS-232-C.
4. A late-1970s government standards survey and contemporary trade literature both describe RS-232-C as commercially widespread, but neither establishes immediate adoption at the 1969 publication date.
5. Contemporary sources distinguish RS-232-C from the newer RS-422/423 electrical-interface family and from CCITT V.24/V.28/V.31; equivalence or ancestry should not be inferred solely from functional overlap.

## Lineage decision

The edition sequence supports **high-certainty document-revision edges** if the repository vocabulary contains a narrowly defined `revision-of`/`supersedes` relation:

- RS-232-A → RS-232;
- RS-232-B → RS-232-A;
- RS-232-C → RS-232-B.

No generic `derived-from` edge should be created merely to encode this chronology. No RS-232-C → RS-422/423 causal edge is justified by the current evidence: the NBS survey records expected replacement, not technological descent.

## Explicit negative claims

This batch does **not** prove:

- the technical clause deltas among the 1960, 1963, 1965, and 1969 texts;
- any specific connector becoming mandatory in a specific edition;
- a particular voltage/capacitance change without the edition text;
- first vendor implementation or first operational deployment;
- 1969 publication immediately causing commercial ubiquity;
- that RS-232 defines character coding, asynchronous framing, or modem modulation;
- that RS-422/423 actually displaced RS-232-C as predicted;
- causation from publication order.

## Remaining work

- recover the original EIA RS-232, RS-232-A, and RS-232-B texts or authoritative catalog scans;
- compare electrical limits and interchange-circuit tables clause by clause;
- recover contemporary modem/terminal manuals that cite a specific edition rather than generic “RS-232” compatibility;
- only then decide whether structured artifact records and revision edges can be added without flattening revision-specific behavior.

Research and drafting: **OpenAI, 10 October 2026**.
