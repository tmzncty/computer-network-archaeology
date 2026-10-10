# EIA RS-232 in the 1960s: revision chronology and evidence boundaries

## Question

The roadmap lists both **serial interfaces before RS-232 standardization** and **EIA RS-232 revisions** as open coverage. Before reconstructing individual electrical changes, the repository needs a defensible revision spine: which 1960s editions existed, when were they issued, what did the 1969 edition claim to standardize, and what can later evidence safely say about adoption?

## Strongest recovered source

A useful near-contemporary institutional source is the U.S. National Bureau of Standards survey *Interface Standards for Automated Coal Mining Equipment*. Its RS-232-C entry identifies the standard as:

- **EIA RS 232-C, August 1969**;
- title: *Interface Between Data Terminal Equipment and Data Communication Equipment Employing Serial Binary Data Interchange*;
- maintenance authority: **Electronic Industries Association, Subcommittee TR-30.2**.

The same entry gives the preceding revision sequence explicitly:

| edition | date reported by NBS |
| --- | --- |
| RS 232 | May 1960 |
| RS 232-A | October 1963 |
| RS 232-B | October 1965 |
| RS 232-C | August 1969 |

Source: National Bureau of Standards, *Interface Standards for Automated Coal Mining Equipment*, RS-232-C entry, p. 17 in the GovInfo PDF: https://www.govinfo.gov/content/pkg/GOVPUB-C13-eb9a42c57ad9d661ec3bb231207d0919/pdf/GOVPUB-C13-eb9a42c57ad9d661ec3bb231207d0919.pdf

This chronology is materially better evidence than undated web summaries because it is an institutional standards survey that names the responsible EIA subcommittee and bibliographically identifies the August 1969 standard.

## What RS-232-C covered

The NBS entry summarizes the 1969 scope as the interconnection of **data terminal equipment (DTE)** and **data communication equipment (DCE)** using serial binary data interchange. It says RS-232-C defined four classes of interface property:

1. electrical signal characteristics;
2. mechanical interface characteristics;
3. functional descriptions of interchange circuits;
4. standard interfaces for selected communications-system configurations.

The entry also identifies related standards, including EIA RS-334 / ANSI X3.24-1968 for signal quality and CCITT V.24 plus V.28/V.31 as competing or corresponding international work.

This matters for repository language: RS-232-C should be treated as an **interface standard**, not as a character encoding, terminal protocol, modem modulation scheme, or complete end-to-end communications protocol.

## Contemporary implementation evidence

The NBS survey says RS-232-C had, commercially, achieved broad acceptance as the terminal-to-modem interface by the time of the survey. It also describes RS-232-C as constrained to approximately **20 kbit/s and 12 metres** in that survey's comparison with the newer RS-422/423 family.

A 14 September 1978 *Electronics* article independently describes RS-232-C as the most widely used DTE/DCE interface and characterizes it as intended for serial interchange over less than 50 feet at rates below 20 kilobaud. This is useful corroboration for late-1970s practice, but it is not evidence for the adoption state in 1960, 1963, 1965, or 1969.

Source: *Electronics*, 14 September 1978, discussion of interface standards: https://www.worldradiohistory.com/Archive-Electronics/70s/78/Electronics-1978-09-14.pdf

## Revision and lineage interpretation

The dated sequence supports a high-confidence **revision-of** relation among the named standards:

`RS-232 (1960) → RS-232-A (1963) → RS-232-B (1965) → RS-232-C (1969)`

This is a standards-document revision chain, not proof that every deployed device was upgraded in the same sequence or on the publication dates.

The NBS source also says RS-422 and RS-423 were expected to replace RS-232-C gradually. That is evidence of a contemporary **planned standards succession**, not proof that RS-232-C actually disappeared, nor proof that RS-422/423 are simple code- or design-descendants of every RS-232-C mechanism. A generic `derived-from` edge would overstate the evidence.

## What this evidence does not prove

This evidence does **not** prove:

- the exact drafting or committee-approval date of the original RS-232 before its May 1960 issue;
- the exact technical delta between 232, 232-A, and 232-B;
- that a particular voltage, capacitance, connector, or pin assignment changed in a particular revision unless the revision text itself is recovered;
- that DB-25 was mandatory in every 1960s edition;
- that RS-232 defines ASCII, start/stop framing, modem modulation, or an application protocol;
- that equipment vendors implemented each edition immediately after publication;
- that late-1970s commercial ubiquity proves 1960s deployment volume;
- that RS-422/423 actually replaced RS-232-C on the schedule expected by the NBS survey;
- any causal relation merely because one standard was published before another.

## Repository consequences

This evidence is enough to replace vague statements such as “RS-232 appeared in the early 1960s” with a revision-specific spine. It is **not** enough to close the roadmap item for EIA RS-232 revisions completely. The next step should recover scans or catalog records for the 1960, 1963, and 1965 EIA texts and compare their electrical, circuit-function, and mechanical clauses directly.

### Suggested lineage edge

If the structured vocabulary has a relation whose semantics are strictly document revision/supersession, the following edges are supportable at **high certainty**:

- RS-232-A `revision-of` RS-232;
- RS-232-B `revision-of` RS-232-A;
- RS-232-C `revision-of` RS-232-B.

Do **not** encode these as broad technological causation or implementation descent if `revision-of` is unavailable.

Research and drafting: **OpenAI, 10 October 2026**.
