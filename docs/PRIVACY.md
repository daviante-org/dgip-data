# Privacy Policy

**Effective Date:** November 2, 2026  
**Maintainer:** Daviante (`https://daviante.org`)  
**Contact:** `code@daviante.org`

This Privacy Policy describes what data is included in the `dgip-data` datasets and how network requests are handled by the DGIP API (`https://dgip.daviante.org`).

---

## 1. Scope of Published Datasets (`daviante-org/dgip-data`)

The datasets published in `daviante-org/dgip-data` contain exclusively network-level infrastructure metadata derived from public Regional Internet Registry (RIR) allocation records and global Border Gateway Protocol (BGP) routing tables:

- IPv4 and IPv6 address block boundaries (`start_ip`, `end_ip`, and CIDR prefixes).
- Autonomous System Numbers (ASNs) and registered Autonomous System organization names.
- Country and territory codes (ISO 3166-1 alpha-2) corresponding to RIR delegation records.

The datasets **do not** contain:
- Individual subscriber names, email addresses, account identifiers, or contact details.
- Street addresses, postal codes, or GPS/latitude-longitude coordinates.
- End-user browsing, connection, or application logs.

When you download release archives from GitHub (`github.com/daviante-org/dgip-data`), standard HTTP request handling by GitHub is governed by the [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).

---

## 2. Public API Queries (`https://dgip.daviante.org`)

When an application or user queries `https://dgip.daviante.org` (for example `/v1/ip/*` or `/v1/snapshots/*`):

1. **Query Processing**: Submitted IP literals and the connecting client IP address are processed in memory solely to return the requested ASN/country metadata or snapshot resource.
2. **Rate Limiting**: Client IP addresses are held transiently in volatile process memory (sliding-window counters) to enforce fair-use rate limits and mitigate abuse. These counters expire automatically once the rate-limit window elapses and are never written to disk or persistent databases.
3. **No Query Profiling or Resale**: Daviante does not log historical IP lookup queries to persistent storage, correlate lookup queries across users, use tracking cookies, or share query traffic with third parties.
4. **Operational Error Logs**: Minimal server diagnostics (such as upstream synchronization errors or malformed HTTP request faults) may be recorded for service reliability and do not retain bulk lookup payloads.

---

## 3. Data Accuracy and Corrections

IP allocation and ASN records reflect upstream RIR and BGP routing publications. Because Daviante does not maintain personal data in these datasets, network operators seeking to update country or ASN registration metadata for an IP block they administer should update the authoritative record at their Regional Internet Registry (ARIN, RIPE NCC, APNIC, LACNIC, or AFRINIC) or in their BGP/IRR announcements; updates propagate automatically into subsequent synchronization cycles. See [DATA_POLICY.md](./DATA_POLICY.md) for details.

---

## 4. Contact

Questions regarding this Privacy Policy may be directed to `code@daviante.org`.
