# Research batch — RS-232-A Bell Data Set 202C/202D implementation

Date: 2026-10-17

## Target gap

ROADMAP: `1960s → Terminals and access → EIA RS-232 revisions`.

Existing coverage establishes the revision chronology and recovers RS-232-B primary text, but RS-232-A primary text and clause-level A→B comparison remain open. This batch adds near-contemporary implementation evidence without pretending the vendor manual is the EIA standard itself.

## E1 — Bell System 202C/202D interface specification

Source: Bell System Data Communications, *Data Set 202C and 202D — Interface Specification*, May 1964.

URLs:

- https://bitsavers.org/communications/westernElectric/modems/202C_and_202D_Interface_Specification_May64.pdf
- https://archive.computerhistory.org/resources/access/text/2024/09/102749014-05-0012-acc.pdf

Locators / facts:

- opening general/comparison section: 202C and 202D supersede 202A and 202B; new models meet the new EIA RS-232-A standard of October 1963;
- section 2.1: interface conforms to RS-232-A in using voltage levels on all leads;
- section 4.21: customer cable terminates in Cinch or Cannon DB-19604-432 plug with Cinch DB-s1226-1 hood or equivalent; data-set receptacle equivalent to DB-19604-433; threaded retaining hardware; cable should not exceed 50 ft;
- interface-connection figure: positions 1–25 mapped to RS-232-A circuit designations;
- comparison sections: standard-ACU compatibility is a new C/D capability relative to A/B model-shop ACU compatibility.

Evidence strength: **high** for Bell's May 1964 implementation, model succession and connector practice; **none** for exact normative wording of RS-232-A beyond what Bell explicitly attributes to it.

## E2 — IBM 1966 installed-base context

Source: IBM Field Engineering Education, *Common Carrier Facilities for Teleprocessing*, Z25-2529-0, March 1966.

URL: https://archive.decromancer.ca/bitsavers.org/pdf/ibm/datacomm/Z25-2529-0_Common_Carrier_Facilites_For_Teleprocessing_Mar66.pdf

Locator: Session 11, `DATA SET - WESTERN ELECTRIC TYPE 202`, especially `DIFFERENCES - A AND B VS. C AND D`.

Facts:

- IBM calls 202A/B obsolete but says many remained in use;
- IBM says many machines in the 202 rate range were still interfaced for A/B rather than C/D;
- IBM contrasts A/B's use of contact closure on certain interface leads with the newer RS-232-A-oriented C/D interface;
- IBM describes 202C/202D as more recent models.

Evidence strength: **high** for documented IBM field-engineering view in March 1966; not a quantitative installed-base census.

## New facts safe to add

1. By May 1964 Bell documented Data Sets 202C/202D as superseding 202A/202B and meeting EIA RS-232-A of October 1963. **Certainty: high.**
2. Bell explicitly described one interface delta as use of voltage levels on all leads. **Certainty: high.**
3. Bell's 202C/202D implementation used named Cinch/Cannon D-subminiature-family plug/receptacle hardware and a <=50-ft cable recommendation. **Certainty: high.**
4. The Bell implementation used a 1–25 position map with RS-232-A circuit designations. **Certainty: high for implementation, not proof that EIA A normatively mandated the shell.**
5. By March 1966 IBM still reported substantial operational continuity of older 202A/B interfaces despite calling them obsolete. **Certainty: medium-high for qualitative persistence; no quantitative share.**

## Lineage / relation assessment

Candidates:

- `202C successor-of 202A` — **high certainty**, explicit Bell wording;
- `202D successor-of 202B` — **high certainty**, explicit Bell wording;
- `202C implements-interface RS-232-A` — **high certainty**;
- `202D implements-interface RS-232-A` — **high certainty**.

Do not encode these as generic `derived-from` if the structured vocabulary cannot distinguish product succession and standards conformance.

## Explicit negative claims

The evidence does not prove:

- the complete RS-232-A standard text or exact A→B clause delta;
- that RS-232-A itself mandated Bell's exact Cinch/Cannon connector;
- that Bell 202C/202D originated the 25-position convention;
- causal influence from Bell hardware to the EIA standard or vice versa beyond explicit conformance;
- first shipment, first customer installation, or first production use;
- immediate field replacement of 202A/202B;
- universal RS-232-A adoption.

## Files added

- `docs/interfaces/eia-rs232a-bell-202cd-implementation.md`
- `data/batches/2026-10-17-rs232a-bell-202cd-implementation.md`

## Next evidence target

Recover the October 1963 EIA RS-232-A pamphlet and perform a direct A→B clause comparison. The Bell May 1964 implementation should then be compared against the normative A connector and electrical clauses rather than treated as a substitute for them.
