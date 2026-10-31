# Research batch — direct Bell 303 evidence for ARPANET

Date: 2026-10-31
Scope: early ARPANET modem identity; Bell 303; later operational corroboration

## Why this batch exists

The 2026-10-27 batch established a strong rate/service-family match between the ARPANET's documented 50-kbit/s common-carrier circuits and Western Electric's 303-type wideband data system, but deliberately stopped short of asserting that the original ARPANET actually selected Bell 303 equipment. This batch adds evidence that crosses that boundary while preserving the unresolved site/revision questions.

## New evidence

### E1 — Robert Kahn directly identifies Bell 303 as mandated in the original ARPANET design

**Source:** Robert E. Kahn, oral history interviewed by Vinton Cerf, Computer History Museum, recorded 30 September 2006, CHM reference X3699.2007.

**Locator:** p. 24; https://archive.computerhistory.org/resources/access/text/2012/04/102657973-05-01-acc.pdf

**Finding:** Kahn states that during the original ARPANET design “it had been mandated that we use Bell 303 modems,” and identifies them as 50-kilobit Bell System equipment. He describes visiting Bell Labs to understand the 303 and finding a higher-capacity Bell 304 prototype that Bell would not release as a product.

**Certainty:** medium-high for original-design modem-family selection. This is direct testimony by a BBN IMP-team participant, but it was recorded 37 years later and is not a surviving 1969 procurement record.

**Supports:** upgrading `Bell-303 compatible-with ARPANET-50k-service` from a rate/service inference to `original-ARPANET-design specifies/mandates Bell-303`, with a retrospective-source qualifier.

**Does not prove:** which organization/person imposed the mandate; exact Bell 303 subtype/revision; serial numbers; exact first-four-node installation inventory; tariff/order identifiers.

### E2 — Kahn's Bell 304 account is explicit negative deployment evidence

**Source:** same oral history, p. 24.

**Finding:** Kahn says Bell Labs had a working Bell 304 capable of substantially greater capacity over the same channel bandwidth, but Bell would not release it because it was not a market product.

**Certainty:** medium-high as participant recollection.

**Supports:** a negative boundary against converting technical availability or superiority into deployment lineage.

**Does not prove:** full Bell 304 technical specification, whether any other external experiment obtained a 304, or the precise institutional decision trail.

### E3 — Department of Commerce documents Bell 303 in an operational ARPANET/TIP installation

**Source:** Judd A. Payne, *ARPANET Host to Host Access and Disengagement Measurements*, NTIA Report 78-3, U.S. Department of Commerce, May 1978.

**Locator:** section 3 and figure 4, pp. 11–13; https://www.govinfo.gov/content/pkg/GOVPUB-C60-PURL-gpo5575/pdf/GOVPUB-C60-PURL-gpo5575.pdf

**Finding:** the NTIA/ITS PDP-11 host-to-DOCB TIP VDH configuration explicitly uses Bell 303 modems at both ends. Figure 4 also labels Bell 303 modems on the TIP's 50-kbit/s inter-node connections. The report states that the VDH special interfaces plug directly into Bell 303 modems and that the local pair is connected over nearly 1,800 feet of shielded twisted-pair cable inside the Radio Building.

**Certainty:** high for the documented Boulder installation and its Bell 303 interface identity.

**Supports:** `DOCB-TIP/NTIA-VDH implemented-with Bell-303`; operational continuity of Bell 303 interfaces in the ARPANET environment into the late 1970s.

**Does not prove:** that the Boulder configuration was identical to UCLA/SRI/UCSB/Utah in 1969; exact subtype/revision; that the local VDH cable and inter-IMP common-carrier facilities were the same physical service.

## Relation / lineage assessment

- `original-ARPANET-design specifies/mandates Bell-303` — **medium-high certainty**; direct participant testimony, retrospective source.
- `DOCB-TIP/NTIA-VDH implemented-with Bell-303` — **high certainty**; explicit federal operational report.
- `Bell-303 is original-ARPANET modem family` — **medium-high certainty** when E1 is combined with the 1966 Western Electric 303 technical reference and 1970 BBN 50-kbit common-carrier description.
- `Bell-304 deployed-on ARPANET` — **negative / contradicted by this evidence**; Kahn recalls that Bell would not release it.
- `UCLA/SRI/UCSB/Utah 1969 endpoint implemented-by Bell-303-[specific variant]` — **not yet established**.

No causal edge should be inferred from Bell 303 predating ARPANET. The evidence supports selection/implementation relations, not a claim that the modem caused packet switching or the ARPANET architecture.

## Repository changes

Updated:

- `docs/arpanet/arpanet-50k-wideband-common-carrier.md`

Added:

- `data/batches/2026-10-31-arpanet-bell-303-direct-evidence.md`

Related ROADMAP items:

- `50 kbit/s leased circuits`
- `modems/data sets used on early ARPANET lines`

## Negative evidence boundary

This batch does not establish the exact 1969 Bell 303 subtype, revision, serial number, procurement order, tariff, site-by-site physical plant, or who issued the design mandate. It does not prove that every ARPANET 50-kbit/s circuit was physically identical. It also does not turn the Bell 304 prototype into a lineage predecessor deployed on ARPANET; the participant account explicitly says it was not made available.

## Next evidence target

Search 1968–1969 BBN/ARPA specifications and procurement records, Bell circuit orders, acceptance records, installation drawings, and first-four-node site documentation for explicit 303 subtype/assembly identifiers. The remaining question is no longer whether Bell 303 belonged to the original design, but **which 303 hardware was actually installed at each first-four-node endpoint and under what order/service arrangement**.
