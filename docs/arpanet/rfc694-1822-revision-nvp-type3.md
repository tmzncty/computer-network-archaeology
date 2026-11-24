# RFC 694: 1822 revision and uncontrolled packet use, 1974–1975

Follow-up to [RFC 660](rfc660-1974-imp-host-interface-changes.md). Primary source: J. Postel, [RFC 694, Protocol Information](https://www.rfc-editor.org/rfc/rfc694.html), 18 June 1975, pp. 3–5, 11. This is a contemporary status compilation with dated entries, not an IMP release log.

## Evidence batch

| Claim | Locator | Certainty and status | Does not prove |
| --- | --- | --- | --- |
| The eight-message Host-pair window was still described as forthcoming on 31 December 1974 | p. 4, dated entry | High, reported schedule | Exact rollout date or that no experimental installation existed |
| Report 1822 is listed as revised December 1974, NTIS ADA002751; an update is recorded on 6 January 1975 | pp. 3–4 | High, bibliographic and update report | That the two dates represent separate editions |
| Sections 3.3–3.4 incorporated uncontrolled packets; new section 3.7 described their use | p. 4, 6 January entry | High, reported specification revision | Exact encoding or installed software build |
| Pluribus material was added to sections 1, 2, 4, 5 and appendix C | p. 4 | High, documentation | Pluribus installation at any named site |
| An expanded NVP was reported operating between Lincoln and CHI since December 1974; the protocol used IMP message types 0 and 3 | p. 11, 20 January 1975 entry | High for contemporary report; medium-high for actual use of type 3 in this experimental context | Packet trace, precise first type-3 transmission, or use at every NVP site |
| Earlier NVP experiments between ISI and Lincoln were reported for August 1974 | p. 11 | High, reported experiment | That August experiments already used type 3 |

The October notice [RFC 660](https://www.rfc-editor.org/rfc/rfc660.html), section d, described the special path prospectively. RFC 694 now supplies both a reported specification incorporation and an operational application context. These are separate from the eight-message window, which must remain unresolved as to deployment. Host-pair access-control deployment and sequence-pool rollout also remain unverified.

## Candidate relationships

- NVP **uses** 1822 message types 0 and 3 — high, RFC 694 p. 11; implementation/service relationship, not protocol descent.
- December 1974 Report 1822 **revision-of** earlier Report 1822 — high for revision identity, RFC 694 p. 3; exact immediate predecessor edition unknown.
- RFC 660 type-3 proposal **incorporated into** revised 1822 specification — high for property-level documentary continuity, RFC 660 section d and RFC 694 p. 4; no inference of IP/UDP ancestry.

No new machine-readable edge until artifact endpoints and controlled relation types are checked. The NVP report does not establish that NVP caused the type-3 design, nor that all four RFC 660 changes shipped together.

## Source leads

- RFC 694, 18 June 1975, pp. 3–5, 11, linked above.
- BBN Report 1822, revised December 1974, NTIS ADA002751: identified in RFC 694 p. 3; retrieve original before asserting bit-level clauses.
- NVP specification, NSC Note 43: listed in RFC 694 p. 10; retrieve to establish the actual voice packet format and message selection.

Suggested integration: link from the RFC 660 narrative; preserve the dated status distinctions in any future 1822 revision catalog. ROADMAP remains open.
