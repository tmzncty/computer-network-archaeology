# Evidence batch — 2026-11-10 — 1973 IMP/TIP memory retrofit

Status: primary-source claims and boundaries; RFC 476 not yet independently checked. Narrative: `docs/arpanet/imp-tip-1973-memory-retrofit-rfc434-447.md`.

| ID | New claim | Primary locator | Confidence | Explicit exclusion |
| --- | --- | --- | --- | --- |
| MEM73-01 | RFC 434 (1973-01-04) announced retrofit targets IMP 516/316 16K words; TIP 28K; magnetic-tape TIP 32K | RFC 434 p. 1, target table | High (announced) | Not completed-installation counts |
| MEM73-02 | TIP memory expansion necessitates a two-cabinet machine | RFC 434 p. 1, paragraph after table | High (planned configuration) | No chassis or board revision identified |
| MEM73-03 | BBN coordinated retrofits with routine monthly preventive maintenance and warned of longer outages | RFC 434 p. 1, scheduling paragraph | High | Not measured outage durations |
| MEM73-04 | RFC 447 (1973-01-29) explicitly revises RFC 434; CCA moved Mar 20 to Feb 28 | RFC 447 p. 1 opening; p. 2 CCA; RFC 434 p. 2 CCA | High | Not a hardware revision, not a verified installation |
| MEM73-05 | BBN stated that retrofits scheduled before Feb 1 had been completed by Jan 29 | RFC 447 p. 1, opening | High for contemporary completion **statement** | Not independent acceptance evidence |
| MEM73-06 | Remaining schedule names Utah Feb 1, UCSB Feb 6, SRI Mar 7, UCLA Mar 19, Illinois Apr 18 | RFC 447 pp. 1–2 | High for plan | Not actual installation dates |
| MEM73-07 | RFC 215 describes 1971 TIP 8K-word constraint; 1973 target is 28K | RFC 215 p. 1 vs RFC 434 p. 1 | High for separately dated statements | No causal proof of protocol fixes |

**Allowed lineage:** `RFC447 revision-of RFC434` (high; explicit). Hardware change: retrofit-target-of IMP/TIP classes (high for intent). **Disallowed:** `memory retrofit caused RFC215 protocol fixes`, `1973 TIP revision-of 1971 TIP software`, or site-specific installed-at edges absent installation evidence.

Source URLs: https://www.rfc-editor.org/rfc/rfc434.html ; https://www.rfc-editor.org/rfc/rfc447.html ; https://www.rfc-editor.org/rfc/rfc215.html . No copyrighted scans mirrored.
