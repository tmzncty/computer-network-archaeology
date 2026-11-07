# Evidence batch — 1971 Terminal IMP implementation limits

Date: 2026-11-07
Scope: TIP host software, terminal multiplexing, NCP/ICP/TELNET implementation versus specification

## Gap check
ROADMAP still leaves TIP terminal access, IMP revisions and ARPANET operational practices open. Main at the start of this batch was commit `c0b68c18d7c21d51dc4a0ae43f7865112196eee2` (merged PR #36, IMPSYS 2500/2505). Repository code search found no RFC 215 or Terminal IMP coverage. Unlike PR #36's general IMP release change control, this batch isolates a documented TIP-specific NCP implementation and its memory-driven exceptions.

## Primary evidence
**A. McKenzie, BBN, RFC 215, NIC #7545, 30 August 1971**, https://www.rfc-editor.org/rfc/rfc215.html ; DOI https://doi.org/10.17487/RFC215.

- **E1 — hardware/software budget (p. 1):** 8K 16-bit words, no bulk buffering, up to 64 terminals, up to 128 simplex connections. **High** (contemporary implementer description). **Not proof:** installed port count or terminal population.
- **E2 — deployed software scope (pp. 1–2):** TIP has client NCP/ICP/TELNET, lacks ICP server/logger, anticipates later data transfer protocol. **High** for described implementation. **Not proof:** future implementation happened.
- **E3 — deliberate non-compliance (pp. 2–6, A.1–7):** conditional ECO/ERP, conditional unsolicited RFC/CLS, bounded CLS wait, ignored RET/GVB, 65,534-bit allocation limit, ignored ICP 32-bit value. **High** for author-described behavior. **Not proof:** all TIP versions or all hosts shared behavior.
- **E4 — physical-to-logical mapping (p. 7, B.4):** terminal multiplexer device address 0–63 maps into high 16 socket-number bits; low bits usually 2/3. **High**. **Not proof:** terminal multiplexer vendor/model or later persistence.
- **E5 — delivery forecast (p. 1):** six TIPs expected by early December 1971 and subsequent rate ~one/month. **High** for *forecast*, **unknown** for realized deployment.

## Proposed relationship claims
1. TIP implementation -> NCP/ICP/TELNET with documented deviations; **high**, RFC 215 pp. 1–7; conformance/exception, not software ancestry.
2. TIP socket identifier -> terminal multiplexer physical address; **high**, p. 7 B.4; property mapping, not a vendor-lineage edge.
3. Memory constraint -> documented implementation choices; **high as author-stated design rationale**, pp. 1–6; not independently measured causation.
4. RFC 210 -> TIP protocol behavior; **unsupported**, do not record.
5. IMPSYS 2505 -> TIP binary/software derivation; **unsupported**, do not record.

## Suggested repository locations
- Added narrative: `docs/arpanet/tip-rfc215-memory-protocol-exceptions.md`
- Added batch: `data/batches/2026-11-07-tip-rfc215-implementation.md`
- No `data/lineage-ledger.csv` row until an allowed relationship type and a documented actual descent are established.

## Open targets
TIP program listing/release identifiers, delivered site configurations and actual terminal-multiplexer model, and later RFC/BBN change notices documenting correction or persistence of the seven exceptions. Do not transform forecasts into installation dates.
