# Research batch — RS-232-A → RS-232-B IBM comparison

Date: 2026-10-24
Scope: EIA RS-232 revisions; property-level A→B delta

## New evidence

### E1 — IBM explicitly says B retained A's lead mapping

**Source:** IBM, *Teleprocessing General — Field Engineering Handbook*, Y27-0042-1, March 1969, “RS-232-B INTERFACE,” p. 2-10, revision marker (7/68).

**Locator:** https://www.bitsavers.org/pdf/ibm/datacomm/Y27-0042-1_Teleprocessing-General_FE_Handbook_Mar69.pdf

**Finding:** IBM says the pin assignments, names and directions of the RS-232-B interface leads are identical to RS-232-A.

**Certainty:** high.

**Supports:** continuity of circuit/position mapping A→B.

**Does not prove:** identity of physical connector shells or every electrical clause.

### E2 — IBM identifies a grounding provision as added in B

**Source/locator:** same as E1.

**Finding:** IBM says B added a requirement that signal ground (pin 7) be brought to one point in the data set, with provision to connect it to protective ground (pin 1) by wire strap.

**Certainty:** high for the A→B comparative claim.

**Does not prove:** the engineering motivation, deployment date, or that all contemporary equipment immediately complied.

### E3 — IBM identifies 3–7 kΩ receiver termination as added in B

**Source/locator:** same as E1.

**Finding:** IBM says B added a requirement that receiver terminating resistance be no less than 3,000 ohms and no more than 7,000 ohms.

**Certainty:** high for the A→B comparative claim.

**Cross-check:** the separately recovered RS-232-B text contains the 3,000–7,000 ohm receiver terminating-resistance requirement. IBM's comparison adds the missing historical attribution that this was new relative to A.

**Does not prove:** that other B electrical properties such as the 2,500 pF capacitance limit were also new in B.

## Suggested repository placement

Added narrative:

- `docs/interfaces/eia-rs232a-to-b-ibm-delta.md`

Related existing material:

- `docs/interfaces/eia-rs232-1960s-revision-chronology.md`
- `docs/interfaces/eia-rs232a-pin-assignment-evidence.md`
- `docs/interfaces/eia-rs232b-primary-text-and-univac-implementation.md`

## Lineage / relation assessment

Existing document lineage remains:

- `RS-232-B revision-of RS-232-A` — high certainty.

New property-level relations supported in prose:

- pin assignments/names/directions: **preserved A→B** — high certainty;
- signal-ground/protective-ground strap provision: **added in B relative to A** — high certainty;
- 3–7 kΩ receiver termination: **added in B relative to A** — high certainty.

Do not create a generic `derived-from` edge between hardware products from this evidence. If the repository later introduces typed standard-property edges, these findings are candidates for those narrower relations.

## Negative evidence boundary

This batch does not establish a complete A→B diff. In particular it does not establish when the 2,500 pF capacitance limit, voltage limits, transition-time requirement, intended baud range, or any specific D-sub connector shell entered the standard. Recovery of the October 1963 RS-232-A text remains necessary.
