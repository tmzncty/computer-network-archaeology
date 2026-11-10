# 1973 IMP/TIP core-memory retrofit: machine classes, cabinets, and dated rollout revisions

## Scope

The ROADMAP still lists IMP revisions, TIP terminal access, hardware catalogs and ARPANET operational procedures as open. Earlier research covers the **1971 TIP 8K-word memory constraint** (RFC 215) and its protocol consequences. This note documents a **different, explicitly dated 1973 network-wide hardware retrofit plan** rather than treating a later memory configuration as an original TIP property.

The source is a contemporary BBN operational announcement series by Alexander A. McKenzie: [RFC 434](https://www.rfc-editor.org/rfc/rfc434.html), **4 January 1973**, NIC 13658, and [RFC 447](https://www.rfc-editor.org/rfc/rfc447.html), **29 January 1973**, NIC 14104, explicitly titled revision 1 and marked as updating RFC 434.

## Primary evidence and locators

| Claim | Source and exact locator | Certainty |
| --- | --- | --- |
| BBN announced a program to add core memory to **each IMP and TIP** in the first months of 1973 | RFC 434 p. 1, opening paragraph; RFC 447 p. 1 | High: **announced plan**, not verified completion |
| Target memory: **IMP (Honeywell 516 or 316) 16K words**, **TIP 28K words**, **TIP with magnetic tape option 32K words** | RFC 434 p. 1, three-item table; repeated RFC 447 p. 1 | High for stated targets; not an inventory of installed memory |
| TIP expansion would require **two cabinets** | RFC 434 p. 1, immediately following memory table; RFC 447 p. 1 | High for planned physical consequence; no cabinet part number |
| Retrofit scheduling was coordinated with **monthly preventive maintenance**, but could lengthen downtime | RFC 434 p. 1, paragraph preceding site schedule; RFC 447 p. 1 | High for stated operational practice |
| **CCA** moved from **March 20** to **February 28** | RFC 434 p. 2, CCA (3/20); RFC 447 p. 1 explanatory paragraph and p. 2 CCA (2/28) | High for explicit schedule revision; **not proof work was done Feb 28** |
| By Jan 29, RFC 447 says all retrofits scheduled **before February 1** had been completed and were removed from the revised schedule | RFC 447 p. 1, first paragraph | High for BBN's contemporaneous **completion report**; site-by-site acceptance logs absent |
| Revised remaining-site list included Utah Feb 1, UCSB Feb 6, SRI Mar 7, UCLA Mar 19, and Illinois Apr 18 | RFC 447 pp. 1–2, dated site list | High for schedule only |

## Interpretation and bounded lineage

**Direct documentary revision edge:** `RFC 447 revision-of / updates RFC 434` — **high**, explicitly labelled revision 1 and `Updates: 434` on RFC 447 p. 1. This is a **document/schedule** revision, not a machine hardware revision.

**Machine-configuration edge:** `1973 IMP/TIP memory retrofit planned-target-configurations {IMP 16K, TIP 28K, tape TIP 32K}` — **high** as a planned hardware modification; individual sites require dated installation or acceptance evidence to assert actual deployment.

**Operational edge:** `1973 retrofit scheduled-with monthly preventive maintenance` — **high** as an explicitly stated coordination practice, not proof that downtime was minimized.

**Connection to 1971 TIP:** RFC 215 (30 Aug 1971) describes 8K 16-bit words total in the then-described TIP implementation. RFC 434/447 show a later planned 28K-word TIP configuration. This supports **a change in stated memory configuration over time**, not a demonstrated causal claim that the RFC 215 NCP/ICP exceptions were fixed by the 1973 retrofit. Neither RFC 434 nor 447 provides a TIP software release, a post-retrofit conformance test, a motherboard revision, or an implementation listing. The two sources also do not establish that every 1971 TIP was identical to every 1973 TIP.

## What this evidence does NOT prove

- The proposed targets were installed at every site or on the exact scheduled dates.
- All 1973 IMPs and TIPs had identical boards, memory modules, cabinet configurations or software.
- The extra memory caused any particular NCP/TELNET behavior change, or resolved RFC 215's seven exception classes.
- The magnetic-tape option was present at every TIP, or that a 32K-word tape TIP was installed at any specific named site.
- CCA's rescheduling indicates a technical fault, procurement delay or other cause: RFC 447 supplies **no reason**.
- The 1973 target configurations describe original 1969 IMP or original 1971 TIP hardware.

## Next archival checks

1. Read [RFC 476](https://www.rfc-editor.org/rfc/rfc476.html), titled *IMP/TIP memory retrofit schedule (rev 2)*, and compare its site dates and completion claims to RFC 447 before recording further deployments.
2. Seek BBN installation/acceptance reports, Honeywell 316/516 memory option documentation, site photographs and preventive-maintenance logs to identify actual installed memory boards and the two-cabinet TIP physical revision.
3. Compare subsequent TIP software release notes against RFC 215 to test whether memory growth actually changed protocol behavior. Do **not** infer a software lineage from the retrofit chronology alone.

## Source records

- Alexander A. McKenzie (BBN-NET), *IMP/TIP Memory Retrofit Schedule*, RFC 434 / NIC 13658, 4 Jan 1973, pp. 1–2. https://www.rfc-editor.org/rfc/rfc434.html ; https://doi.org/10.17487/RFC434.
- Alexander A. McKenzie (BBN-NET), *IMP/TIP Memory Retrofit Schedule (Revision 1)*, RFC 447 / NIC 14104, 29 Jan 1973, pp. 1–2. https://www.rfc-editor.org/rfc/rfc447.html ; https://doi.org/10.17487/RFC447.
- A. McKenzie, *NCP, ICP, and TELNET: The Terminal IMP Implementation*, RFC 215, 30 Aug 1971, p. 1 (earlier 8K TIP context only). https://www.rfc-editor.org/rfc/rfc215.html.
