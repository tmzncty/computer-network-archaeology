# Evidence batch — RFC 660 / 1974 IMP–Host interface change notice

**Reviewed:** 2026-11-21. **Primary:** D. Walden, RFC 660, October 1974, NIC 31202, https://www.rfc-editor.org/rfc/rfc660.html. **Status:** proposed near-term changes; no release/deployment confirmation.

| ID | Claim | Exact locator | Confidence / status | Does not prove |
| --- | --- | --- | --- | --- |
| R660-01 | Four outstanding messages per IMP pair, shared among Host pairs, reported as practice since 1972 | p. 1, a | high / contemporary retrospective statement | Exact 1972 introduction date or version |
| R660-02 | Separate dynamically pooled message sequences per Host pair planned; pool exhaustion time-multiplexes traffic | p. 1, a | high / proposed | Field installation or no performance penalty |
| R660-03 | ARPA-requested Host-pair permission check after two-minute inactivity; denial via Destination Dead sub-code 3; initially allow-all | p. 1, b | high / proposed | Actual blocklists, denied Hosts, or enforcement date |
| R660-04 | Per-Host-pair outstanding window planned 4 to 8 | p. 2, c | high / proposed | Throughput doubling in practice |
| R660-05 | Type-3 single-packet Host–IMP path bypasses ordered/reliable mechanism; multipacket type 3 discarded | p. 2, d(i–iv) | high / proposed | Implementation at any site or lineage to IP |
| R660-06 | Resource-starved type-3 packets may be dropped; NCC to regulate authorized Hosts | p. 2, d(v–vi) and final paragraph | high / proposed | Specific experiments, users, or drop measurements |
| R660-07 | RFC to be filed with Report 1822 until updated | p. 2, closing | high / document relationship | A new 1822 edition was published |

**Suggested records:** `docs/arpanet/rfc660-1974-imp-host-interface-changes.md` (narrative); this evidence batch. **Candidate edge:** `RFC-660 --announces-interface-amendments-to--> BBN-Report-1822` (high, documentary relation only). **Do not create:** `RFC-660 --caused--> IP/UDP` or `type-3 --deployed-at--> [site]` without new sources.

**Follow-up:** locate contemporary IMPSYS change logs and subsequent Report 1822 editions to verify deployment and field encodings.
