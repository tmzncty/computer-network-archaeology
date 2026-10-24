# IBM evidence for the RS-232-A → RS-232-B clause delta

## Question

The repository has recovered the October 1965 RS-232-B text and independent evidence that RS-232-A already assigned interface circuits to numbered positions. What remained missing was a contemporary source that explicitly identifies particular requirements as **additions in RS-232-B over RS-232-A**.

A 1969 IBM field-engineering handbook supplies exactly that comparison.

## Source and locator

IBM, *Teleprocessing General — Field Engineering Handbook*, form Y27-0042-1, March 1969. The relevant subsection is **“RS-232-B INTERFACE”**, manual page **2-10**, revision marker **(7/68)**.

Surviving scan/searchable copy:

- https://www.bitsavers.org/pdf/ibm/datacomm/Y27-0042-1_Teleprocessing-General_FE_Handbook_Mar69.pdf

This is not the EIA RS-232-A pamphlet itself. It is a near-contemporary IBM engineering handbook explicitly comparing A and B, so it is strong evidence for the stated delta but should not be treated as a substitute for a complete A text.

## Explicit A → B comparison

IBM first states that the **pin assignments, names, and directions** of the interface leads in RS-232-B are identical to RS-232-A. This independently reinforces the repository's earlier conclusion that the familiar circuit-to-position mapping was already present in A.

IBM then says RS-232-B **added the following requirements over RS-232-A**:

1. **Signal-ground / protective-ground bonding provision.** Signal ground at pin 7 is to be brought to one point in the data set, where it can be connected to protective ground at pin 1 by a wire strap.
2. **Receiver terminating resistance.** The receiving end of an interchange circuit is to present a terminating resistance of **not less than 3,000 ohms and not more than 7,000 ohms**.

These are clause/property-level differences explicitly attributed by IBM to B over A. They are stronger evidence than inferring change merely because the requirements appear in the recovered B text.

## What this changes in the repository

The recovered RS-232-B text already establishes a 3,000–7,000 ohm receiver terminating resistance. Until this source, however, the repository correctly refused to claim that this requirement was **introduced by B**, because the A text was unavailable for direct comparison.

IBM's comparison now supports the narrower historical statement:

> By IBM's contemporary engineering account, RS-232-B added the 3–7 kΩ receiver terminating-resistance requirement over RS-232-A, and also added an explicit signal-ground/protective-ground bonding provision.

The same IBM passage says the pin assignments, names and directions were unchanged from A to B. Therefore those properties should **not** be listed as B innovations.

## Evidence strength and lineage

- `RS-232-B revision-of RS-232-A` — **high certainty**; already explicit on the reproduced EIA B title page.
- `3–7 kΩ receiver termination introduced-in RS-232-B relative to RS-232-A` — **high certainty for the comparative claim**, because IBM explicitly labels it an added B requirement.
- `pin assignments/names/directions preserved A→B` — **high certainty**, explicit in the same IBM comparison.
- `signal-ground/protective-ground strap provision introduced-in B relative to A` — **high certainty**, explicit in the same IBM comparison.

These are standard-revision/property relations, not evidence that one physical product caused another. Do not encode a generic technological `derived-from` edge merely from this chronology.

## What this evidence explicitly does not prove

This source does **not** prove:

- the complete clause-by-clause RS-232-A → RS-232-B delta;
- that the two IBM-listed additions were the **only** changes in B;
- that RS-232-B introduced the 2,500 pF capacitance limit, voltage limits, rise/fall-time rule, or intended baud range;
- that RS-232-A standardized a particular DB-25/D-subminiature connector shell;
- that unchanged pin assignments imply unchanged connector mechanics;
- why EIA chose the 3–7 kΩ range or the grounding provision;
- that any particular modem or terminal implemented the new requirements immediately in October 1965;
- first deployment, first shipment, or industry-wide adoption of RS-232-B.

The October 1963 RS-232-A pamphlet remains the highest-value missing source. It is still required before asserting changes not explicitly identified by this IBM comparison.

## Repository consequence

This closes one narrow part of the ROADMAP item **EIA RS-232 revisions**: the repository now has contemporary evidence for at least two specific A→B additions and for continuity of pin assignments/names/directions. The broader roadmap item remains open pending recovery of RS-232-A and a fuller A→B comparison.

Research and drafting: **OpenAI, 24 October 2026**.
