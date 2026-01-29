## Exercise 2 — Kasiski examination (Vigenère attack)

**Kasiski examination** is a classical attack against the **Vigenère cipher** (a polyalphabetic substitution).
It exploits that repeated plaintext segments can produce repeated ciphertext segments **when they align under the same key letters**.

### How it attacks Vigenère (high level)

- **Step 1: Find repeated ciphertext sequences**
  - Scan the ciphertext for repeated (commonly length 3+).
  - Example: if a trigram appears multiple times, note all positions where it occurs.

- **Step 2: Compute distances between repeats**
  - For each repeated sequence, compute the difference in starting indices between occurrences.
  - This produces a list of distances like \( d_1, d_2, \dots \).

- **Step 3: Guess key length**
  - In Vigenère, repeats tend to occur at offsets that are multiples of the **key length**.
  - Take the **GCDs** (greatest common divisors) of the collected distances and/or factor the distances.
  - Frequent factors are candidates for the key length \(k\).

- **Step 4: Reduce to Caesar problems**
  - Once a candidate key length \(k\) is chosen, split ciphertext into \(k\) streams:
    - stream 0: letters at indices 0, k, 2k, ...
    - stream 1: letters at indices 1, k+1, 2k+1, ...
    - ...
  - Each stream is (approximately) a **Caesar cipher** (shift) because the same key letter encrypts those positions.

- **Step 5: Solve each stream by frequency analysis**
  - Use English frequency analysis (or a scoring function) to find the best shift per stream.
  - The \(k\) shifts map to the \(k\) letters of the Vigenère key.


If two plaintext blocks are the same, and they are encrypted using the same section of the repeating key, then the ciphertext blocks will also be the same.
That “same key alignment” happens when the distance between the repeats is a multiple of the key length.

### Limitations

- Needs enough ciphertext length and enough repetition to produce reliable distances.
- Works best on natural-language plaintext (lots of repeated patterns like “THE”, “ING”, common phrases).
- Can produce multiple plausible key lengths; typically you verify by trying candidates and checking decryption quality.

