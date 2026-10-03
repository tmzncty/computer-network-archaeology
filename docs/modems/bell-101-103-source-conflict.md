# Research Note: Bell 101 / Bell 103 Chronology Is Not Yet Clean

This note exists because a small modem-history claim already demonstrates the repository's method: **do not copy a widely repeated date until the underlying artifact chain agrees.**

## The common simplified story

Modern histories frequently summarize the lineage roughly as:

```text
SAGE-era modem work
   ↓
Bell 101 — 110 bit/s / late 1950s
   ↓
Bell 103 — 300 bit/s / early 1960s
```

That broad sequence is plausible and useful. The exact product dates, variant names and meanings of “introduced”, “released” and “commercially available”, however, are not yet sufficiently pinned down.

## Evidence currently located

### Bell Laboratories historical innovation list

An IEEE History Center-hosted Bell Telephone Laboratories innovation list includes **“1958 — Bell 101 Dataset Modem.”**

Location:
https://ethw.org/w/images/9/9a/BTL_INNOVATION_LIST_GRAPH.pdf

This supports a 1958 Bell 101 milestone but does not, by itself, define whether that milestone means engineering completion, announcement, SAGE deployment or ordinary commercial availability.

### Computer History Museum

CHM's networking timeline gives a broad **1958 Bell commercialization** milestone for modem technology, while its object page for an early AT&T modem notes Bell Laboratories development during the mid-1950s and later Bell 103 sales.

Locations:
- https://www.computerhistory.org/timeline/networking-the-web/
- https://www.computerhistory.org/revolution/networking/19/371/2033

Again, this is institutional historical evidence, not yet the original product announcement.

### Bell System Practices: Data Set 101C

A surviving-document trail points to:

**Bell System Practices — Data Set 101C: Identification and Operation, Issue 2, March 1963.**

A historical-computing mailing-list discussion links a scan and also identifies later 101C installation/test documents.

Discovery trail:
https://www.classiccmp.org/pipermail/cctalk/2017-May/034745.html

This proves that the **101C variant** must be treated separately from the generic “Bell 101” label. A 1963 101C manual is not proof that every 101-family feature existed in 1958.

### March 1963 Bell System Data Set 103A marketing brochure

A contemporary Bell System marketing brochure is now available as a surviving scan:

**Data Set 103-A**, print code **3163 358** (March 1963).

TCI Library scan:
https://www.telephonecollectors.info/index.php/browse/document-repository/catalogs-manuals/western-electric-bell-system/marketing-documents-by-date/14723-1963-data-set-103a-dataphone/file

This is stronger evidence for public product/service availability than a later retrospective timeline. The brochure advertises the 103-A for ordinary Bell System customers, describing transmission over regular telephone lines, Private Line service and WATS; DATA-PHONE service could use local or long-distance calls at normal telephone rates. It also advertises automatic answering and use with an associated Automatic Calling Unit.

Most importantly, this March 1963 brochure says the product transmits and receives at **up to 200 bits per second**. That does **not** match the later 103A technical material that states up to 300 baud / 300 bit/s in DATA-PHONE service. The discrepancy must be preserved rather than normalized away. Plausible explanations include an early marketed operating limit, a brochure simplification, or a revision/configuration change, but none is proven by the brochure alone.

What this source proves:
- a Bell System product explicitly named **Data Set 103-A** was being marketed by March 1963;
- Bell marketed it for DATA-PHONE, Private Line and WATS contexts;
- the surviving brochure states a maximum of 200 bit/s.

What it does **not** prove:
- that March 1963 was the first announcement, first installation or first sale;
- that all 103A revisions were limited to 200 bit/s;
- when or why the later 300 bit/s rating appeared;
- that a generic “Bell 103” family introduction date equals this brochure date.

### Bell System Practices: Data Set 103A Type

A scan is indexed as:

**SECTION 591-014-100 — DATA SET 103A TYPE — IDENTIFICATION AND OPERATION.**

Bitsavers location:
https://bitsavers.org/communications/westernElectric/modems/591-014-100_Data_Set_103A_Identification_and_Operation_Jan67.pdf

