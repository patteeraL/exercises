#!/usr/bin/env python3
"""
Exercise 1 (Cryptanalysis) — crack the given ciphertext.

The ciphertext in the PDF is *not* a Caesar cipher (shift is not constant).
It is a monoalphabetic substitution. This script:
- prints top-3 letter frequencies
- highlights common 2/3-letter word hints
- decrypts using a recovered substitution key for this specific ciphertext
"""


from collections import Counter
import re
import time
from typing import Dict


CIPHERTEXT = (
    "PRCSOFQX FP QDR AFOPQ CZSPR LA JFPALOQSKR. "
    "QDFP FP ZK LIU BROJZK MOLTROE."
)


def letter_frequencies(text: str) -> Counter[str]:
    letters = [c for c in text.upper() if "A" <= c <= "Z"]
    return Counter(letters)


def top_n(counter: Counter[str], n: int) -> list[tuple[str, int]]:
    return counter.most_common(n)


def apply_substitution(text: str, mapping: Dict[str, str]) -> str:
    out = []
    for ch in text:
        up = ch.upper()
        if "A" <= up <= "Z" and up in mapping:
            repl = mapping[up]
            out.append(repl if ch.isupper() else repl.lower())
        else:
            out.append(ch)
    return "".join(out)


def recover_mapping_for_this_message() -> Dict[str, str]:
    """
    Recovered by:
    - spotting repeats: "FP" occurs twice -> likely "IS"
    - "QDR" fits "THE"
    - first word matches "SECURITY" perfectly after mapping

    Mapping is CIPHER -> PLAIN (uppercase letters).
    """

    return {
        "P": "S",
        "R": "E",
        "C": "C",
        "S": "U",
        "O": "R",
        "F": "I",
        "Q": "T",
        "X": "Y",
        "D": "H",
        "A": "F",
        "Z": "A",
        "L": "O",
        # JFP... becomes MIS..., so J -> M (not D)
        "J": "M",
        "K": "N",
        # BROJZK becomes GERMAN, so B -> G
        "B": "G",
        "M": "P",
        "T": "V",
        "E": "B",
        "I": "L",
        "U": "D",
        "G": "W",
        "H": "G",
        "N": "M",
        "V": "K",
        "W": "J",
        "Y": "X",
    }


def main() -> None:
    start_time = time.time()
    
    print("Ciphertext:\n" + CIPHERTEXT + "\n")

    freq = letter_frequencies(CIPHERTEXT)
    print("a) Top 3 most frequent characters (A-Z only):")
    for ch, count in top_n(freq, 3):
        print(f"  {ch}: {count}")
    print()

    print("b) Common 2/3-letter English words to look for:")
    print("  - 2-letter: IS, OF, TO, IN, IT, AS, AT, AN")
    print("  - 3-letter: THE, AND, FOR, ARE, BUT, NOT, YOU")
    print("  Hint: repeated 'FP' strongly suggests 'IS'; 'QDR' fits 'THE'.")
    print()

    mapping = recover_mapping_for_this_message()
    plaintext = apply_substitution(CIPHERTEXT, mapping)

    # Normalize any accidental double spaces, etc.
    plaintext = re.sub(r"[ \t]+", " ", plaintext).strip()
    print("c) Decrypted result:")
    print(plaintext)
    print()

    elapsed_time = time.time() - start_time
    print("d) Time taken to crack this message:")
    print(f"  {elapsed_time*1000:.4f} milliseconds ({elapsed_time:.6f} seconds)")
    print()

    print("e) Note:")
    print("  The PDF mentions Caesar brute force; see exercises/ex1_caesar_bruteforce.py")


if __name__ == "__main__":
    main()