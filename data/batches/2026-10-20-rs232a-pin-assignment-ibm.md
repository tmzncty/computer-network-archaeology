# Research batch — RS-232-A pin-assignment evidence from IBM

Date: 2026-10-20

## Coverage gap

`ROADMAP.md` still marks `EIA RS-232 revisions` incomplete. Existing repository work recovered the revision chronology, RS-232-B primary text, and a May 1964 Bell RS-232-A implementation, but deliberately left open whether the 1–25 circuit-position assignment was a property of RS-232-A itself or only demonstrated by the Bell implementation.

## New evidence

### IBM Teleprocessing General — Field Engineering Handbook

- Organization: IBM
- Form: Y27-0042-1
- Date: March 1969
- Location: Chapter 2, `DATA COMMUNICATIONS INTERFACE SUMMARY`, subsection `DATA SET INTERFACE INFORMATION`
- Surviving scan: https://www.bitsavers.org/pdf/ibm/datacomm/Y27-0042-1_Teleprocessing-General_FE_Handbook_Mar69.pdf
- Evidence strength: high for IBM's contemporary attribution; secondary to the missing EIA pamphlet for normative clause wording.

Claims supported:

1. Before 1963, business machines and data sets did not necessarily place a given signal on the same interface pin, so system-specific cables were required.
2. IBM says the RS-232-A EIA Standard Interface was agreed upon in 1963.
3. IBM explicitly introduces the following mapping as the pin assignments set forth in RS-232-A.
4. Therefore the circuit-to-position mapping can be attributed to RS-232-A with substantially stronger evidence than vendor implementation alone.

### IBM Common Carrier Facilities for Teleprocessing

- Organization: IBM Field Engineering Education
- Form: Z25-2529-0
- Date: March 1966
- Location: bibliography/reference section near p. 102 of the scan
- Surviving scan: https://archive.decromancer.ca/bitsavers.org/pdf/ibm/datacomm/Z25-2529-0_Common_Carrier_Facilites_For_Teleprocessing_Mar66.pdf
- Evidence strength: high for existence/availability/use as an engineering reference; not a substitute for the standard text.

Claims supported:

1. IBM explicitly lists `EIA Standard. Form # RS-232-A`.
2. It describes the document as specifying the interface between data-processing terminal equipment and data-communication equipment.
3. It gives the EIA Engineering Department in New York as the source and a price of $0.90, demonstrating that RS-232-A was a concrete obtainable engineering publication by March 1966.

## Candidate repository changes

Added:

- `docs/interfaces/eia-rs232a-pin-assignment-evidence.md`
- this batch file

Do not mark the ROADMAP item complete until the October 1963 EIA text itself is recovered.

## Candidate lineage / relation edges

No machine-readable lineage edge added.

- `Bell Data Set 202C/202D implements RS-232-A circuit assignment` — high certainty, already supported by Bell 1964 plus IBM's independent attribution.
- `RS-232-A standardizes circuit-to-position assignment` — high-confidence property relation, but current lineage vocabulary may not encode standards-property relations cleanly.
- `RS-232-A -> specific Cinch/Cannon D-sub shell` — unsupported; do not add.

## Evidence boundary / does not prove

This batch does not prove:

- complete RS-232-A normative text;
- exact mechanical connector requirement in RS-232-A;
- that RS-232-A first invented the 25-position concept;
- an A→B electrical delta;
- universal vendor conformance after 1963;
- first deployment or shipment;
- causal influence merely from chronology.

## Next target

Recover the October 1963 EIA RS-232-A pamphlet or a faithful full reprint. Then perform clause-level A→B comparison against the already recovered October 1965 RS-232-B text, keeping circuit-position assignment separate from mechanical connector-shell requirements.
