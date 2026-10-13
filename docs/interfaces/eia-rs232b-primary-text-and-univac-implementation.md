# EIA RS-232-B primary text and a 1968 UNIVAC implementation

## Question

The repository already has a defensible 1960s RS-232 revision spine, but deliberately left clause-level changes and implementation evidence open. This note advances that gap with a surviving reproduction of the October 1965 RS-232-B text embedded, with EIA permission, in a 1968 UNIVAC 9000 Series manual.

The narrow questions are:

1. what does the recovered RS-232-B text itself actually specify about connector mechanics, pin assignment, electrical loading and intended operating range?;
2. can we identify a contemporary computer-vendor implementation that explicitly designed around RS-232-B?;
3. which common retrospective claims remain unsafe without RS-232-A and original RS-232 texts for direct comparison?

## Source and provenance

Sperry Rand, *UNIVAC 9000 Series Data Communications Subsystem: Programmer/Operator Reference*, UP-7613, copyright 1968, reproduces EIA RS-232-B in section 8. The manual states that RS-232-B was the current version and that it was reproduced with the consent of the Electronic Industries Association.

The reproduced title page identifies:

- **EIA Standard RS-232-B**;
- **Revision of RS-232-A**;
- **October 1965**;
- Electronic Industries Association, Engineering Department;
- derivation from RS-232-A plus Standards Proposal No. 879 under Committee TR-30 on Data Transmission Systems and Equipment.

Primary locator: https://bitsavers.org/pdf/univac/9x00/UP-7613_Data_Communications_Subsystem_Programmer-Operator_Reference.pdf, PDF pp. 68-81 (manual section 8).

This is not the original EIA pamphlet as a separately scanned physical artifact. It is, however, a contemporary vendor manual reproducing the standard text with an explicit statement of EIA consent, so it is much stronger evidence for the content of RS-232-B than later summaries.

## What RS-232-B actually says

### Scope and distance

Section 1 defines the interface between data processing terminal equipment and data communication equipment, covering synchronous and asynchronous communication, private-line and switched-network service. Section 1.4 places the signal interchange point on the customer's premises and says interchange circuits are for relatively short distances, **less than fifty feet**.

This is an interface specification. It does not define a character encoding, application protocol or modem modulation scheme.

### Connector mechanics: pin assignment is not connector-shell standardization

The most important recovered boundary is in section 3.

Section 3.1 requires the DTE/DCE interchange point to be a **pluggable connector**, with the female connector associated with the data communication equipment and an extension cable with a male connector supplied with the terminal equipment.

But section 3.2 then states that specifying a **25-pin connector is intended for a future revision**.

At the same time, section 3.4 gives numbered assignments for positions 1 through 25. Among the familiar assignments are:

- 1 protective ground (AA);
- 2 transmitted data (BA);
- 3 received data (BB);
- 4 request to send (CA);
- 5 clear to send (CB);
- 6 data set ready (CC);
- 7 signal ground (AB);
- 8 data carrier detector (CF);
- 20 data terminal ready (CD);
- 22 ring indicator (CE).

Therefore RS-232-B is direct evidence for a **25-position pin-numbering scheme**, but it is direct negative evidence against saying that RS-232-B itself standardized the physical 25-pin connector shell. Those are distinct claims.

This distinction is especially important because later summaries often collapse “25 pin assignments” and “the DB-25 connector was standardized” into one event.

### Electrical characteristics

The reproduced RS-232-B text provides the following directly recoverable constraints:

- maximum open-circuit voltage to protective or signal ground: **25 V**;
- maximum short-circuit current between conductors: **0.5 A**;
- data marking condition: more negative than **-3 V**;
- data spacing condition: more positive than **+3 V**;
- receiver terminating resistance: **3,000-7,000 ohms**;
- receiver-side effective shunt capacitance, including connecting cable: at most **2,500 pF**;
- the undefined transition region is between +3 V and -3 V;
- section 4.7 constrains rise/fall time through that undefined six-volt range to at most three percent of nominal signal-element duration for data and timing circuits.

