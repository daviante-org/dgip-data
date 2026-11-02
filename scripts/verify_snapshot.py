#!/usr/bin/env python3
"""Verify DGIP snapshot release artifacts using Python 3 standard library only.

Checks:
1. Every present release file matches its SHA-256 digest in SHA256SUMS.txt.
2. manifest.json parses cleanly and every present dataset file matches both
   the SHA-256 digest and exact byte size recorded in manifest.json.
3. If bundle.tar.gz is present, verifies every archived member's SHA-256 digest
   against manifest.json without extracting files to disk.

Usage:
    python3 scripts/verify_snapshot.py --dir ./release-dir
    python3 scripts/verify_snapshot.py --dir ./release-dir --require-all
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_sha256sums(sums_path: Path) -> dict[str, str]:
    if not sums_path.is_file():
        raise FileNotFoundError(f"Missing checksum file: {sums_path}")

    entries: dict[str, str] = {}
    for line_no, raw in enumerate(sums_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or len(parts[0]) != 64:
            raise ValueError(f"Malformed SHA256SUMS.txt entry on line {line_no}: {raw!r}")
        sha_hex = parts[0].lower()
        int(sha_hex, 16)
        filename = parts[1].lstrip("*")
        entries[filename] = sha_hex

    if not entries:
        raise ValueError("SHA256SUMS.txt contains no entries.")
    return entries


def verify_release_directory(release_dir: Path, require_all: bool = False) -> None:
    sums_map = parse_sha256sums(release_dir / "SHA256SUMS.txt")
    manifest_path = release_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Missing manifest file: {manifest_path}")

    checked_files = 0
    for filename, expected_sha in sorted(sums_map.items()):
        candidate = release_dir / filename
        if not candidate.is_file():
            if require_all:
                raise FileNotFoundError(f"Required artifact missing from {release_dir}: {filename}")
            continue
        actual_sha = sha256_file(candidate)
        if actual_sha != expected_sha:
            raise ValueError(
                f"SHA-256 mismatch for {filename}: expected {expected_sha}, got {actual_sha}"
            )
        checked_files += 1
        print(f"[OK] SHA256SUMS.txt verified: {filename} ({actual_sha[:16]}...)")

    if checked_files == 0:
        raise ValueError(f"No artifacts listed in SHA256SUMS.txt were found in {release_dir}.")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest.get("version")
    files_meta = manifest.get("files")
    if not isinstance(version, str) or not version or not isinstance(files_meta, dict) or not files_meta:
        raise ValueError("manifest.json is missing required 'version' or non-empty 'files' map.")

    for filename, meta in sorted(files_meta.items()):
        expected_sha = str(meta["sha256"]).lower()
        expected_size = int(meta["size_bytes"])
        if filename in sums_map and sums_map[filename] != expected_sha:
            raise ValueError(
                f"Digest conflict between manifest.json and SHA256SUMS.txt for {filename}"
            )
        candidate = release_dir / filename
        if candidate.is_file():
            actual_size = candidate.stat().st_size
            if actual_size != expected_size:
                raise ValueError(
                    f"Size mismatch for {filename}: manifest expects {expected_size} B, got {actual_size} B"
                )
        elif require_all:
            raise FileNotFoundError(f"Manifest artifact missing from {release_dir}: {filename}")

    bundle_path = release_dir / "bundle.tar.gz"
    if bundle_path.is_file():
        with tarfile.open(bundle_path, mode="r:gz") as tf:
            members = {m.name: m for m in tf.getmembers() if m.isfile()}
            if "manifest.json" not in members:
                raise ValueError("bundle.tar.gz is missing manifest.json")
            for filename, meta in sorted(files_meta.items()):
                if filename not in members:
                    raise ValueError(f"bundle.tar.gz is missing dataset member {filename}")
                extracted = tf.extractfile(members[filename])
                if extracted is None:
                    raise ValueError(f"Unable to read member {filename} from bundle.tar.gz")
                digest = hashlib.sha256()
                size = 0
                for chunk in iter(lambda: extracted.read(65536), b""):
                    digest.update(chunk)
                    size += len(chunk)
                if digest.hexdigest() != str(meta["sha256"]).lower():
                    raise ValueError(f"Corrupt tar member {filename} inside bundle.tar.gz")
                if size != int(meta["size_bytes"]):
                    raise ValueError(f"Size mismatch for tar member {filename} inside bundle.tar.gz")
        print(f"[OK] bundle.tar.gz archive members verified ({len(files_meta)} datasets + manifest.json)")

    print(f"[OK] Snapshot {version} verified successfully ({checked_files} files checked).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify DGIP release checksums and manifest.")
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("."),
        help="Directory containing downloaded DGIP release artifacts.",
    )
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="Require every file listed in SHA256SUMS.txt and manifest.json to exist on disk.",
    )
    args = parser.parse_args()

    try:
        verify_release_directory(args.dir, require_all=args.require_all)
    except Exception as exc:
        print(f"[ERROR] Verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
