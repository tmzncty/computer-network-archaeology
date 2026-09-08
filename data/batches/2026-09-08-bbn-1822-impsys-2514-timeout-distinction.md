# Batch: BBN Report 1822 correction vs. IMPSYS 2514 timing — 2026-09-08

This batch advances a revision-specific ARPANET Host–IMP evidence gap already identified by the January 1976 BBN Report 1822 source record: earlier Report 1822 states must not be collapsed into the later revision.

## Research question

How should the January 1972 evidence be reconciled when RFC 270 says a 40-second Report 1822 timeout was a documentation error while RFC 271 says IMPSYS 2513 really did have a delay of slightly over 40 seconds?

## Narrative excavation

- `docs/arpanet/bbn-1822-impsys-2514-timeout-distinction.md`

## Structured sources

- `SRC-0277` — RFC 270, 1 January 1972: Report 1822 page-25/page-26 correction.
- `SRC-0278` — RFC 271, 3 January 1972: IMPSYS 2514 change notification.
- `SRC-0279` — RFC 331, 19 April 1972: later operational lower-bound confirmation for IMPSYS 2514.

`SRC-0271..0276` are left untouched because concurrent open research branches already reserve that range.

## Recovered facts

1. RFC 270 corrects an earlier Report 1822 text: under the stated conditions the Host is not marked dead and the relevant timeout is 30 rather than 40 seconds.
2. RFC 270 explicitly says this is a documentation error, not an IMP-system change.
3. RFC 271 independently records a real IMPSYS 2513 implementation behavior: after a Host came alive, the delay before its IMP accepted a second packet had been increased to slightly over 40 seconds and could ambiguously reach about 75 seconds.
4. IMPSYS 2514 restored that Host-up delay to 30 seconds and removed the ambiguity.
5. RFC 271 explicitly separates the Host queue timeout from the Host-up delay and says those timers are not synchronized; its footnote cites RFC 270 for the queue/interface-clearing behavior.
6. RFC 271 scheduled IMPSYS 2514 field installation for 13 January 1972; this is a schedule, not proof of completed rollout at every site.
7. RFC 331, dated 19 April 1972, calls IMPSYS 2514 the current system, providing a confirmed operational lower bound by that date.
8. The interface behavior was asymmetric during Host startup: the IMP temporarily limited Host-to-IMP acceptance, while the Host was expected to accept network messages immediately.

## Suggested repository interpretation

Attach this revision-specific evidence to the already cataloged:

- `ART-0008` — Host–IMP Interface;
- `ART-0006` — Interface Message Processor.

Do not create a new artifact merely to represent the fact that two existing objects had a corrected documentation state and an implementation-version timing distinction.

## Lineage decision

**No `LIN-*` record is created.**

RFC 270 and RFC 271 were generated together and are chronologically adjacent, but their cross-reference establishes a distinction between timing conditions, not a causal/descent relation between artifacts. Chronology alone is insufficient for lineage.

## Explicit negative claims

This batch does **not** prove:

- that every IMP timer was always 30 seconds;
- that the Report 1822 error and the IMPSYS 2513 Host-up delay describe the same mechanism;
- that IMPSYS 2514 successfully reached every ARPANET IMP during the scheduled 13 January 1972 window;
- the exact first completed deployment timestamp of 2514;
- a complete BBN Report 1822 revision tree from 1969 through 1976;
- that a documentation error caused an implementation change, or vice versa;
- any lineage edge inferred only from publication order.

## Remaining work

- recover dated full Report 1822 revisions or amendment packets surrounding 1969–1975;
- establish page-level concordance between the RFC 270 correction and surviving pre-/post-correction Report 1822 scans;
- recover surviving IMPSYS 2513/2514 listings or release media and compare the relevant timer code if provenance permits;
- recover site-level operational evidence if an exact 2514 cutover chronology is required.

Research and initial drafting: **GPT-5.6 Sol (OpenAI), September 2026**.
