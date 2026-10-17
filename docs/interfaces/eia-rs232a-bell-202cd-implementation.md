# EIA RS-232-A in the Bell System Data Sets 202C and 202D

## Question

The repository has recovered the 1960/1963-A/1965-B/1969-C revision spine and primary text for RS-232-B, but the October 1963 RS-232-A edition is still missing as a primary standard text. This note advances the gap from a different direction: a surviving Bell System interface specification dated May 1964 documents a concrete, near-contemporary implementation of RS-232-A in Data Sets 202C and 202D.

The narrow questions are:

1. did a named Bell System data-set revision explicitly implement RS-232-A soon after the October 1963 standard?;
2. what interface changes did Bell document when moving from 202A/202B to 202C/202D?;
3. what connector and cable practice did this implementation actually use?;
4. which claims about the RS-232-A standard itself remain unsafe without the EIA text?

## Primary source

Bell System Data Communications, *Data Set 202C and 202D — Interface Specification*, May 1964.

Surviving scan: https://bitsavers.org/communications/westernElectric/modems/202C_and_202D_Interface_Specification_May64.pdf

Computer History Museum access copy: https://archive.computerhistory.org/resources/access/text/2024/09/102749014-05-0012-acc.pdf

The document is a vendor technical reference for the named data sets, not a retrospective history.

## Model succession and interface change

The opening comparison explicitly says **Data Sets 202C and 202D supersede Data Sets 202A and 202B**. It then says the new models meet the new **EIA RS-232-A interface standard of October 1963**.

Section 2.1 makes the implementation change more concrete: the 202C/202D interface conforms to RS-232-A in that **voltage levels are used for communication on all leads**.

This matters because the same document's interface table compares the older 202A/202B assignments with the RS-232-A-style interface. Some older interface functions are identified as contact-closure leads while the new interface uses the standardized voltage-signaling arrangement.

The safe lineage statement is therefore property-level:

- `Data Set 202C/202D successor-of Data Set 202A/202B` — **high certainty**, explicit vendor wording;
- `Data Set 202C/202D implements/conforms-to RS-232-A interface convention` — **high certainty**, explicit vendor wording;
- the documented inherited/changed property is the DTE/DCE interface, including the move to voltage signaling on all interface leads.

This is not evidence that RS-232-A was derived from Bell 202C/202D. The standard predates this May 1964 document, but chronology alone does not establish the opposite influence either.

## Connector implementation

Section 4.21 gives an unusually concrete implementation snapshot. The customer's data equipment is to use a cable terminating in a **Cinch or Cannon DB-19604-432 plug** in a **Cinch DB-s1226-1 hood assembly or equivalent**. The data-set receptacle is equivalent to **Cinch or Cannon DB-19604-433** and has threaded retaining spacers; retaining screws in the hood prevent accidental disengagement.

The same section says the cable **should not exceed 50 feet**.

The interface-connection figure maps positions 1 through 25 to RS-232-A circuit designations, including familiar assignments such as protective ground (AA), transmitted data (BA), received data (BB), request to send (CA), clear to send (CB), data set ready (CC), signal ground (AB), data carrier detector (CF), data terminal ready (CD), and ring indicator (CE).

This is strong evidence for a **Bell implementation using a specific 25-position D-subminiature-family plug/receptacle and the RS-232-A circuit numbering in May 1964**.

It is not sufficient evidence that the October 1963 EIA standard itself normatively required that exact Cinch/Cannon shell. That distinction is important because the recovered RS-232-B text later says specification of a 25-pin connector was intended for a future revision while nevertheless assigning positions 1–25. Vendor implementation and normative standard text must therefore remain separate until the RS-232-A text is recovered.

## Operational/product context

The specification distinguishes the new models by service role:

- **202C**: DATA-PHONE service where an integrated equipment arrangement is desired, plus alternate voice-data private-line service;
- **202D**: data-only private-line service;
- 202D combined with Data Auxiliary Set 804A variants supports additional alternate voice/data arrangements.

It also says 202C/202D are compatible with the **standard version of the Automatic Calling Unit (ACU)**, whereas 202A/202B had been compatible with model-shop ACUs but not the standard ACU. The new sets provide the required 2025-cps tone capability for that application.

These statements document intended product/service integration. They do not establish first shipment, first customer installation, installed-base size, or industry-wide adoption.

## Independent contemporary corroboration

IBM's March 1966 field-engineering training manual *Common Carrier Facilities for Teleprocessing* describes 202A/202B as obsolete but still widely present and says many IBM machines in the relevant rate range were still interfaced for A/B rather than C/D. It explicitly contrasts the older interface with RS-232-A, noting contact closure on certain leads, and describes 202C/202D as the more recent models.

Surviving scan: https://archive.decromancer.ca/bitsavers.org/pdf/ibm/datacomm/Z25-2529-0_Common_Carrier_Facilites_For_Teleprocessing_Mar66.pdf

This is valuable negative context: a standards-conforming successor did not instantly erase the older installed base.

## Lineage assessment

Candidate relations supported by explicit documentation:

- `Bell Data Set 202C successor-of Bell Data Set 202A` — **high certainty**;
- `Bell Data Set 202D successor-of Bell Data Set 202B` — **high certainty**;
- `Bell Data Set 202C implements-interface RS-232-A` — **high certainty**;
- `Bell Data Set 202D implements-interface RS-232-A` — **high certainty**.

Only mint machine-readable edges if the repository vocabulary has semantics narrow enough for product succession and standard conformance. Do not substitute `derived-from` merely because it is available.

## What this evidence explicitly does not prove

This evidence does **not** prove:

- the complete clause text of October 1963 RS-232-A;
- which RS-232-A clauses differed from the original May 1960 RS-232;
- that RS-232-A normatively required the exact Cinch/Cannon connector used by Bell;
- that RS-232-A originated the familiar 25-position numbering;
- that Bell's 202C/202D caused RS-232-A, or that RS-232-A caused every 202C/202D engineering change;
- first announcement, first shipment, first installation, or first revenue service for 202C/202D;
- immediate replacement of 202A/202B in the field;
- universal vendor adoption of RS-232-A in 1964.

## Repository consequence

The ROADMAP item `EIA RS-232 revisions` remains incomplete because the primary RS-232-A text is still missing. The coverage gap is nevertheless narrower: there is now a named May 1964 Bell System implementation, a documented A/B→C/D product succession, a property-level interface change, exact connector hardware, and evidence that older A/B interfaces remained operational into 1966.

Highest-value next source remains the October 1963 EIA RS-232-A pamphlet itself. Once recovered, compare its connector and electrical clauses directly with both this May 1964 Bell implementation and the recovered October 1965 RS-232-B text.

Research and drafting: **OpenAI, 17 October 2026**.
