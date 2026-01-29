#!/usr/bin/env python3
"""
Exercise 4 — OpenSSL performance and security comparison.

(a) Measure performance: SHA1 (hash), RC4, Blowfish, DSA using OpenSSL.
(b) Compare performance and security of each method.
(c) Explain Digital Signature mechanism and how it combines strengths/weaknesses.
"""

import os
import re
import subprocess
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent / "out"


def run_openssl_speed(algo_args: list[str], seconds: int = 2) -> tuple[bool, str]:
    """Run `openssl speed` and return (success, output)."""
    try:
        result = subprocess.run(
            ["openssl", "speed", "-elapsed", "-seconds", str(seconds)] + algo_args,
            capture_output=True,
            text=True,
            timeout=60,
        )
        out = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, out
    except Exception as e:
        return False, str(e)


def extract_throughput(output: str) -> str:
    """Extract a simple throughput line from openssl speed output."""
    for line in reversed(output.splitlines()):
        if "bytes" in line.lower() or "signs" in line.lower() or "verify" in line.lower():
            return line.strip()
    return "(see raw output)"


def main() -> None:
    # --- (a) Experimental design ---
    print("=" * 70)
    print("(a) EXPERIMENTAL DESIGN")
    print("=" * 70)
    print("""
  • Tool: OpenSSL `openssl speed -elapsed -seconds N <algo>`
  • Algorithms: sha1 (hash), rc4 (stream cipher), bf/Blowfish (block cipher), dsa (signature)
  • Method: Same machine, same OpenSSL version; short fixed-time runs (2 s per algo)
  • Metric: Throughput (bytes/s or operations/s) from OpenSSL output
  • Repeatability: Run multiple times and report median/mean if writing a report
""")

    # Run benchmarks
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = [
        ("sha1", ["sha1"]),
        ("rc4", ["rc4"]),
        ("blowfish", ["bf"]),
        ("dsa", ["dsa"]),
    ]

    print("Running OpenSSL speed (this may take a few seconds)...\n")
    results = []
    for name, args in targets:
        ok, out = run_openssl_speed(args)
        raw_path = OUT_DIR / f"{name}.txt"
        raw_path.write_text(out, encoding="utf-8", errors="replace")
        summary = extract_throughput(out) if ok else "FAILED or unavailable"
        results.append((name, ok, summary))
        status = "OK" if ok else "FAILED/UNAVAILABLE"
        print(f"  {name:10s} {status:20s} {summary[:60]}")

    # --- (b) Performance and security comparison ---
    print("\n" + "=" * 70)
    print("(b) PERFORMANCE AND SECURITY COMPARISON")
    print("=" * 70)
    print("""
  • SHA1 (hash):     Fast; integrity/checksum. Security: deprecated for collision resistance.
  • RC4 (stream):    Very fast; historically used in TLS. Security: broken, do not use.
  • Blowfish (block): Fast; 64-bit block cipher. Security: legacy, small block size weak.
  • DSA (signature):  Slower (asymmetric); used for signing/verification. Security: still used with safe params.

  In practice: hashes are fastest; symmetric ciphers next; public-key (e.g. DSA) slowest.
  Security: prefer SHA-2/SHA-3, AES, and Ed25519/ECDSA over SHA1, RC4, Blowfish, classic DSA where possible.
""")

    # --- (c) Digital signature mechanism ---
    print("=" * 70)
    print("(c) DIGITAL SIGNATURE MECHANISM")
    print("=" * 70)
    print("""
  How it works:
    1. Signer has a private key (secret) and public key (shared).
    2. Sign: hash the message (e.g. with SHA-2) → then sign the hash with the private key (e.g. DSA/ECDSA/RSA).
    3. Verify: recompute hash of message; verify the signature using the public key.

  Combining strengths and weaknesses:
    • Hash: gives integrity (any change changes the hash). Weakness: hash alone is not secret.
    • Asymmetric crypto (DSA/RSA): only the private key can create a valid signature; anyone with the
      public key can verify. Weakness: slower and key management.
    • Together: integrity (hash) + authenticity and non-repudiation (signature). The signature scheme
      does not provide confidentiality; encryption (e.g. symmetric) is used for that.
""")
    print("=" * 70)


if __name__ == "__main__":
    main()
