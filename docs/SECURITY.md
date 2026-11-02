# Security Policy

**Maintainer:** Daviante (`https://daviante.org`)  
**Security Contact:** `code@daviante.org`

---

## 1. Reporting a Vulnerability

Do **not** open public GitHub issues for suspected security vulnerabilities in `dgip`, `dgip-data` workflows, or `https://dgip.daviante.org`.

Report security issues privately by emailing **`code@daviante.org`** with:
- A clear description of the issue and affected component (`dgip` API, dataset compiler, verification script, or GitHub Actions workflow).
- Minimal reproduction steps or proof-of-concept details.
- Impact assessment.

We aim to acknowledge reports within 72 hours and coordinate remediation before public disclosure.

---

## 2. Release Integrity and Supply-Chain Verification

Every weekly `vYYYY.Www` release published in `daviante-org/dgip-data` provides two independent layers of cryptographic verification requiring zero manual key configuration:

### 2.1 SHA-256 Digest Verification (`SHA256SUMS.txt` & `manifest.json`)
Every release includes `SHA256SUMS.txt` and `manifest.json` recording the exact `SHA-256` digest and byte length of all published artifacts:

```bash
# GNU coreutils verification
sha256sum --ignore-missing -c SHA256SUMS.txt

# Zero-dependency Python stdlib verification (checks SHA256SUMS.txt + manifest.json + sizes)
python3 scripts/verify_snapshot.py --dir ./downloaded-release
```

### 2.2 GitHub Keyless OIDC Build Provenance (SLSA / Sigstore)
Weekly releases created by `.github/workflows/weekly-release.yml` generate cryptographic Sigstore build provenance attestations bound to the `daviante-org/dgip-data` GitHub Actions OIDC identity (`actions/attest-build-provenance`). Verify any downloaded asset with the GitHub CLI:

```bash
gh attestation verify bundle.tar.gz --repo daviante-org/dgip-data
gh attestation verify dgip-country.mmdb --repo daviante-org/dgip-data
```
