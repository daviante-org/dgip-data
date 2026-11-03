# Terms of Use

**Effective Date:** November 2, 2026  
**Maintainer:** Daviante (`https://daviante.org`)  
**Contact:** `code@daviante.org`

By downloading datasets from `daviante-org/dgip-data` or querying `https://dgip.daviante.org`, you agree to these Terms of Use.

---

## 1. Licensing and Permitted Use

1. **Datasets**: Weekly snapshot archives published under `daviante-org/dgip-data` Releases are made available under the licensing terms set out in [LICENSE](../LICENSE), subject to upstream Regional Internet Registry, operator geofeed, and security-feed conditions documented in [CREDITS.md](../CREDITS.md), [NOTICE](../NOTICE), and [DATA_POLICY.md](./DATA_POLICY.md). Daviante claims no ownership over third-party upstream records and does not transfer or sublicense rights belonging to upstream providers.
2. **Software and Documentation**: Scripts, specifications, and workflow definitions in this repository are licensed under the Apache License, Version 2.0.

---

## 2. Acceptable Use of the Hosted API (`https://dgip.daviante.org`)

1. **Rate Limits**: Automated clients must respect HTTP `429 Too Many Requests` responses, `Retry-After` headers, and `X-RateLimit-*` headers.
2. **Bulk Workloads**: High-throughput applications, mail servers, and security appliances performing continuous or high-volume IP lookups should download the weekly dataset archives (`.csv.gz`, `.mmdb`, or `bundle.tar.gz`) and evaluate lookups locally rather than sending unbounded live traffic to the public API.
3. **Prohibited Conduct**: You may not attempt to disrupt service availability, bypass rate controls, probe non-public infrastructure, or misrepresent modified datasets as unaltered official Daviante releases.

---

## 3. Geolocation and Routing Accuracy Disclaimer

IP-to-country and IP-to-ASN mappings are statistical and administrative approximations derived from Regional Internet Registry delegation files and global BGP routing announcements:

- Allocated IP blocks may be routed via global anycast networks, virtual private networks (VPNs), satellite constellations, mobile carrier gateways, or cross-border Local Internet Registry (LIR) assignments that do not correspond to the physical jurisdiction of an end user.
- BGP origin ASNs and organization names may change at any time due to prefix transfers, leasing, traffic engineering, or route hijacks prior to upstream registry convergence.

**High-Risk Use Restriction**: The datasets and API are not designed, certified, or intended for emergency services routing (such as E911/E112), life-safety systems, critical infrastructure control, or as sole dispositive evidence of an individual's physical location or identity in legal or regulatory proceedings.

---

## 4. Disclaimer of Warranties and Limitation of Liability

THE DATASETS, SOFTWARE, AND HOSTED API ARE PROVIDED "AS IS" AND "AS AVAILABLE," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, ACCURACY, COMPLETENESS, OR NON-INFRINGEMENT.

IN NO EVENT SHALL DAVIANTE, ITS MAINTAINERS, OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES, LOSS OF USE, DATA, OR PROFITS, OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT, ARISING IN ANY WAY OUT OF THE USE OF THE DATASETS OR API, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

## 5. Modifications and Contact

Daviante may update these Terms of Use by committing a revised version to `daviante-org/dgip-data`. Inquiries may be sent to `code@daviante.org`.
