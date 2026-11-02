# Data Governance and 4-Layer Provenance Policy

**Maintainer:** Daviante (`https://daviante.org`)  
**Contact:** `code@daviante.org`

This document defines the authoritative open upstream sources, compilation methodology, validation controls, and correction procedures for datasets published in `daviante-org/dgip-data`.

---

## 1. Authoritative Open Upstream Sources (25 Feeds Across 4 Layers)

DGIP compiles all IP geolocation, Autonomous System, RPKI route validity, and security/threat tables directly from primary Internet number registries, public BGP route collectors, RPKI validators, first-party network operator geofeeds, and open threat feeds. No commercial geolocation brokers or opaque scraper repositories are used.

### 1.1 Layer 1 — RIR Country Allocations & RIPE RIS BGP
- **NRO Extended Delegation Statistics**: **ARIN**, **RIPE NCC**, **APNIC**, **LACNIC**, and **AFRINIC** (`allocated` and `assigned` IPv4/IPv6 delegations, with automatic RIPE NCC NRO mirror fallback if an origin server stalls).
- **Global BGP Routing & AS Names**: **RIPE NCC Routing Information Service (RIS)** (`riswhoisdump.IPv4.gz`, `riswhoisdump.IPv6.gz`) and **RIPE NCC** registered AS names (`asn.txt`).

### 1.2 Layer 2 — Sub-National & Cloud Regional Geofeeds (`RFC 8805`)
- **Amazon Web Services (AWS)** (`https://ip-ranges.amazonaws.com/geo-ip-feed.csv`)
- **Google Cloud Platform (GCP)** (`https://www.gstatic.com/ipranges/cloud.json`)
- **Oracle Cloud Infrastructure (OCI)** (`https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json`)
- **DigitalOcean** (`https://digitalocean.com/geo/google.csv`)
- **Akamai Connected Cloud / Linode** (`https://geoip.linode.com/`)
- **Vultr / Constant** (`https://geofeed.constant.com/`)
- **Apple iCloud Private Relay** (`https://mask-api.icloud.com/egress-ip-ranges.csv`)

### 1.3 Layer 3 — Cryptographic RPKI ROV & AS Classification
- **OpenBSD `rpki-client` Public Console** (`https://console.rpki-client.org/vrps.csv`) — Validated ROA Payloads across all 5 RIR Trust Anchors (`RFC 6811` & `RFC 7607`).
- **bgp.tools AS Classifications** (`https://bgp.tools/asns.csv`) — Global AS role taxonomy (`isp`, `hosting`, `cdn`, `transit`, `content`, `education`, `government`, `business`).

### 1.4 Layer 4 — Cloud, CDN, Tor Exit, Privacy Relay & Threat Feeds
- **Edge CDNs & Developer Platforms**: **Cloudflare** (`ips-v4`, `ips-v6`), **Fastly** (`public-ip-list`), and **GitHub** (`api.github.com/meta`).
- **Anonymity Networks**: **Tor Project Bulk Exit List** (`check.torproject.org/torbulkexitlist`) and **Apple iCloud Private Relay**.
- **Open Threat & Abuse Intelligence**: **Spamhaus DROP (`IPv4` & `IPv6`)** and **Abuse.ch Feodo Tracker Botnet C2s**.

---

## 2. Compilation and Normalization Rules

1. **Special-Purpose Address Exclusion (RFC 6890)**: Loopback, private-use (RFC 1918 / RFC 4193), link-local, documentation, multicast, carrier-grade NAT (RFC 6598), and reserved ranges are stripped from all public tables during compilation and classified explicitly as bogon space at query time.
2. **Cryptographic RPKI Filtering & BGP Hygiene**: Announcements with fewer than `5` RIS BGP peers, default/supernet leaks (`< /8` IPv4, `< /12` IPv6), private/reserved ASNs, and BGP hijacks failing cryptographic RPKI Route Origin Validation (`invalid`) are filtered out before interval flattening.
3. **Geofeed Priority Overlay**: Layer 2 physical regional feeds (`geo_source = "geofeed"`) are overlaid onto Layer 1 RIR headquarters allocations (`geo_source = "rir"`) so cloud regions and operator POPs resolve to their physical country, ISO 3166-2 subdivision, and city.
4. **Multi-Label Security Sweep-Line**: Overlapping infrastructure and threat intervals are combined via a coordinate sweep-line so every applicable boolean flag (`is_cloud`, `is_datacenter`, `is_cdn`, `is_tor_exit`, `is_privacy_relay`, `is_threat`), highest-specificity `provider`, and sorted `threat_feeds` list are preserved without loss.
5. **Canonical Formatting**: IPv6 addresses follow **RFC 5952**; ASNs follow **RFC 6793**; country and region codes follow **ISO 3166-1 alpha-2** and **ISO 3166-2**.

---

## 3. Release Cadence and Change Gating

- **Live API Synchronization**: `https://dgip.daviante.org` refreshes its active lookup tables every 24 hours against the upstream endpoints using atomic Blue/Green table swaps.
- **Weekly Snapshot Releases (`vYYYY.Www`)**: Official immutable snapshot archives are cut weekly (Mondays in UTC) using ISO-8601 week numbering. If normalized upstream outputs are identical to the previous weekly release, duplicate releases are skipped automatically.

---

## 4. Correction Policy for Network Operators

Daviante does not maintain manual per-IP geolocation override lists in `dgip-data`. Network operators wishing to update country, sub-national location, or ASN metadata for their prefixes should:
1. Update the `country:` and `geofeed:` (`RFC 9092` / `RFC 8805`) attributes on the relevant `inetnum` / `inet6num` / `NetRange` object in their authoritative RIR database (ARIN, RIPE, APNIC, LACNIC, or AFRINIC).
2. Ensure intended origin ASNs are announced consistently in global BGP routing tables with matching **RPKI ROAs**.

Once reflected in upstream publications, updates propagate automatically in the next synchronization and weekly release cycle. Technical defects in the DGIP compiler may be reported via GitHub Issues on `daviante-org/dgip` or to `code@daviante.org`.
