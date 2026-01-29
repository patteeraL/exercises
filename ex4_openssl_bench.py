#!/usr/bin/env python3
"""
Exercise 4 — measure performance of sha1, RC4, Blowfish, and DSA using OpenSSL.

Implementation approach:
- Use `openssl speed -elapsed <algo>` where possible.
- Write raw output logs to exercises/out/
- Print a small summary and any availability warnings (some algorithms may be disabled
  in modern OpenSSL builds, e.g., RC4, Blowfish depending on provider config).
"""


import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


OUT_DIR = Path(__file__).resolve().parent / "out"


@dataclass(frozen=True)
class BenchResult:
    name: str
    ok: bool
    detail: str
    raw_path: Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )


def parse_best_throughput(openssl_speed_output: str) -> Optional[str]:
  
    lines = openssl_speed_output.splitlines()
    table = [ln for ln in lines if re.search(r"\bbytes\b", ln)]
    if table:
        return table[-1].strip()
    return None


def bench_one(name: str, args: list[str]) -> BenchResult:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = OUT_DIR / f"{name}.txt"

    # Keep runs short so the lab is fast/repeatable.
    cp = run(["openssl", "speed", "-elapsed", "-seconds", "3", *args])
    raw_path.write_text(cp.stdout, encoding="utf-8", errors="replace")

    if cp.returncode != 0:
        return BenchResult(name=name, ok=False, detail=f"openssl speed failed (exit {cp.returncode})", raw_path=raw_path)

    best = parse_best_throughput(cp.stdout)
    return BenchResult(name=name, ok=True, detail=(best or "ok (see raw log)"), raw_path=raw_path)


def main() -> None:
    targets = [
        ("sha1", ["sha1"]),
        ("rc4", ["rc4"]),
        ("blowfish", ["bf"]),
        ("dsa", ["dsa"]),
    ]

    results: list[BenchResult] = []
    for name, args in targets:
        results.append(bench_one(name, args))

    print("OpenSSL speed results (best-effort parsing):\n")
    for r in results:
        status = "OK" if r.ok else "UNAVAILABLE/FAILED"
        print(f"- {r.name:9s} {status:17s}  {r.detail}  (raw: {os.path.relpath(r.raw_path, Path.cwd())})")

    print("\nNotes:")
    print("- If RC4/Blowfish are disabled in your OpenSSL build, their benchmark will fail; check the raw logs.")
    print("- For reporting, describe your experimental design: same machine, same OpenSSL version, repeated runs, and median/mean.")
    print("- For security comparison: SHA1 is deprecated for collision resistance; RC4 is broken; Blowfish is legacy; DSA is signature scheme.")


if __name__ == "__main__":
    main()

