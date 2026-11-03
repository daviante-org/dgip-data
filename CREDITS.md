# Data Sources, Ownership, Credits & Legal Attribution

**Repository:** `daviante-org/dgip-data`  
**Compiler Engine:** [`daviante-org/dgip`](https://github.com/daviante-org/dgip) (`https://dgip.daviante.org`)  
**Maintainer:** Daviante (`https://daviante.org`)  
**Legal & Provenance Contact:** `code@daviante.org`

---

## 1. Ownership Statement & Scope of Rights

1. **Scope of Daviante's License (`PDDL-1.0` & `Apache-2.0`)**:
   - Verification scripts, GitHub Actions workflows, and documentation in this repository are licensed under the **Apache License, Version 2.0**.
   - Daviante's **PDDL v1.0** public-domain dedication in [`LICENSE`](./LICENSE) applies **solely** to any copyright or database compilation rights held by Daviante in its own normalization, interval flattening, sweep-line merging, and packaging work.
2. **No Claim of Ownership Over Upstream Data**: **Daviante does not claim ownership over any underlying registry records, BGP routing tables, RPKI cryptographic objects, cloud/operator geofeeds, or threat intelligence lists**, and **does not grant, transfer, or sublicense any proprietary or database rights belonging to upstream data providers**.
3. **Downstream Responsibility**: Consumers, ISPs, and commercial vendors using `dgip-data` snapshots are solely responsible for ensuring their downstream use complies with the applicable public data policies and attribution terms of the underlying upstream sources listed below.
4. **Nominative Attribution & Non-Endorsement**: All third-party names, logos, and trademarks are the property of their respective owners. Their inclusion here is strictly nominative attribution of data origin and implies zero affiliation, sponsorship, or endorsement.

---

## 2. Complete Upstream Data Credits (25 Feeds Across 4 Layers)

### 2.1 Layer 1 — Regional Internet Registries (NRO) & Global BGP Routing

| Dataset Signal | Upstream Owner / Legal Entity | Canonical Origin | Public Data Terms / Reference |
| :--- | :--- | :--- | :--- |
| North America IPv4/IPv6 Allocations | **American Registry for Internet Numbers, Ltd. (ARIN)** | `https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest` | Public NRO Extended Delegation Statistics ([ARIN Statistics](https://www.arin.net/resources/registry/statistics/)) |
| Europe, Middle East & Central Asia Allocations | **Réseaux IP Européens Network Coordination Centre (RIPE NCC)** | `https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest` | Public NRO Extended Delegation Statistics ([RIPE NCC Legal](https://www.ripe.net/about-us/legal/)) |
| Asia-Pacific IPv4/IPv6 Allocations | **Asia-Pacific Network Information Centre Pty Ltd (APNIC)** | `https://ftp.apnic.net/stats/apnic/delegated-apnic-extended-latest` | Public NRO Extended Delegation Statistics ([APNIC FTP Site Terms of Use](https://www.apnic.net/about-apnic/corporate-documents/documents/resource-guidelines/apnic-ftp-site-terms-of-use/)) |
| Latin America & Caribbean Allocations | **Latin America and Caribbean Network Information Centre (LACNIC)** | `https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest` | Public NRO Extended Delegation Statistics ([LACNIC](https://www.lacnic.net/)) |
| Africa IPv4/IPv6 Allocations | **African Network Information Centre (AFRINIC) Ltd** | `https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest` | Public NRO Extended Delegation Statistics ([AFRINIC](https://afrinic.net/)) |
| Global BGP Origin ASNs (`IPv4` & `IPv6`) | **RIPE NCC — Routing Information Service (RIS)** | `https://www.ris.ripe.net/dumps/riswhoisdump.IPv4.gz` · `riswhoisdump.IPv6.gz` | Public BGP Route Collector Data (`rrc00`–`rrc26`, [RIPE RIS](https://ris.ripe.net/)) |
| Registered AS Organization Names | **RIPE NCC** | `https://ftp.ripe.net/ripe/asnames/asn.txt` | Public RIR Autonomous System Registry Metadata |

### 2.2 Layer 2 — First-Party Cloud & Network Operator Geofeeds (`IETF RFC 8805`)

| Operator / Owner | Canonical Origin | Standard / Publication Purpose |
| :--- | :--- | :--- |
| **Amazon Web Services, Inc. (AWS)** | `https://ip-ranges.amazonaws.com/geo-ip-feed.csv` | Self-published `RFC 8805` regional geofeed |
| **Google LLC (Google Cloud Platform)** | `https://www.gstatic.com/ipranges/cloud.json` | Published GCP regional IP ranges JSON |
| **Oracle America, Inc. (Oracle Cloud Infrastructure)** | `https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json` | Published OCI regional public IP ranges JSON |
| **DigitalOcean, LLC** | `https://digitalocean.com/geo/google.csv` | Self-published `RFC 8805` regional geofeed |
| **Akamai Technologies, Inc. / Linode LLC** | `https://geoip.linode.com/` | Self-published `RFC 8805` regional geofeed |
| **The Constant Company, LLC (Vultr)** | `https://geofeed.constant.com/` | Self-published `RFC 8805` regional geofeed |
| **Apple Inc. (iCloud Private Relay)** | `https://mask-api.icloud.com/egress-ip-ranges.csv` | Self-published `RFC 8805` egress geofeed |

### 2.3 Layer 3 — Cryptographic RPKI Route Origin Validation & AS Classification

| Signal | Upstream Project / Owner | Canonical Origin | License / Terms |
| :--- | :--- | :--- | :--- |
| RPKI Validated ROA Payloads (`rpki_status`) | **The OpenBSD Project — `rpki-client`** | `https://console.rpki-client.org/vrps.csv` | Public RPKI VRPs (`RFC 6811` / `RFC 7607`) across all 5 RIR Trust Anchors (`rpki-client` is ISC-licensed) |
| Autonomous System Roles (`network_type`) | **bgp.tools (Port 179 Ltd / Ben Cox)** | `https://bgp.tools/asns.csv` | Public AS classification export ([`bgp.tools/kb/api`](https://bgp.tools/kb/api)) |

### 2.4 Layer 4 — Edge CDNs, Tor Consensus & Open Threat Intelligence

| Signal | Upstream Maintainer / Owner | Canonical Origin | License / Attribution Notice |
| :--- | :--- | :--- | :--- |
| `provider="cloudflare"` (`is_cdn`, `is_cloud`) | **Cloudflare, Inc.** | `https://www.cloudflare.com/ips-v4` · `ips-v6` | Published edge proxy IPv4/IPv6 CIDR lists |
| `provider="fastly"` (`is_cdn`, `is_cloud`) | **Fastly, Inc.** | `https://api.fastly.com/public-ip-list` | Published edge POP IPv4/IPv6 CIDR list |
| `provider="github"` (`is_cloud`, `is_datacenter`) | **GitHub, Inc.** | `https://api.github.com/meta` | Published GitHub infrastructure CIDR metadata |
| `is_tor_exit` | **The Tor Project, Inc.** | `https://check.torproject.org/torbulkexitlist` | Public Tor network consensus exit relay addresses |
| `spamhaus_drop` (`is_threat`) | **The Spamhaus Project** (`© The Spamhaus Project`) | `https://www.spamhaus.org/drop/drop_v4.json` · `drop_v6.json` | **Free with Attribution**: Provided free of charge by **The Spamhaus Project** ([Spamhaus DROP](https://www.spamhaus.org/drop/)). All underlying copyright and database rights remain with The Spamhaus Project. |
| `feodo_c2` (`is_threat`) | **abuse.ch** (Institute for Cybersecurity and Engineering ICE, Bern University of Applied Sciences) | `https://feodotracker.abuse.ch/downloads/ipblocklist.txt` | **CC0 1.0 Universal (Public Domain)** ([Feodo Tracker](https://feodotracker.abuse.ch/)) |

---

## 3. Binary Format & Protocol Specification Credits

- **MaxMind DB File Format Specification v2.0 (`.mmdb`)**:
  - Specification copyright **MaxMind, Inc.** (`https://maxmind.github.io/MaxMind-DB/`), licensed under the **Creative Commons Attribution-ShareAlike 3.0 Unported License (`CC BY-SA 3.0`)** (`https://creativecommons.org/licenses/by-sa/3.0/`).
  - The `.mmdb` files in `dgip-data` (`dgip-asn.mmdb`, `dgip-country.mmdb`, `dgip-security.mmdb`) are generated by `dgip`'s clean-room Rust binary encoder strictly from the open registries and feeds credited above, and contain **zero** MaxMind GeoLite2 or GeoIP2 data. `MaxMind` and `GeoIP` are registered trademarks of MaxMind, Inc.
- **IETF & IANA Standards**: IANA Special-Purpose IP Address Registries (`RFC 6890`, `RFC 4291`), Self-Published IP Geolocation Feeds (`RFC 8805`), and RPKI Route Origin Validation (`RFC 6811`, `RFC 7607`).

---

## 4. Rights-Holder & Attribution Inquiries

If you represent an upstream registry, CSIRT, researcher, or network operator and wish to request an attribution update, usage clarification, or removal of a source from future snapshots, please contact **`code@daviante.org`**.
