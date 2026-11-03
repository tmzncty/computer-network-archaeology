# Research batch — IMPSYS 2500/2505 change control and NCC reporting

Date: 2026-11-03
Scope: ARPANET IMP software versions; Host–IMP interface assumptions; operational change notification; NCC telemetry

## Why this batch exists

Existing repository coverage reconstructs BBN 1822 physical behavior and later 1972 timing/documentation corrections. This batch fills an earlier operational gap: a June 1971 IMP software deployment that broke NCPs relying on undocumented timing, followed by explicit BBN change notices and stronger NCC-oriented statistics/reporting.

## E1 — IMPSYS 2500 deployment exposed undocumented Host assumptions

**Source:** Bernie Cosell, BBN, RFC 209, *Host/IMP Interface Documentation*, 13 August 1971.

**Locator:** page 1 / complete RFC; https://www.rfc-editor.org/rfc/rfc209.html

**Facts:**
- BBN put IMP system Version 2500 into the network on 25 June 1971.
- A fix for spurious `Destination Dead` messages caused the IMP to refuse Host-originated messages for about 30 seconds after Host-up indication.
- A number of NCPs had imposed their own upper limit on IMP acceptance time; they therefore declared the IMP down and shut themselves down.
- BBN says it believed no advertised property had changed.
- BBN asks implementors to rely only on behavior guaranteed by Report 1822 and report discrepancies instead of coding around observations.
- BBN explicitly acknowledges that Report 1822 was not in fact complete/correct, making this a specification-governance response rather than evidence of an already-perfect standard.

**Certainty:** high; contemporary BBN operational notice.

**Does not prove:** affected sites/NCPs; exact Report 1822 revision at each site; that the 30-second behavior was new in every possible sense rather than part of the particular Version 2500 fix described.

## E2 — IMPSYS 2505 expands Host capacity and NCC statistics

**Source:** Bernie Cosell, BBN, RFC 213, *IMP System Change Notification*, 20 August 1971.

**Locator:** complete RFC; https://www.rfc-editor.org/rfc/rfc213.html

**Facts:**
- Version 2505 was installed during the week of 16 August 1971.
- supported Hosts increased from 3 to 4;
- status light 8 monitors Host 4;
- 10-second and snapshot statistics became longer;
- Host-handling routines collected more accurate/voluminous Host usage statistics for the NCC;
- Host round-trip statistic resolution/unit changed from 100 to 800 microseconds.

**Certainty:** high.

**Does not prove:** every IMP immediately had four populated Host interfaces; complete internal delta; absence of intervening software versions.

## E3 — binary status reporting becomes an NCC facility

**Source:** Bernie Cosell, BBN, RFC 218, *Changing the IMP Status Reporting Facility*, 8 September 1971.

**Locator:** complete RFC; https://www.rfc-editor.org/rfc/rfc218.html

**Facts:**
- BBN says the change is intended to expand its NCC role;
- text status reports were to be removed because binary reports sent directly to NCC had already superseded them;
- status reporting on fake host 3 would remain with the statistics program;
- Host `PARAMETER CHANGE` settings would no longer affect those reports, to prevent Hosts from interfering with NCC operation.

**Certainty:** high.

**Does not prove:** complete NCC architecture, telemetry record format, operator procedures, or exact rollout date beyond the stated within-next-month plan for the described change.

## Relation assessment

- `IMPSYS-2505 successor-version-of IMPSYS-2500` — **medium**: chronological/version-line evidence is strong, but these RFCs do not enumerate intervening builds or explicitly say direct derivation.
- `IMPSYS-2505 reports-statistics-to NCC` — **high**.
- `IMP-binary-status-reporting feeds NCC` — **high**.
- `IMPSYS-2500 incident caused NCC centralization` — **unsupported**; do not create.
- `Version-2500 timing behavior is guaranteed-by Report-1822` — **unsupported/contradicted by BBN's framing**; the point of RFC 209 is that Host implementations had depended on behavior BBN did not regard as advertised.

## Repository changes

Added:
- `docs/arpanet/impsys-2500-2505-change-control.md`
- `data/batches/2026-11-03-impsys-2500-2505-change-control.md`

Related ROADMAP areas:
- `IMP software architecture`
- `ARPANET operational procedures`
- `Network Measurement Center` / operational monitoring context
- `Host–IMP interface electrical/logical details` (specification/implementation boundary)

## Negative evidence boundary

Do not infer causation from the chronology. In particular, the sources do not say that the June 2500 compatibility incident caused the August 2505 statistics work or September NCC centralization. They also do not justify treating a software-supported fourth Host as proof of a physically installed fourth Host interface at every IMP.

## Next evidence target

Recover the actual IMPSYS 2500/2505 program listings, release memoranda, or BBN technical reports if surviving, and identify which Host NCPs/sites experienced the Version 2500 timeout failure. A second useful target is the binary NCC status-report format and the implementation of fake host 3.