Section 5.3 says the standard is intended for transmission speeds from zero to an upper limit of approximately **10,000-30,000 baud**. This is an intended design range in RS-232-B, not evidence that any particular modem or terminal actually operated at 30 kbaud.

## Contemporary implementation evidence: UNIVAC 9000

The surrounding 1968 manual is not merely a convenient container for the EIA text. It also records implementation practice.

Section 8.1 says the serial-data interface standard adhered to by common carriers and specified in the design of **all UNIVAC communication equipment** was the EIA RS-232 specification, with RS-232-B identified as the current version.

Elsewhere, the manual's communication-interface characteristics table explicitly marks several UNIVAC interface variants as **EIA RS 232B**. The interunit-cabling table gives **50 feet** as the maximum communication-interface-to-modem cable length for DCS-1, DCS-4 and DCS-4A, matching the short-distance design envelope reproduced in section 1.4.

This gives a useful deployment/implementation lower bound: by 1968, Sperry Rand documented production UNIVAC 9000-series communications subsystem interfaces in explicit RS-232-B terms. It does **not** establish the first RS-232-B implementation by UNIVAC, the first customer installation, or industry-wide adoption in 1965.

The manual also shows why “RS-232 speed” must not be confused with modem line speed. Its modem compatibility table pairs RS-232-B-capable communication interfaces with multiple modem/services and rates. RS-232-B is the local DTE/DCE electrical/control interface; the remote communication service and modem modulation are separate engineering layers.

## What changed from RS-232-A?

The title page explicitly calls RS-232-B a revision of RS-232-A and says it derives from RS-232-A plus Standards Proposal No. 879. That establishes the **document-revision relation** at high certainty.

It does **not** by itself establish which individual clauses came from A and which were introduced by Proposal 879. In particular, this evidence alone cannot safely say that RS-232-B introduced the 2,500 pF limit, changed a voltage limit, or introduced the numbered pin assignments. Those claims require the October 1963 RS-232-A text (or a reliable clause-level change record) for comparison.

## Lineage assessment

Supportable relation:

- `RS-232-B revision-of RS-232-A` — **high certainty**, explicit on the reproduced EIA title page.

Do not encode a broader technological `derived-from` or causal edge merely from chronology. Do not infer that UNIVAC hardware is “derived from” RS-232-B; the manual supports **conformance/design-to-interface** language, not hardware ancestry.

If the structured relation vocabulary lacks a narrowly defined `revision-of` relation, leave the relation in prose rather than force a misleading lineage type.

## What this evidence explicitly does not prove

This source does **not** prove:

- the exact clause-level delta from RS-232-A to RS-232-B;
- that RS-232-A lacked any of the electrical or pin-assignment features seen here;
- that RS-232-B standardized the physical DB-25/D-subminiature connector shell;
- that every device using the familiar 25-position numbering used the same physical connector;
- that 30 kbaud was a guaranteed or deployed operating rate;
- that RS-232-B defined modem modulation, character encoding, framing or end-to-end protocol;
- first vendor adoption, first customer shipment, or first production installation of RS-232-B;
- industry-wide adoption merely because a 1968 UNIVAC manual calls the interface accepted by common carriers;
- any causal relation between publication of RS-232-B and a particular UNIVAC product decision beyond the manual's explicit design/conformance statement.

## Repository consequence

The roadmap item **EIA RS-232 revisions** remains incomplete, but the 1965 edition is no longer represented only by a date/title spine. The repository now has recoverable primary text for RS-232-B plus one concrete 1968 vendor implementation context.

Highest-value next source: the October 1963 RS-232-A text, followed by a clause-by-clause A→B comparison. That comparison should be completed before accepting retrospective claims about which revision changed voltage, capacitance or connector requirements.

Research and drafting: **OpenAI, 13 October 2026**.
