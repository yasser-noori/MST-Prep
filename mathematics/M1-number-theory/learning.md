# M1 — Number theory: Learning

[← Back to the index](../../README.md) · [Go to the M1 practice questions →](doing.md)

## 1. What you remember

**From the test (your own recollection):**
- LCM and GCF appeared on the test. Exact wording unknown.

**Recognized later when topics were suggested:**
- No follow-up recognition recorded for this category.

**Added for practice (not recalled from the test):**
- Divisibility, remainders, and factor counting are added for transfer; they were not specifically recalled.

All questions here are original practice. They are not copies of real test questions.

## 2. Core skills taught on this page

- Find factors, multiples, and prime factorizations.
- Use divisibility rules (2, 3, 4, 5, 6, 8, 9, 10, 11) to test numbers and recover missing digits.
- Recognize GCF situations: splitting several totals into the greatest number of identical groups.
- Recognize LCM situations: matching totals from packs of different sizes, and recurring events that coincide.
- Decide which unknown is asked for (number of groups, items per group, or the shared total) and check it.

## 3. Core patterns

### Pattern 1: Splitting totals into identical groups (GCF)

- **Clue to notice:** you already *have* several amounts (18 red, 30 blue), and you must cut them into the **greatest number of identical** groups, bags, or teams with **nothing left over**. The answer has to be *smaller* than (or equal to) the amounts you started with.
- **Decision to make:** the greatest number of groups is the GCF of the totals. Then ask yourself which unknown the question wants:
  - number of groups = GCF
  - items of one kind in each group = that total ÷ GCF
  - items in each group altogether = add up the per-group amounts
- **How to check it:** the number of groups must divide **every** total exactly. List the divisors of the smaller total from largest to smallest. The first one that divides every total gives the greatest possible number of groups.

Example: 18 red and 30 blue tiles → GCF(18, 30) = 6 bags, each with 3 red + 5 blue = 8 tiles.

### Pattern 2: Matching totals and events that line up (LCM)

- **Clue to notice:** things come in fixed **steps** (packs of 8, a bus every 12 minutes, a light every 6 seconds) and you want the steps to **match** or happen **together again**. The answer has to be *at least as big as* the largest step.
- **Decision to make:** the first shared total or shared time is the LCM. Again, decide which unknown is asked:
  - shared total, or time until they meet again = LCM
  - number of packs of one kind = LCM ÷ that pack size
  - a clock time or date = start + LCM (count forward, do not count the starting day)
  - If the events start at **different** times, the LCM alone is not enough: list each schedule and find the first time on both lists.
- **How to check it:** the answer must be a multiple of **every** step size. List the positive multiples of the largest step in order. The first one divisible by every step is the least common multiple. The plain product of the numbers is a common multiple, but often not the *least* one.

Example: packs of 18 and 30 → LCM(18, 30) = 90 tiles of each colour (5 packs of 18, 3 packs of 30).

**GCF or LCM?** Ask: "Am I *cutting up* amounts I already have (answer gets smaller → GCF), or *building up* to a total that several step sizes all reach (answer gets bigger → LCM)?"

### Pattern 3: Remainders and leftovers

- **Clue to notice:** words such as *left over*, *how many more*, *rows needed*, *every student has a seat*, or a statement like "in groups of 6, 4 are left".
- **Decision to make:** write the division as *total = (groups × size) + remainder*, then pick the number the question wants:
  - full groups → the whole-number part
  - left over → the remainder
  - groups needed so nobody is left out → whole-number part + 1 (if the remainder is not 0)
  - how many more to fill one more group → group size − remainder
  - Working backward: if a number leaves the **same** remainder for several divisors, then (number − remainder) is a common multiple. If it is always **short by the same amount** (4 left in 6s, 6 left in 8s are both "2 short"), then (number + 2) is a common multiple.
- **How to check it:** rebuild the total. For 46 bottles in crates of 8, write 46 = 5 × 8 + 6. Six bottles are left over and two more would fill another crate.

### Pattern 4: Prime factorization and divisibility rules

- **Clue to notice:** large numbers, missing digits (31□4), counting factors, or numbers already written as products of primes.
- **Decision to make:** break numbers into primes (180 = 2² × 3² × 5) or use a quick rule:

| Divisible by | Rule |
|---|---|
| 2 | last digit even |
| 3 | digit sum divisible by 3 |
| 4 | last two digits divisible by 4 |
| 5 | last digit 0 or 5 |
| 6 | divisible by both 2 and 3 |
| 8 | last three digits divisible by 8 |
| 9 | digit sum divisible by 9 |
| 10 | last digit 0 |
| 11 | alternating sum of digits (+ − + − …) is 0 or a multiple of 11 |

  - GCF from prime factorizations: take each shared prime with the **smaller** power.
  - LCM from prime factorizations: take every prime that appears, with the **larger** power.
  - To count factors, list factor **pairs** (1 × 16, 2 × 8, 4 × 4). A square number has one pair with a repeated factor, so count it once.
  - For "divisible by 45" or "divisible by 6", split into rules you know: 45 = 5 × 9, 6 = 2 × 3.
- **How to check it:** multiply the prime factorization back out, and check that every factor in it really is prime. For a missing digit, test your digit **and** confirm that no other digit 0–9 also works.

## 4. Worked example

> A rectangular floor measures 84 cm by 60 cm. It will be covered exactly, with no gaps, overlaps, or cutting, by identical square tiles that are as large as possible. How many tiles are needed?
>
> A. 7
>
> B. 12
>
> C. 35
>
> D. 140
>
> E. 420
>
> **Answer: C.**
>
> **Decisive step:** the tile side must fit exactly into **both** 84 and 60, and it must be as large as possible, so the side is GCF(84, 60). 84 = 2² × 3 × 7 and 60 = 2² × 3 × 5, so the GCF is 2² × 3 = 12 cm. Along the 84 cm side there are 84 ÷ 12 = 7 tiles, and along the 60 cm side there are 60 ÷ 12 = 5 tiles, so 7 × 5 = **35 tiles**.
>
> **Check:** 35 tiles × (12 × 12) cm² = 5040 cm², and 84 × 60 = 5040 cm².
>
> **Why the tempting answer is wrong:** **B (12)** is the side length of each tile, not the number of tiles. It answers "how big?" when the question asks "how many?". The other traps: A (7) counts only one row; D (140) uses a common factor that is not the greatest (6 cm tiles → 14 × 10); E (420) is a common multiple of the two lengths. A tile side must divide both lengths.

## 5. Practise

Go to [M1 practice questions (doing.md)](doing.md). Commit to an answer for each question before you open the answer key.
