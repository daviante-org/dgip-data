# Dataset Format Specification (4-Layer Schema)

**Version:** 2.0  
**Maintainer:** Daviante (`https://daviante.org`)  
**Repository:** `https://github.com/daviante-org/dgip-data`

Each weekly release (`vYYYY.Www`) in `daviante-org/dgip-data` publishes standardized 4-layer IP routing, RPKI validation, sub-national geolocation, and security intelligence tables in three industry formats — **RFC 4180 Range CSV**, **IETF RFC 8805 Geofeed CSV**, and **MaxMind DB Binary Format v2.0 (`.mmdb`)** — accompanied by a machine-readable `manifest.json` and `SHA256SUMS.txt`.

---

## 1. Release Artifacts Overview

| Filename | Format Standard | Compression | Description |
| :--- | :--- | :--- | :--- |
| `dgip-asn-ipv4.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv4 `[start_ip, end_ip]` intervals mapped to ASN, organization, `network_type`, and `rpki_status`. |
| `dgip-asn-ipv6.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv6 `[start_ip, end_ip]` intervals (RFC 5952) mapped to ASN, organization, `network_type`, and `rpki_status`. |
| `dgip-country-ipv4.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv4 `[start_ip, end_ip]` intervals mapped to country, ISO 3166-2 region, city, and `geo_source`. |
| `dgip-country-ipv6.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv6 `[start_ip, end_ip]` intervals (RFC 5952) mapped to country, ISO 3166-2 region, city, and `geo_source`. |
| `dgip-security-ipv4.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv4 `[start_ip, end_ip]` intervals mapped to cloud, datacenter, CDN, Tor, privacy-relay, and threat flags. |
| `dgip-security-ipv6.csv.gz` | RFC 4180 CSV | `gzip` | Disjoint sorted IPv6 `[start_ip, end_ip]` intervals (RFC 5952) mapped to cloud, datacenter, CDN, Tor, privacy-relay, and threat flags. |
| `dgip-geofeed.csv.gz` | IETF RFC 8805 | `gzip` | Dual-stack CIDR prefix geolocation feed (`ip_prefix,country_code,region_code,city,`). |
| `dgip-asn.mmdb` | MaxMind DB v2.0 | Binary | Dual-stack (IPv4 + IPv6) binary radix-tree database for ASN, `network_type`, and `rpki_status` lookups. |
| `dgip-country.mmdb` | MaxMind DB v2.0 | Binary | Dual-stack (IPv4 + IPv6) binary radix-tree database for country, continent, subdivision, and city lookups. |
| `dgip-security.mmdb` | MaxMind DB v2.0 | Binary | Dual-stack (IPv4 + IPv6) binary radix-tree database for cloud/CDN/Tor/privacy-relay/threat lookups. |
| `bundle.tar.gz` | POSIX.1-2001 PAX | `tar.gz` | Deterministic archive containing `manifest.json` and all 10 dataset artifacts above. |
| `manifest.json` | RFC 8259 JSON | None | Release version, build metadata, row/prefix counts, byte sizes, and `SHA-256` digests. |
| `SHA256SUMS.txt` | GNU `sha256sum` | None | Checksum manifest for command-line verification (`sha256sum -c`). |

---

## 2. RFC 4180 Range CSV Tables (`dgip-*.csv.gz`)

All range CSV files are UTF-8 encoded without BOM, use LF (`\n`) line endings, omit header rows for direct bulk database ingestion (`COPY`) and zero-copy streaming parsers, and guarantee strictly ascending, non-overlapping inclusive intervals (`start_ip <= end_ip`).

### 2.1 Autonomous System & RPKI Tables (`dgip-asn-ipv4.csv.gz`, `dgip-asn-ipv6.csv.gz`)

Columns (6):
1. `start_ip` — Inclusive lower IP bound (dotted-quad IPv4 or RFC 5952 canonical IPv6).
2. `end_ip` — Inclusive upper IP bound.
3. `asn` — 32-bit Autonomous System Number per RFC 6793 (`1..4294967294`), unsigned decimal integer without `AS` prefix.
4. `asn_org` — UTF-8 organization name registered for the ASN (RFC 4180 quoted when containing commas or quotes).
5. `network_type` — Classified AS network role (`cdn`, `hosting`, `isp`, `transit`, `content`, `education`, `government`, or `business`).
6. `rpki_status` — Cryptographic RFC 6811 / RFC 7607 Route Origin Validation status (`valid`, `invalid`, or `unknown`).

Example (`dgip-asn-ipv4.csv`):
```csv
1.1.1.0,1.1.1.255,13335,"Cloudflare, Inc.",cdn,valid
3.6.0.0,3.7.255.255,16509,"Amazon.com, Inc.",hosting,valid
```

### 2.2 Country & Sub-National Geolocation Tables (`dgip-country-ipv4.csv.gz`, `dgip-country-ipv6.csv.gz`)

Columns (6):
1. `start_ip` — Inclusive lower IP bound.
2. `end_ip` — Inclusive upper IP bound.
3. `country_code` — Uppercase 2-letter **ISO 3166-1 alpha-2** code (e.g. `US`, `DE`, `IN`, `JP`).
4. `region_code` — **ISO 3166-2** subdivision code when published by a Layer 2 geofeed or cloud region feed (e.g. `IN-MH`, `JP-13`, `US-VA`; empty `""` for country-only RIR delegations).
5. `city` — UTF-8 city name when published by a Layer 2 geofeed or cloud region feed (e.g. `Mumbai`, `Tokyo`, `Ashburn`; empty `""` otherwise).
6. `geo_source` — Provenance indicator: `geofeed` (physical operator/cloud regional feed) or `rir` (Regional Internet Registry delegation).

Example (`dgip-country-ipv4.csv`):
```csv
1.0.0.0,1.0.0.255,AU,,,rir
3.6.0.0,3.7.255.255,IN,IN-MH,Mumbai,geofeed
```

### 2.3 Security & Infrastructure Tables (`dgip-security-ipv4.csv.gz`, `dgip-security-ipv6.csv.gz`)

Columns (10):
1. `start_ip` — Inclusive lower IP bound.
2. `end_ip` — Inclusive upper IP bound.
3. `is_cloud` — `1` if hosted on public cloud infrastructure, else `0`.
4. `is_datacenter` — `1` if hosted in a server/datacenter environment, else `0`.
5. `is_cdn` — `1` if operated by an edge CDN proxy, else `0`.
6. `is_tor_exit` — `1` if an active Tor Project exit relay, else `0`.
7. `is_privacy_relay` — `1` if an anonymizing consumer privacy relay (e.g. Apple iCloud Private Relay), else `0`.
8. `is_threat` — `1` if listed on one or more verified open threat/abuse blocklists, else `0`.
9. `provider` — Matched infrastructure/relay provider slug (`aws`, `gcp`, `oracle`, `digitalocean`, `linode`, `vultr`, `cloudflare`, `fastly`, `github`, `apple_icloud_relay`, or empty `""`).
10. `threat_feeds` — Comma-separated list of matched threat feeds (`spamhaus_drop`, `feodo_c2`; RFC 4180 quoted when multiple feeds match).

Example (`dgip-security-ipv4.csv`):
```csv
3.6.0.0,3.7.255.255,1,1,0,0,0,0,aws,
104.16.0.0,104.27.255.255,1,0,1,0,0,0,cloudflare,
```

---

## 3. IETF RFC 8805 Geofeed (`dgip-geofeed.csv.gz`)

Conforms to **IETF RFC 8805** (*A Format for Self-Published IP Geolocation Feeds*) and **RFC 9632**. Disjoint `[start_ip, end_ip]` geolocation intervals are decomposed into minimal exact CIDR prefixes covering both IPv4 and IPv6, preserving sub-national ISO 3166-2 `region_code` and `city` wherever known.

Columns (5):
1. `ip_prefix` — Canonical IPv4 or IPv6 CIDR prefix.
2. `alpha2code` — ISO 3166-1 alpha-2 country code.
3. `region` — ISO 3166-2 subdivision code (or empty).
4. `city` — UTF-8 city name (or empty).
5. `postal_code` — Empty (omitted per RFC 8805 Section 2.1.1.5).

Example (`dgip-geofeed.csv`):
```csv
# DGIP Geofeed (RFC 8805) - https://github.com/daviante-org/dgip-data
1.0.0.0/24,AU,,,
3.6.0.0/15,IN,IN-MH,Mumbai,
```

---

## 4. MaxMind DB Binary Format v2.0 (`dgip-asn.mmdb`, `dgip-country.mmdb`, `dgip-security.mmdb`)

All three `.mmdb` databases implement the open **MaxMind DB File Format Specification v2.0** (`ip_version: 6` dual-stack binary search tree with standard `::/96` and `::ffff:0:0/96` IPv4 subtree pointers).

### 4.1 `dgip-asn.mmdb` (`database_type: "GeoLite2-ASN"` compatible + Layer 3 fields)
```json
{
  "autonomous_system_number": 13335,
  "autonomous_system_organization": "Cloudflare, Inc.",
  "network_type": "cdn",
  "rpki_status": "valid"
}
```

### 4.2 `dgip-country.mmdb` (`database_type: "GeoLite2-Country"` / `GeoIP2-City` compatible)
```json
{
  "continent": {
    "code": "AS",
    "names": { "en": "Asia" }
  },
  "country": {
    "iso_code": "IN",
    "names": { "en": "India" }
  },
  "subdivisions": [
    { "iso_code": "MH" }
  ],
  "city": {
    "names": { "en": "Mumbai" }
  },
  "source": "geofeed"
}
```
*(Note: `subdivisions` and `city` are included whenever sub-national metadata is present for the matched range.)*

### 4.3 `dgip-security.mmdb` (`database_type: "DGIP-Security"`)
```json
{
  "is_cloud": true,
  "is_datacenter": true,
  "is_cdn": false,
  "is_tor_exit": false,
  "is_privacy_relay": false,
  "is_threat": false,
  "provider": "aws"
}
```
*(When `is_threat` is `true`, `"threat_feeds": ["spamhaus_drop", ...]` is also populated.)*
