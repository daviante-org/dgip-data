<div align="left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/logo.svg">
    <img alt="dgip-data" src="./assets/logo.svg" width="276" height="56">
  </picture>
</div>

<br>

**Weekly 4-Layer IPv4 & IPv6 Network, Geolocation, RPKI & Security Intelligence Releases**

`dgip-data` is the public dataset distribution repository maintained by [Daviante](https://daviante.org). It publishes weekly snapshots mapping global IPv4 and IPv6 address space across **4 open IP intelligence layers**:
1. **Autonomous Systems & RPKI Validation**: BGP origin ASNs, registered organizations, AS network types (`isp`, `hosting`, `cdn`, `transit`, `content`, `education`, `government`, `business`), and cryptographic RPKI ROV status (`valid`, `unknown`).
2. **Sub-National & Cloud Geolocation**: ISO 3166-1 alpha-2 country codes, ISO 3166-2 subdivisions (`region_code`), and cities compiled from RIR delegations overlaid with first-party **RFC 8805** operator and hyperscale cloud regional feeds.
3. **Cloud, CDN, Privacy Relay, Tor & Threat Intelligence**: Multi-label infrastructure and abuse classifications (`is_cloud`, `is_datacenter`, `is_cdn`, `is_tor_exit`, `is_privacy_relay`, `is_threat`, `provider`, `threat_feeds`).

Application source code for the self-hosted lookup and synchronization service lives in [`daviante-org/dgip`](https://github.com/daviante-org/dgip). Keeping weekly dataset artifacts in `dgip-data` ensures automated data snapshots remain decoupled from application releases.

---

## Versioning & Release Schedule

- **Version Tag**: `vYYYY.Www` using ISO-8601 week numbering (for example `v2026.W45`; same-week rebuilds append `.1`, `.2`).
- **Schedule**: Evaluated weekly on Mondays at `02:30 UTC` via [`.github/workflows/weekly-release.yml`](./.github/workflows/weekly-release.yml) against `https://dgip.daviante.org` and published by `mr-vegapunk[bot]`. A new GitHub Release is published only when upstream registry data has changed since the previous release.

---

## Published Formats in Every Release

Full schema details are documented in [docs/FORMAT_SPEC.md](./docs/FORMAT_SPEC.md).

| Artifact | Standard | Primary Use Case |
| :--- | :--- | :--- |
| `bundle.tar.gz` | PAX `tar.gz` | Complete snapshot bundle (`manifest.json` + all 10 CSV, Geofeed, and MMDB files) for `dgip` bootstrap and DGMail updates. |
| `dgip-asn-ipv4.csv.gz` | RFC 4180 CSV | IPv4 `start_ip,end_ip,asn,asn_org,network_type,rpki_status` intervals for SQL `int8range` / in-memory tables. |
| `dgip-asn-ipv6.csv.gz` | RFC 4180 CSV | IPv6 `start_ip,end_ip,asn,asn_org,network_type,rpki_status` intervals (RFC 5952) for SQL `numrange` / in-memory tables. |
| `dgip-country-ipv4.csv.gz` | RFC 4180 CSV | IPv4 `start_ip,end_ip,country_code,region_code,city,geo_source` intervals. |
| `dgip-country-ipv6.csv.gz` | RFC 4180 CSV | IPv6 `start_ip,end_ip,country_code,region_code,city,geo_source` intervals. |
| `dgip-security-ipv4.csv.gz` | RFC 4180 CSV | IPv4 `start_ip,end_ip,is_cloud,is_datacenter,is_cdn,is_tor_exit,is_privacy_relay,is_threat,provider,threat_feeds` intervals. |
| `dgip-security-ipv6.csv.gz` | RFC 4180 CSV | IPv6 `start_ip,end_ip,is_cloud,is_datacenter,is_cdn,is_tor_exit,is_privacy_relay,is_threat,provider,threat_feeds` intervals. |
| `dgip-geofeed.csv.gz` | IETF RFC 8805 | Standard dual-stack CIDR geolocation feed (`ip_prefix,country_code,region_code,city,`). |
| `dgip-asn.mmdb` | MaxMind DB v2.0 | Dual-stack binary ASN, `network_type`, and `rpki_status` database compatible with `libmaxminddb`, NGINX, Envoy, HAProxy, Go, Rust, and Python. |
| `dgip-country.mmdb` | MaxMind DB v2.0 | Dual-stack binary Country/Continent/Subdivision/City database compatible with `libmaxminddb`, NGINX, Envoy, HAProxy, Go, Rust, and Python. |
| `dgip-security.mmdb` | MaxMind DB v2.0 | Dual-stack binary Cloud/CDN/Tor/Privacy-Relay/Threat database compatible with `libmaxminddb`, Go, Rust, and Python. |
| `manifest.json` | RFC 8259 JSON | Structured version metadata, record counts, byte sizes, and `SHA-256` hashes. |
| `SHA256SUMS.txt` | `sha256sum` | Checksum file for CLI integrity verification. |

---

## Downloading & Verifying a Release

### Latest Release Direct URLs

```bash
BASE="https://github.com/daviante-org/dgip-data/releases/latest/download"

curl -fsSLO "$BASE/bundle.tar.gz"
curl -fsSLO "$BASE/manifest.json"
curl -fsSLO "$BASE/SHA256SUMS.txt"
```

### Integrity & Provenance Verification

1. **Verify `SHA-256` digests** with `sha256sum` or [scripts/verify_snapshot.py](./scripts/verify_snapshot.py) (Python 3 standard library only):
   ```bash
   sha256sum --ignore-missing -c SHA256SUMS.txt
   python3 scripts/verify_snapshot.py --dir .
   ```
2. **Verify GitHub OIDC SLSA build provenance** (for releases published by GitHub Actions):
   ```bash
   gh attestation verify bundle.tar.gz --repo daviante-org/dgip-data
   ```

---

## Primary Open Data Sources (Layers 1–4)

Datasets are compiled directly from 25 authoritative public Internet registries, route collectors, RPKI validators, operator geofeeds, and open threat feeds without commercial aggregator dependencies:

- **Layer 1 — RIR Delegations & BGP**: NRO Extended Delegation Statistics from **ARIN**, **RIPE NCC**, **APNIC**, **LACNIC**, and **AFRINIC**, plus **RIPE NCC RIS** (`riswhois`) BGP tables and AS names.
- **Layer 2 — Sub-National & Cloud Regional Geofeeds (`RFC 8805`)**: **AWS**, **Google Cloud**, **Oracle Cloud**, **DigitalOcean**, **Akamai/Linode**, **Vultr**, and **Apple iCloud Private Relay**.
- **Layer 3 — RPKI ROV & AS Classification**: **OpenBSD `rpki-client`** Validated ROA Payloads (`RFC 6811` / `RFC 7607`) and **`bgp.tools`** AS classes.
- **Layer 4 — Infrastructure & Threat Feeds**: **Cloudflare**, **Fastly**, **GitHub**, **Tor Project**, **Spamhaus DROP (`IPv4`/`IPv6`)**, and **Abuse.ch Feodo Tracker**.

---

## Repository Structure & Documentation

- [`docs/FORMAT_SPEC.md`](./docs/FORMAT_SPEC.md) — Technical file and binary schema specification
- [`docs/DATA_POLICY.md`](./docs/DATA_POLICY.md) — Upstream registry provenance, normalization rules, and operator correction policy
- [`docs/TERMS.md`](./docs/TERMS.md) — Terms of Use and geolocation accuracy disclaimer
- [`docs/PRIVACY.md`](./docs/PRIVACY.md) — Dataset and `https://dgip.daviante.org` API Privacy Policy
- [`docs/SECURITY.md`](./docs/SECURITY.md) — Vulnerability disclosure and artifact verification guide
- [`scripts/verify_snapshot.py`](./scripts/verify_snapshot.py) — Standalone release checksum and archive verifier
- [`LICENSE`](./LICENSE) — PDDL v1.0 (datasets) and Apache-2.0 (scripts, workflows, and documentation)

Maintained by **Daviante** (`https://daviante.org`) — Contact: `code@daviante.org`.
