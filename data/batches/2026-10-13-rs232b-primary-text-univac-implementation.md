# Research batch — RS-232-B primary text and UNIVAC implementation

Date: 2026-10-13

## Target gap

ROADMAP: `1960s → Terminals and access → EIA RS-232 revisions`.

Existing coverage already established the 1960 / 1963 A / 1965 B / 1969 C chronology but explicitly left clause-level technical deltas and implementation evidence open.

## New evidence

### E1 — contemporary reproduction of RS-232-B

Source: Sperry Rand, *UNIVAC 9000 Series Data Communications Subsystem: Programmer/Operator Reference*, UP-7613 (1968), section 8, reproducing EIA RS-232-B with stated EIA consent.

URL: https://bitsavers.org/pdf/univac/9x00/UP-7613_Data_Communications_Subsystem_Programmer-Operator_Reference.pdf

Locators:

- PDF p. 68 / section 8.1: RS-232-B identified as current version and reproduced with EIA consent.
- PDF p. 69: EIA title page, `RS-232-B`, `Revision of RS-232-A`, October 1965; from RS-232-A and Standards Proposal No. 879 under Committee TR-30.
- PDF p. 70: scope; customer-premises / <50 ft interface envelope.
- PDF pp. 76-77: pluggable-connector requirement; future-revision statement for a 25-pin connector; numbered 1-25 pin assignments.
- PDF pp. 78-80: electrical limits, 3-7 kohm termination, <=2500 pF effective shunt capacitance, +/-3 V recognition thresholds, rise/fall constraint, approximate 10,000-30,000 baud intended upper range.

Evidence strength: **high** for the content of RS-232-B. The copy is embedded rather than a separately scanned EIA pamphlet, but the 1968 manual explicitly says it is reproduced with EIA consent.

### E2 — 1968 vendor implementation context

Same source.

Locators:

- PDF p. 31: UNIVAC communication-interface characteristics table marks interface variants `EIA RS 232B`.
- PDF p. 61: communication-interface-to-modem maximum cable length 50 ft for DCS-1, DCS-4 and DCS-4A.
- PDF p. 68: manual states EIA RS-232 was specified in design of all UNIVAC communication equipment and calls B the current version.

Evidence strength: **high** for documented 1968 UNIVAC design/conformance; **low/none** for first customer deployment or first vendor adoption.

### E3 — official/historical catalog corroboration

Accuris/TIA historical standards catalog lists RS-232-B as October 1965 and RS-232-A as October 1963.

URL: https://store.accuristech.com/standards/tia-rs-232-b?product_id=2593750

Use: bibliographic corroboration only; the recovered UNIVAC reproduction is stronger for clause content.

## New facts safe to add

1. RS-232-B explicitly identifies itself as a revision of RS-232-A and as deriving from RS-232-A plus Standards Proposal No. 879 under EIA Committee TR-30. **Certainty: high.**
2. RS-232-B requires a pluggable DTE/DCE connector but says specification of a 25-pin connector is intended for a future revision. **Certainty: high.**
3. RS-232-B nevertheless specifies numbered positions 1-25 and assigns familiar circuits to many of them. Thus physical connector-shell standardization and pin-number assignment must not be collapsed into one claim. **Certainty: high.**
4. Recovered B electrical constraints include <=25 V open-circuit, <=0.5 A short-circuit, +/-3 V recognition thresholds, 3-7 kohm receiver termination, and <=2500 pF effective shunt capacitance including cable. **Certainty: high.**
5. B states an intended approximate upper range of 10,000-30,000 baud; this is not a deployed modem-speed claim. **Certainty: high.**
6. By 1968, Sperry Rand documented UNIVAC 9000 communications subsystem interfaces explicitly as EIA RS-232-B and used a 50-ft interface-to-modem cable limit. **Certainty: high for documentation/design, not first deployment.**

## Lineage / relation assessment

Candidate edge:

- `RS-232-B revision-of RS-232-A` — **high certainty**, explicit in source.

Do not mint as `derived-from` if the relation vocabulary does not distinguish document revision from technological ancestry.

UNIVAC equipment should be represented, if desired, by a conformance/implements-interface relation, not a lineage edge.

## Explicit negative claims

The evidence does not prove:

- which clauses differ from RS-232-A;
- that A lacked the 2500 pF, voltage or pin-assignment provisions;
- that B standardized the physical DB-25 shell;
- first UNIVAC implementation or first customer installation;
- universal carrier/vendor adoption in 1965;
- that the approximate 30 kbaud upper design range was achieved in a named deployed system;
- that publication chronology caused later hardware design decisions.

## Files added / suggested follow-up

Added:

- `docs/interfaces/eia-rs232b-primary-text-and-univac-implementation.md`
- `data/batches/2026-10-13-rs232b-primary-text-univac-implementation.md`

Suggested next work:

1. recover October 1963 RS-232-A primary text;
2. perform clause-level A→B comparison;
3. only then encode claims about which revision changed capacitance, voltage or connector requirements;
4. separately recover RS-232-C original text to determine exactly when the physical 25-pin connector form became normative rather than merely anticipated.