The scan's visible copyright line is **1967**, while machine-readable text exposed by some indexes renders the issue line as “Issue 5, January 1961”. Those signals conflict. Until the original page image and revision history are reconciled, neither OCR-derived “1961” nor a filename-derived edition date should be used as the first-availability date.

A separate February 1967 Bell System *Data Set 103A — Interface Specification* states up to **300 baud (300 bit/s maximum)** in DATA-PHONE service and 150 baud in TWX-CE service:
https://bitsavers.org/communications/westernElectric/modems/103A_Interface_Specification_Feb67.pdf

This makes the March 1963 brochure's **200 bit/s** rating a concrete revision-history question rather than something that should be silently corrected to the familiar later 300 bit/s figure.

The document is nevertheless rich hardware evidence: it describes 103A-type simultaneous low-speed serial transmit/receive service, DATA-PHONE/TWX use, two FSK channels, business-machine interface leads, line-control circuitry, manual/automatic answer and physical connectors.

## Why secondary sources disagree

Different narratives may be dating different events:

- invention/development;
- military/SAGE use;
- Bell internal availability;
- product announcement;
- Bell System tariff/service availability;
- first public commercial order;
- a specific 101A/B/C or 103A revision;
- publication of a technical paper;
- mass use with time-sharing computers.

A sentence like “Bell 103 was released in 1962” cannot be accepted until we know **which one of these events the source means**.

## Variant problem

The archive must not merge:

- 101 family;
- 101A;
- 101B;
- 101C;
- related Bell data-set variants;
- 103 family;
- 103A1;
- 103A2;
- 103F and other documented variants.

Each may differ in terminal service, character-rate assumptions, originate/answer behavior, control hardware and interface arrangements.

## Terminology problem

Early Bell literature often says **data set**, not simply “modem”.

The repository should preserve contemporary terminology because a “data set” can include more than the modulation/demodulation function we casually mean by modem today:

- line interface;
- call control;
- ringing detection;
- answer/originate control;
- data-terminal control signals;
- test functions;
- telephone/data switching.

## Physical interface evidence from the 103A manual

The surviving 103A Bell System Practice identifies a **25-pin business-machine connector** and interface functions including transmitted/received data, clear-to-send, data-set-ready, carrier detect, terminal-ready, ring indication and grounds/power.

That is historically important because it belongs to the genealogy that eventually becomes familiar modem-control wiring in EIA/RS-232 environments.

The exact edition and contemporary EIA revision must be checked against the scan before writing a final interface genealogy.

## Priority primary-source hunt

The chronology should not be marked resolved until we locate, preferably from Bell/AT&T archival material:

1. original Bell 101-family announcement;
2. original Bell 103-family announcement;
3. first-edition Bell System Practice for each family;
4. Bell System tariff/DATA-PHONE service documents;
5. Laurance A. Weber's 1959 paper on frequency-modulation data transmission;
6. R. O. Soffel and E. G. Spack's 1959 *SAGE Data Terminals* paper;
7. Bell Laboratories product catalogs/price lists around 1958–1963;
8. first-edition 101A/B/C and 103A/F interface documents;
9. surviving hardware labels/serial plates with dated provenance.

## Working conclusion

It is safe at present to say:

- Bell Labs modem/data-set work grew from mid-century digital communication and SAGE-era requirements;
- **1958 is a well-attested Bell 101-family historical milestone**;
- 101C and 103A have surviving Bell System Practices that expose much more detailed hardware/service history;
- a Bell System marketing artifact now proves that **Data Set 103-A was publicly marketed by March 1963**, but does not establish its first announcement or first deployment;
- the March 1963 brochure's **200 bit/s** ceiling conflicts with later 300 bit/s technical documentation and therefore exposes a still-unresolved product/revision boundary;
- the exact first-announcement chronology and revision genealogy still require additional primary-document resolution.

It is **not** yet safe for this repository to pretend that one neat sentence has resolved every Bell 101/103 date.

## Research status

**Priority / unresolved chronology.**

This file should be updated as soon as original Bell announcement, tariff or first-edition practice documents are recovered.