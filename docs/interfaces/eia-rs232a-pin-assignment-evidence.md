# EIA RS-232-A pin-assignment evidence from IBM field documentation

## Question

The repository already has the 1960/1963-A/1965-B/1969-C chronology, the October 1965 RS-232-B text, and a May 1964 Bell implementation of RS-232-A. One boundary remained deliberately unresolved: whether the familiar 1–25 circuit-position assignment can be attributed to RS-232-A itself rather than merely to Bell's implementation.

The October 1963 EIA pamphlet is still not recovered here. This note therefore uses independent, near-contemporary IBM field-engineering documentation to narrow that claim without pretending that a vendor manual is the missing normative text.

## Evidence

### IBM, March 1969: explicit attribution to RS-232-A

IBM's *Teleprocessing General — Field Engineering Handbook* (Y27-0042-1, March 1969), chapter 2, describes the data-set interface as the demarcation between common-carrier equipment and the business machine. It says that before 1963 business machines and data sets did not necessarily use the same interface pin for a given signal, requiring system-specific cables.

It then states that the **RS-232-A EIA Standard Interface was agreed upon in 1963** and introduces a table as the **pin assignments set forth in the RS-232-A EIA Standard**.

Surviving scan:
https://www.bitsavers.org/pdf/ibm/datacomm/Y27-0042-1_Teleprocessing-General_FE_Handbook_Mar69.pdf

This is independent of the Bell 202C/202D manual already in the repository. It supports the narrower historical statement that IBM understood the standardized circuit-to-position mapping to be a property of RS-232-A, not merely a Bell-specific wiring convention.

### IBM, March 1966: the standard was an active engineering reference

IBM's *Common Carrier Facilities for Teleprocessing* field-engineering education manual (Z25-2529-0, March 1966) lists **EIA Standard RS-232-A** as a source, describes it as covering the interface between data-processing terminal equipment and data-communication equipment, gives the EIA Engineering Department as publisher/contact, and lists its price as $0.90.

Surviving scan:
https://archive.decromancer.ca/bitsavers.org/pdf/ibm/datacomm/Z25-2529-0_Common_Carrier_Facilites_For_Teleprocessing_Mar66.pdf

This does not reproduce the standard, but it shows that RS-232-A was a concrete, separately obtainable engineering document in IBM's training/source ecosystem by March 1966 rather than a retrospective label applied later.

## Relationship to the Bell 202C/202D evidence

The repository's May 1964 Bell specification shows a real implementation using positions 1–25 and RS-232-A circuit designations, plus a specific Cinch/Cannon D-subminiature-family connector.

The 1969 IBM handbook adds a different kind of evidence: it explicitly attributes the **pin assignments themselves** to RS-232-A. Together, the sources justify separating two claims:

1. **Circuit-to-position assignment:** supported as an RS-232-A standard property by IBM's explicit 1969 attribution — **high confidence**, though still awaiting the EIA pamphlet for clause-level confirmation.
2. **Exact connector shell/hardware:** Bell's May 1964 use of Cinch/Cannon DB-19604-432/433 is an implementation fact; these sources still do **not** prove that RS-232-A normatively required that exact shell — **unresolved**.

This distinction also fits the recovered RS-232-B text, which assigns positions 1–25 while stating that specification of a 25-pin connector was left for a future revision. Numbered contact assignments and normative mechanical connector specification are therefore not interchangeable claims.

## Lineage / relation assessment

No new machine-readable lineage edge should be minted from chronology alone.

Safe relations and certainty:

- `RS-232-A standardizes circuit-to-position assignments used by later conforming interfaces` — **high confidence as a property claim**, based on IBM's explicit attribution plus the Bell implementation.
- `Bell 202C/202D implements RS-232-A circuit assignment` — **high confidence**, already supported by the May 1964 Bell source.
- `RS-232-A requires Cinch/Cannon DB-19604-432/433` — **not established**.
- `RS-232-A caused Bell to choose the D-subminiature shell` — **not established**.

If the repository later adds a relation vocabulary for standards conformance, the Bell products can use `implements-interface` / `conforms-to`; `derived-from` remains too strong and semantically misleading.

## What this evidence explicitly does not prove

It does **not** prove:

- the complete October 1963 RS-232-A clause text;
- the exact wording, figures, or mechanical requirements of RS-232-A;
- that RS-232-A was the first historical document ever to propose a 25-position mapping;
- that the standard normatively required Bell's specific Cinch/Cannon connector shell;
- which electrical limits changed from May 1960 RS-232 to October 1963 RS-232-A;
- that all post-1963 data sets actually conformed, despite IBM's broad 1969 field-engineering statement;
- first shipment, first installation, or industry-wide adoption dates;
- any causal path from EIA committee work to a particular vendor's connector choice.

## Repository consequence

The `EIA RS-232 revisions` ROADMAP item should remain incomplete. The missing October 1963 EIA pamphlet is still the highest-value source because only it can support a clause-by-clause A→B comparison.

However, one previous uncertainty can now be narrowed: the familiar 1–25 **circuit-position assignment** is independently attributed by IBM to RS-232-A, rather than being supported only by Bell's 1964 implementation. The remaining connector question is specifically about the normative mechanical shell, not about whether RS-232-A had standardized pin/circuit positions.

Research and drafting: **OpenAI, 20 October 2026**.
