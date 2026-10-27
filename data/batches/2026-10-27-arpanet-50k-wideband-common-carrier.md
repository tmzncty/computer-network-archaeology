# Research batch — ARPANET 50 kbps wideband common-carrier context

Date: 2026-10-27
Scope: early ARPANET physical circuits; Bell System wideband data service; 303-type data stations

## New evidence

### E1 — BBN identifies the initial network links as 50-kilobit common-carrier circuits

**Source:** F. E. Heart, R. E. Kahn, S. M. Ornstein, W. R. Crowther, D. C. Walden, “The Interface Message Processor for the ARPA Computer Network,” *AFIPS Spring Joint Computer Conference*, 5–7 May 1970, pp. 551–567.

**Locator:** https://doi.org/10.1145/1476936.1477021

**Finding:** BBN describes the initial ARPA Network as interconnecting sites with 50-kilobit common-carrier circuits; provision of those circuits and associated modems is part of subnet implementation.

**Certainty:** high.

**Supports:** 50 kbps as an inter-IMP/common-carrier circuit property.

**Does not prove:** exact modem/data-station model at any individual 1969 site; host-to-IMP rate; underlying carrier plant type on every route.

### E2 — Western Electric 303-type data stations provide 50 kbps over a group facility

**Source:** Western Electric, *Wideband Data: 303-Type Wideband Data Stations — Technical Reference*, August 1966.

**Locator:** https://bitsavers.trailing-edge.com/communications/westernElectric/modems/303_Wideband_Data_Stations_Technical_Reference_Aug66.pdf

**Finding:** standard 303-type equipment supports 50 kbit/s synchronous operation over a “group” channel; the manual says the group channel uses the bandwidth of 12 voice circuits. It separately gives 19.2 kbps half-group and 230.4 kbps supergroup modes.

**Certainty:** high.

**Supports:** a pre-ARPANET Bell/Western Electric service/equipment family matching the documented 50-kbit/s common-carrier requirement.

**Does not prove:** that a specific 303 variant was installed at UCLA, SRI, UCSB, or Utah.

### E3 — Bell engineering literature identifies the 50 kbps group service as analog-carrier adaptation

**Source:** J. J. Mahoney, “Transmission Plan for General Purpose Wideband Services,” *IEEE Transactions on Communication Technology* 14(5), 1966, 641–648, DOI 10.1109/TCOM.1966.1089388.

**Locator:** https://doi.org/10.1109/TCOM.1966.1089388

**Finding:** the transmission plan for type 303 wideband data stations explicitly admits frequency-division analog facilities and focuses on 50 kb/s service in the 48-kc/s bandwidth ordinarily assigned to 12 telephone channels.

**Certainty:** high for the Bell service architecture.

**Supports:** distinguishing this 1960s wideband data context from later 56-kbit/s DDS/DS0 service.

**Does not prove:** the precise physical route or carrier system used for every ARPANET circuit.

## Suggested repository placement

Added narrative:

- `docs/arpanet/arpanet-50k-wideband-common-carrier.md`

Related ROADMAP items:

- `50 kbit/s leased circuits`
- `modems/data sets used on early ARPANET lines`

## Lineage / relation assessment

- `303-type 50-kbps-mode uses group-facility` — **high certainty**.
- `group-facility bandwidth-equivalent-to 12-voice-circuits` — **high certainty**.
- `ARPANET initial inter-IMP service has-rate 50-kbit/s` — **high certainty**.
- `303-type wideband service contextual-predecessor/service-family for ARPANET 50-kbps carrier links` — **medium certainty**. The technical/service match is strong, but this batch lacks site-specific procurement or installation evidence.

Do **not** encode `ARPANET implemented-by 303-type` as a high-certainty edge yet. Matching rate and chronology are insufficient to prove installed hardware identity.

## Negative evidence boundary

This batch does not establish the exact data-station model/revision at the first four ARPANET sites, tariff/order numbers, first-service dates, or uniformity of physical plant. It also does not justify describing the 1969 50-kbit/s circuits as 56-kbit/s DDS/DS0 links or as ordinary voice-band modem connections.

## Next evidence target

Search BBN procurement records, ARPA circuit orders, Bell installation records, and UCLA/SRI/UCSB/Utah site documentation for explicit data-station/model identifiers. That is the evidence needed to convert the carrier-family match into a site-specific `implemented-by` relation.
