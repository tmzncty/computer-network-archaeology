# RFC 622: 1974 IMP/TIP outage coordination and Very Distant Hosts

## Scope and existing coverage

This excavation follows the 1973 memory-retrofit schedule records (RFCs 434, 447, 476), but examines a **different object**: the March 1974 *operational procedure for scheduling IMP/TIP downtime*. The existing retrofit research establishes that BBN coordinated upgrades with preventive-maintenance windows; it does not document the later multi-organization notification policy. This is not a claim that the 1973 retrofits caused the 1974 policy revision.

## Primary source

Alexander McKenzie (BBN-NET), **RFC 622 / NIC 21995**, *Scheduling IMP/TIP Down Time*, **13 March 1974**, pp. 1–3, https://www.rfc-editor.org/rfc/rfc622.html (DOI https://doi.org/10.17487/RFC622). Text was entered into the online archive in October 1999, according to its colophon; distinguish original document date from digitization.

## Documented practice and change

1. **Earlier scheduling authority** (p. 1, opening): for downtime outside scheduled preventive maintenance—examples explicitly include retrofit programs and offline diagnosis/repair of intermittent faults—BBN scheduled with a site's **primary site contact**, treating that person as representative of all attached Hosts and TIP users.
2. **Reason for revisiting the practice** (p. 1, opening): McKenzie explicitly attributes the review to proliferation of **Very Distant Hosts** and complaints from representatives of other local or distant Hosts. This is a contemporaneous *stated reason*, not an independently quantified causal analysis.
3. **New optional notification role** (p. 1, policy paragraph): scheduling **continues** through the primary site contact. Any Host organization can nominate a **secondary contact** for telephone notification; the NCC operators call the secondary contact **after** arranging downtime with the primary. The new role is notification, not an equal veto, approval or rescheduling right.
4. **Registration channels** (p. 1): secondary-contact details can be sent to McKenzie at the BBN Network Control Center by postal mail, the Journal system (ident **AAM**), or network mail (**MCKENZIE at BBN-TENEX**). These are explicit operational workflows, not merely protocol specifications.
5. **Named site contacts** (p. 2): the RFC lists primary and backup contacts for dozens of sites, including distinct **AMES IMP** and **AMES TIP** entries and named contacts for **Aberdeen**, **UCSB**, **London**, **NORSAR**, and **Tymshare**. This list is a dated contact directory; it is not a complete physical-network topology or equipment inventory.

## Relationship to the 1973 retrofit evidence

RFC 434 (4 January 1973), p. 1, states that BBN aimed to coordinate retrofits with monthly preventive maintenance. RFC 622 (13 March 1974), p. 1, explicitly names retrofits among reasons for *additional* downtime and revises who receives notice. This supports **continuity of a maintenance-coordination problem** and a **documented 1974 policy modification**, not the assertion that the 1973 memory project caused the 1974 policy or that any named 1973 site retrofit remained incomplete in 1974.

## Evidence / relationship assessment

| Proposed relationship | Confidence | Primary locator | What it does not prove |
| --- | --- | --- | --- |
| 1974 secondary-contact notification policy **modifies** earlier primary-only coordination practice | **High** (explicit policy revision) | RFC 622 p. 1, opening and policy paragraphs | No formal versioned document or software lineage; no proof every operator complied |
| NCC operators **notify** nominated secondary contacts by telephone after primary scheduling | **High** for documented procedure | RFC 622 p. 1, final paragraph | Not proof of actual calls, uptime or acceptance |
| Proliferation of Very Distant Hosts and complaints **stated-as-motivation-for** policy review | **High for author's statement; medium for historical causal completeness** | RFC 622 p. 1, opening | Not a measured trend, sole cause, or quantified number of VDHs |
| 1973 retrofit scheduling and 1974 downtime policy **share a maintenance coordination context** | **High for documented common practice; no causal edge** | RFC 434 p. 1; RFC 622 p. 1 | Not `RFC434 caused RFC622` or `RFC622 revision-of RFC476` |

The relationship `1974-secondary-contact-policy modifies  pre-1974-primary-contact-only-policy` is a **high-confidence policy/procedure edge** in prose; do not force it into a hardware/software `derived-from` lineage or claim RFC 622 formally revises RFC 476. A future structured edge should first check the repository vocabulary for a policy-revision relation.

## Explicitly unresolved

- No actual secondary-contact registrations, NCC telephone logs, or outage records were recovered.
- The document does not identify individual Very Distant Host circuits, modem models, interfaces, or dates of installation.
- Presence of a site in the p. 2 contact list does not demonstrate an IMP or TIP model, a link speed, or contemporaneous active traffic.
- Aberdeen's presence in the 1974 contact list **does not resolve** whether its 1973 core-memory retrofit, postponed indefinitely in RFC 476, eventually happened.
- No evidence establishes that this policy was adopted by later Internet NOCs; role similarity is not documented inheritance.

## Next evidence targets

Find BBN NCC operator manuals, actual outage notices, Journal messages and VDH installation/service records from 1973–1975. Compare the published contact policy with operational practice and determine whether subsequent documents revised the primary/secondary distinction.

**Sources:** [RFC 622](https://www.rfc-editor.org/rfc/rfc622.html), pp. 1–3; [RFC 434](https://www.rfc-editor.org/rfc/rfc434.html), p. 1; [RFC 476](https://www.rfc-editor.org/rfc/rfc476.html), pp. 1–2 (context only). No full documents reproduced.
