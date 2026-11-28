# NVP: NSC Note 68 and RFC 741

Follow-up to [RFC 694 evidence](rfc694-1822-revision-nvp-type3.md). Primary source: Danny Cohen, ISI, [RFC 741](https://www.rfc-editor.org/rfc/rfc741.html), cover, acknowledgments, §§1–2. The cover dates NSC Note 68 to 29 January 1976; the RFC header dates publication to 22 November 1977. These are distinct documentary dates.

## Claim-level evidence

| Fact | Locator | Certainty | Does not establish |
|---|---|---|---|
| Note 68 revises NSC Notes 26, 40 and 43 | Cover | High, explicit revision statement | Immediate sequential order or individual clause deltas |
| Cohen dates initial NVP implementation to December 1973 | Acknowledgments | High for participant report | First intersite call or type-3 use in 1973 |
| ISI used PDP-11/45 and SPS-41; Lincoln used TX2/FDP and PDP-11/45/LDVT; Culler-Harrison used MP32A/AP-90; SRI used PDP-11/40/SPS-41 | Acknowledgments | Medium-high, participant operational report | Exact installation dates, hardware revisions or simultaneous operation |
| Control uses 1822 type 0/0; speech data may use 0/0 or 0/3 | §1 | High, specification | Every implementation selected uncontrolled service |
| 12-bit message ID divided into 8-bit link and 4-bit sublink | §2 | High, specification | IP port semantics |
| Initial contact on octal link 377; two directional control links and two adjacent data links, control link numbers octal 340–375 | §2 | High, specification | Actual trace or universal implementation |

## Engineering context

Cohen identifies ordinary ARPANET host-to-host service as unsuitable for interactive speech. The design separates signaling from media and avoids end-to-end retransmission. This is an explicitly documented design motivation, not a retrospective analogy to UDP. The hardware inventory shows interoperability across different computing and speech-processing equipment, not a single standardized terminal.

## Candidate lineage and integration

- NSC Note 68 **revision-of** NSC Notes 26, 40, 43: three high-certainty documentary edges, cover. Do not infer a chain among the three earlier notes.
- RFC 741 **documents** NSC Note 68: high, cover/header; do not treat RFC publication as a new implementation release.
- NVP **uses** BBN 1822 message services: high, §1; property-level refinement of RFC 694 evidence.
- NVP **implemented-on** the listed configurations: medium-high, acknowledgments; dates and revisions unresolved.

No formal machine-readable edges until endpoints and vocabulary are registered. No direct UDP/RTP descent established here. Earlier NSC notes remain retrieval targets. Suggested cross-link from RFC 694 narrative and future host-software catalog; leave ROADMAP open.
