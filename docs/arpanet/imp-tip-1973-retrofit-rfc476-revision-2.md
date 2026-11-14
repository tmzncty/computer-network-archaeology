# RFC 476: March 1973 IMP/TIP retrofit status and schedule revision 2

## Coverage boundary

This is a focused continuation of [the RFC 434/447 retrofit record](imp-tip-1973-memory-retrofit-rfc434-447.md), not a second account of the 16K/28K/32K memory targets. The earlier record explicitly left RFC 476 unexamined. On the inspected main branch (commit `4f1101b5`, merged PR #38), no RFC 476-specific narrative existed.

## Primary document

Alexander McKenzie, BBN-NET, **RFC 476 / NIC 14920**, *IMP/TIP Memory Retrofit Schedule (Revision 2)*, **7 March 1973**, pp. 1–2: https://www.rfc-editor.org/rfc/rfc476.html (DOI https://doi.org/10.17487/RFC476). Compare [RFC 447](https://www.rfc-editor.org/rfc/rfc447.html), 29 January 1973, pp. 1–2, and [RFC 434](https://www.rfc-editor.org/rfc/rfc434.html), 4 January 1973, pp. 1–2.

## Newly recovered differences

RFC 476 p. 1 explicitly calls itself a revision of **RFC 447**. It reports two categories of changes: **completed** retrofits at **Utah, Belvoir, NOAA, USC, Stanford, ISI, Case, CCA**, which are removed from the outstanding schedule; and **rescheduling** of **UCSB, ETAC, Aberdeen, Rome**. This is BBN's contemporaneous status report, not independent site acceptance documentation.

| Site | RFC 447 scheduled | RFC 476 remaining schedule | Status evidenced by RFC 476 | Locator |
| --- | --- | --- | --- | --- |
| Utah | Feb 1 | omitted | Reported completed | RFC 476 p. 1 opening; RFC 447 p. 1 |
| Belvoir | Feb 8 | omitted | Reported completed | same |
| NOAA | Feb 12 | omitted | Reported completed | same |
| USC | Feb 13 | omitted | Reported completed | same |
| Stanford | Feb 14 | omitted | Reported completed | same |
| ISI | Feb 22 | omitted | Reported completed | RFC 476 p. 1 opening; RFC 447 p. 2 |
| Case | Feb 26 | omitted | Reported completed | same |
| CCA | Feb 28 | omitted | Reported completed | same |
| UCSB | Feb 6 | **May 1** | Rescheduled; not completed | RFC 476 p. 2; RFC 447 p. 1 |
| ETAC | Feb 15 | **Mar 15** | Rescheduled; not completed | RFC 476 p. 1; RFC 447 p. 2 |
| Aberdeen | Feb 22 | **postponed indefinitely** | No new installation date | RFC 476 p. 2; RFC 447 p. 2 |
| Rome | Mar 14 | **Mar 16** | Rescheduled; not completed | RFC 476 p. 1; RFC 447 p. 2 |

RFC 476 pp. 1–2 retains the outstanding schedule for SRI (Mar 7), FNWC (Mar 15), UCLA (Mar 19), AMES IMP (Mar 21), GWC (Mar 22), Carnegie (Apr 4), SDC (Apr 17), and Illinois (Apr 18). **SRI appearing on the same date as publication does not prove it was completed on that date.** The document also repeats the original machine-class memory targets, TIP two-cabinet requirement and monthly preventive-maintenance scheduling; these are *not* new specifications introduced by revision 2.

## Lineage and confidence

- **`RFC 476 revision-of RFC 447` — high**: RFC 476 p. 1 expressly states it changes RFC 447, and its title identifies revision 2. This is a **schedule-document** edge, not a hardware revision or software ancestry edge.
- **`RFC 447 revision-of RFC 434` — high**, already documented in the prior research; do not duplicate as a new discovery.
- **`March-1973 BBN status-report marks eight named site retrofits completed` — high for the *report*, medium for independently established physical completion**: RFC 476 p. 1 provides explicit site names, but no field acceptance sheets or hardware serials.
- **`UCSB/ETAC/Aberdeen/Rome schedule superseded` — high** for dated planning changes, not installation outcomes.

No `derived-from`, `implemented-by` or site-specific hardware-revision edges are justified by this source.

## What the evidence does not establish

1. The eight completed sites' **actual completion dates**, board part numbers, machine serial numbers, or installed memory test results. Removal from a schedule is paired with a completion assertion, not an acceptance record.
2. That the four rescheduled sites were upgraded on their **new** dates; Aberdeen has no new date at all.
3. Why the four dates changed (equipment supply, physical space, staffing, faults or carrier arrangements are not specified).
4. That every IMP/TIP already possessed the target memory by 7 March, or that the tape option existed at any particular site.
5. That TIP's 1971 NCP/ICP exceptions (RFC 215) were fixed by the memory retrofit. The RFCs contain no such software conformance evidence.
6. That the 1973 status changes imply a hardware or protocol **lineage** beyond the explicitly revised operational schedule.

## Next evidence targets

Find a subsequent BBN retrofit completion circular or station maintenance/acceptance record for **UCSB (May 1)** and **Aberdeen (indefinitely postponed)**, and Honeywell/BBN parts lists for the TIP's second cabinet. Keep reported completion, planned date and observed physical configuration as separate fields.
