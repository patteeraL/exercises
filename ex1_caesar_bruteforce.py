#!/usr/bin/env python3
"""
Exercise 1(d) — brute-force Caesar cipher.

This is included because the PDF asks for it, even though the provided
ciphertext is not a Caesar shift (see ex1_substitution_crack.py).

Design:
- Try all 26 shifts
- Score candidates with a lightweight heuristic:
  - count occurrences of common English words
  - add a small bonus for spaces/punctuation being preserved
"""


import string
from dataclasses import dataclass


ALPH = string.ascii_uppercase


DEFAULT_CIPHERTEXT = (
    "PRCSOFQX FP QDR AFOPQ CZSPR LA JFPALOQSKR. "
    "QDFP FP ZK LIU BROJZK MOLTROE."
)


COMMON_WORDS = {
    "THE",
    "AND",
    "THIS",
    "THAT",
    "IS",
    "OF",
    "TO",
    "IN",
    "FOR",
    "ON",
    "AS",
    "AN",
    "A",
}


def caesar_decrypt(text: str, shift: int) -> str:
    out = []
    for ch in text:
        up = ch.upper()
        if up in ALPH:
            idx = ALPH.index(up)
            p = ALPH[(idx - shift) % 26]
            out.append(p if ch.isupper() else p.lower())
        else:
            out.append(ch)
    return "".join(out)


def score_englishish(text: str) -> int:
    score = 0
    upper = text.upper()
    # word hits
    for w in COMMON_WORDS:
        score += 3 * upper.count(f" {w} ")
        score += 2 * upper.count(f"{w} ")
        score += 2 * upper.count(f" {w}")
    # small structural bonus
    score += upper.count(" ")
    score += upper.count(".")
    return score


@dataclass(frozen=True)
class Candidate:
    shift: int
    score: int
    plaintext: str


def main() -> None:
    ct = DEFAULT_CIPHERTEXT
    candidates: list[Candidate] = []
    for s in range(26):
        pt = caesar_decrypt(ct, s)
        candidates.append(Candidate(shift=s, score=score_englishish(pt), plaintext=pt))

    candidates.sort(key=lambda c: c.score, reverse=True)

    print("Top Caesar candidates (best-first):\n")
    for c in candidates[:10]:
        print(f"shift={c.shift:2d} score={c.score:4d}  {c.plaintext}")

    print("\n(All 26 shifts are tried; if this were a Caesar cipher, one would be clearly readable.)")


if __name__ == "__main__":
    main()

