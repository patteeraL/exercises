## Basic Encryption – Activity IV (Implemented)

This repo implements the **4 exercises** from `338_Ch06-Activity IV-Basic Encryption.pdf`.

### Requirements

- **Python 3.10+**
- **OpenSSL** (`openssl`)
- **ImageMagick** (`magick`) for Exercise 3 image conversion

### Exercise 1 — Cryptanalysis (given ciphertext)

Run:

```bash
python3 ./ex1_substitution_crack.py
```

Output: 
```
Ciphertext:
PRCSOFQX FP QDR AFOPQ CZSPR LA JFPALOQSKR. QDFP FP ZK LIU BROJZK MOLTROE.

a) Top 3 most frequent characters (A-Z only):
  P: 7
  R: 6
  O: 6

b) Common 2/3-letter English words to look for:
  - 2-letter: IS, OF, TO, IN, IT, AS, AT, AN
  - 3-letter: THE, AND, FOR, ARE, BUT, NOT, YOU
  - Hint: repeated 'FP' strongly suggests 'IS'; 'QDR' fits 'THE'.

c) Decrypted result:
SECURITY IS THE FIRST CAUSE OF MISFORTUNE. THIS IS AN OLD GERMAN PROVERB.

d) Time taken to crack this message:
  1.4741 milliseconds (0.001474 seconds)

e) Note:
  The PDF mentions Caesar brute force; see /ex1_caesar_bruteforce.py
```

It prints:
- Top-3 letter frequencies (as requested)
- Notes on common 2/3-letter words (“IS”, “THE”, “OF”, etc.)
- The decrypted plaintext

Also included (requested by the PDF) is a brute-force Caesar cracker:

```bash
python3 ./ex1_caesar_bruteforce.py
```
Output:
Top Caesar candidates (best-first):

```
shift=23 score=  32  SUFVRITA IS TGU DIRST FCVSU OD MISDORTVNU. TGIS IS CN OLX EURMCN PROWURH.
shift=16 score=  24  ZBMCYPAH PZ ANB KPYZA MJCZB VK TPZKVYACUB. ANPZ PZ JU VSE LBYTJU WYVDBYO.
shift=15 score=  20  ACNDZQBI QA BOC LQZAB NKDAC WL UQALWZBDVC. BOQA QA KV WTF MCZUKV XZWECZP.
shift= 0 score=  18  PRCSOFQX FP QDR AFOPQ CZSPR LA JFPALOQSKR. QDFP FP ZK LIU BROJZK MOLTROE.
shift= 5 score=  18  KMXNJALS AK LYM VAJKL XUNKM GV EAKVGJLNFM. LYAK AK UF GDP WMJEUF HJGOMJZ.
shift=10 score=  18  FHSIEVGN VF GTH QVEFG SPIFH BQ ZVFQBEGIAH. GTVF VF PA BYK RHEZPA CEBJHEU.
shift=11 score=  18  EGRHDUFM UE FSG PUDEF ROHEG AP YUEPADFHZG. FSUE UE OZ AXJ QGDYOZ BDAIGDT.
shift=17 score=  18  YALBXOZG OY ZMA JOXYZ LIBYA UJ SOYJUXZBTA. ZMOY OY IT URD KAXSIT VXUCAXN.
shift= 1 score=  16  OQBRNEPW EO PCQ ZENOP BYROQ KZ IEOZKNPRJQ. PCEO EO YJ KHT AQNIYJ LNKSQND.
shift= 2 score=  16  NPAQMDOV DN OBP YDMNO AXQNP JY HDNYJMOQIP. OBDN DN XI JGS ZPMHXI KMJRPMC.
```

(All 26 shifts are tried; if this were a Caesar cipher, one would be clearly readable.)

### Exercise 2 — Kasiski examination (Vigenère attack)

See:
- `/ex2_kasiski_examination.md`

### Exercise 3 — Block cipher modes (ECB weakness demo)


1) Encrypt with AES-256-ECB (no salt, no padding):
```bash 
openssl enc -aes-256-ecb -in org.x -nosalt \
-out enc.x 
```

2) Try CBC (with IV Auto generate):
```bash
openssl enc -aes-256-cbc -in org.x -nosalt \
-out enc_cbc.x 
```

**Note:** Open `enc.pbm` and `enc_cbc.pbm` in an image viewer to see the difference. ECB will show visible patterns from the original image, while CBC should look random.

Analysis notes:

When we encrypt the PBM pixel bytes with **AES-256-ECB** and then view the encrypted bytes as a PBM image, the result typically **still shows the original structure/patterns** (edges, large regions, shapes).

With **CBC** (or other modes with IV/chaining/feedback), the encrypted image should look **much more random/noisy**, and the original structure is largely hidden.

- ECB encrypts each block independently:
  - identical plaintext blocks → identical ciphertext blocks (under the same key)
- Images often contain large areas of repeated pixel patterns.
- Therefore ECB preserves repetition structure, which the human eye easily detects.

Modes like CBC introduce dependency between blocks (and an IV):
- even if two plaintext blocks are identical, their ciphertext blocks differ (because the XOR/chaining input differs)
- this breaks the visible pattern repetition.

### Takeaway

For block ciphers, **the mode of operation is security-critical**:
- ECB is generally unsafe for structured data (images, database pages, protocol fields).
- Use modes with IV + integrity in real systems.


### Exercise 4 — Performance measurement (hash/ciphers/signature)

This uses `openssl speed` to measure SHA1, RC4, Blowfish, and DSA (where available in your OpenSSL build).

Run:

```bash
python3 /ex4_openssl_bench.py
```

It prints a small table and writes the raw outputs to `/out/`.

```
======================================================================
(a) EXPERIMENTAL DESIGN
======================================================================

  • Tool: OpenSSL `openssl speed -elapsed -seconds N <algo>`
  • Algorithms: sha1 (hash), rc4 (stream cipher), bf/Blowfish (block cipher), dsa (signature)
  • Method: Same machine, same OpenSSL version; short fixed-time runs (2 s per algo)
  • Metric: Throughput (bytes/s or operations/s) from OpenSSL output
  • Repeatability: Run multiple times and report median/mean if writing a report

Running OpenSSL speed (this may take a few seconds)...

  sha1       OK                   type             16 bytes     64 bytes    256 bytes   1024 b
  rc4        OK                   type             16 bytes     64 bytes    256 bytes   1024 b
  blowfish   OK                   type             16 bytes     64 bytes    256 bytes   1024 b
  dsa        OK                   Doing 2048 bits verify dsa ops for 2s: 15292 2048 bits DSA v

======================================================================
(b) PERFORMANCE AND SECURITY COMPARISON
======================================================================

  • SHA1 (hash):     Fast; integrity/checksum. Security: deprecated for collision resistance.
  • RC4 (stream):    Very fast; historically used in TLS. Security: broken, do not use.
  • Blowfish (block): Fast; 64-bit block cipher. Security: legacy, small block size weak.
  • DSA (signature):  Slower (asymmetric); used for signing/verification. Security: still used with safe params.

  In practice: hashes are fastest; symmetric ciphers next; public-key (e.g. DSA) slowest.
  Security: prefer SHA-2/SHA-3, AES, and Ed25519/ECDSA over SHA1, RC4, Blowfish, classic DSA where possible.

======================================================================
(c) DIGITAL SIGNATURE MECHANISM
======================================================================

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

======================================================================
```