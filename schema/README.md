# Structured Record Layer

The repository began with narrative Markdown and CSV discovery ledgers. Those are deliberately retained: prose is good for historical explanation, and CSV is good for quickly preventing a newly discovered object from disappearing.

The `schema/` layer adds a third form: **claim-oriented machine-readable records**.

## Why add structured records?

A long article can say:

> the 1982 BBN Internet Gateway ran on PDP-11/LSI-11 hardware and supported several network interfaces.

But a database-quality archaeological record should be able to preserve:

- which exact gateway/site/revision;
- exact processor model if known;
- each interface board as a related artifact;
- which document supports each interface;
- page/section locator;
- whether the claim is confirmed or provisional;
- whether a surviving specimen exists;
- whether the source is safe to mirror or should only be linked.

This structure is necessary if the project eventually contains tens of thousands of claims.

## Schemas

- [`artifact-record.schema.json`](artifact-record.schema.json)
- [`source-record.schema.json`](source-record.schema.json)

The schemas use JSON Schema draft 2020-12.

## Three-level workflow

### 1. Discovery — CSV ledger

If you encounter an obscure object while reading, save it immediately in:

- `data/artifact-ledger.csv`, or
- `data/source-ledger.csv`.

Do not wait until enough evidence exists for an article.

### 2. Excavation — Markdown

Write a narrative or technical excavation when a topic needs relationships explained. Markdown is where ambiguity, context, historical interpretation and long unresolved-question lists are easiest to express.

### 3. Promotion — structured JSON

Create a JSON record once claims are stable enough to deserve explicit identities and source locators.

Suggested paths:

```text
records/
  artifacts/
    ART-0063-bbn-darpa-internet-gateway.json
  sources/
    SRC-0048-rfc-823.json
```

A structured record does **not** mean the subject is complete. It means the archive can now reason over its claims without parsing prose.

## Identity rules

IDs are permanent once published.

- artifacts: `ART-####`
- sources: `SRC-####`

If one catalog row later turns out to contain several materially distinct objects, keep the old ID as a family/umbrella record where useful and assign new IDs to the specific revisions.

Never recycle an ID for an unrelated object.

## Granularity rule

Prefer one record per historically meaningful revision.

Bad long-term record:

```text
Bell 103 — 1960s modem
```

Better eventual structure:

```text
Bell Data Set 103 family
  ├── 103A
  ├── 103F
  ├── later variants
  └── compatibility/service relationships
```

The exact split should be driven by evidence, not by a desire to manufacture record count.

## Claim locators

Every nontrivial structured claim should eventually point to the smallest practical locator:

- RFC section;
- report page/figure/table;
- manual page;
- source file and line/commit;
- photograph/archive accession;
- memo date and folder;
- network-map legend;
- tariff page;
- oral-history timestamp/page.

A URL alone is discovery metadata, not a precise citation.

## Dates

Do not force one date into an artifact.

Networks/products often have several legitimate milestones:

```text
conceived
announced
first_tested
first_operational
standardized
withdrawn
last_known_use
```

Each date carries precision and certainty.

This is specifically designed to avoid endless arguments caused by calling every different milestone “the invention date.”

## Physical details

When known, structured records should preserve physical facts that conventional software history drops:

- line service;
- bit rate;
- signaling/modulation;
- connectors;
- interface standards;
- board/module names;
- processor/memory;
- rack/enclosure;
- power;
- diagnostics.

A network is an arrangement of physical artifacts, not merely protocol names.

## Operations details

Also preserve:

- monitoring;
- alarms/traps;
- operator console;
- network control center;
- remote boot/reload;
- failure behavior;
- queue exhaustion;
- troubleshooting tools;
- staffing/organizational boundaries.

The infrastructure only existed because somebody operated it.

## Economics

Use the economics block when possible:

- equipment price;
- monthly rental;
- carrier tariff;
- circuit cost;
- payer/funder.

This is essential for dial-up UUCP, leased packet-network lines, public X.25 service and later ISP economics.

## Survival/provenance

Do not write “one survives in museum X” without provenance evidence.

Distinguish:

- a generic surviving model;
- a surviving unit from the relevant organization;
- a unit documented as having served in the historical network;
- a restored operational specimen.

These are different archaeological claims.

## Source fixity

When a lawful local archival copy is kept, record when feasible:

- SHA-256;
- byte size;
- MIME type;
- page count;
- OCR state;
- scan defects.

The checksum is a way to identify a copy, not a statement that redistribution is lawful.

## Rights

Metadata preservation and document redistribution are separate actions.

A copyrighted manual can have an excellent source record without being committed to this repository.

If rights are unknown, default to metadata + stable link/archive locator rather than mirroring the file.

## Validation

The evidence graph can be checked locally with one deterministic command set:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_records.py
python -m unittest discover -s tests -v
```

The `Validate evidence graph` GitHub Actions workflow runs the same validator
and tests on pull requests and on pushes to `main`, against Python 3.11 and
3.13.

The validator checks every structured artifact, source and lineage record against
its Draft 2020-12 JSON Schema. It also enforces repository-wide invariants that a
schema cannot express:

- structured IDs are unique and agree with their filenames;
- IDs in each discovery ledger are well formed and unique;
- artifact/source references in structured records resolve to either a
  structured record or a discovery-ledger identity;
- every artifact referenced by an extracted source claim is also declared in
  that source record's top-level `artifact_ids` summary;
- non-empty `from_artifact_id` and `to_artifact_id` values in the lineage
  discovery ledger obey the same resolution policy;
- `source_ref` values in lineage records are checked whenever they contain
  explicit `SRC-*` IDs.

A ledger identity is allowed as a reference target because discovery normally
precedes promotion to a claim-level JSON record. It is not treated as evidence
that the target has already been fully excavated.

Future repository tooling should add:

1. URL/dead-link checks with archival fallbacks;
2. chronology checks for impossible ordering;
3. SHA-256 calculation for lawful local source copies;
4. a generator that exports JSON records into browsable tables/graphs;
5. a citation coverage report showing claims without precise locators.

The long-term objective is a corpus that can be read as history **and** interrogated as an evidence graph.
