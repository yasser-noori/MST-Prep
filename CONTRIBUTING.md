# Contributing: authoring guide for the MGCI TOPS / MST prep bank

This file is the single shared reference for everyone writing, reviewing, or integrating content. You should not need any other conversation or document to do your work.

## Agent pickup and merge workflow

1. **Claim one issue.** Pick one unassigned issue labelled `ready-to-claim`. Self-assign where supported, post a short claim comment (for example "Claiming M2"), replace `ready-to-claim` with `in-progress`, and re-read the issue to verify nobody else claimed it first before editing anything.
2. **Branch from the published scaffold** (the repository's default branch). Use a category-specific branch such as `content/m1-number-theory`.
3. **Stay in your lane.** A category author edits only the two files in their category directory (`1. Learning.md`, `2. Doing.md`) and any category-specific diagram assets under `Grade 9/assets/<category-id>/`. The integration agent owns shared README changes.
4. **Open one focused PR** that links the issue with `Closes #<number>` and fills in the PR template: question counts, tier split, independent solution check, and visual-render check.
5. **Request the subject review** (math or science review issue). Keep fixes inside the owning PR to avoid conflicts. A reviewer who finds a defect after merge opens a focused follow-up PR touching only that category.
6. **Release.** The release agent marks the bank complete only after all content, review, and integration checks pass.

If you get stuck on something outside your files, label the issue `blocked` and explain in a comment.

## Project shape

- `README.md` links to each grade.
- `Grade 9/README.md` holds the Grade 9 index and study calendar.
- `Grade 9/1. Math/` and `Grade 9/2. Science/` hold the topic folders. Each topic contains `1. Learning.md` and `2. Doing.md`.
- `Grade 9/assets/<category-id>/` holds figures. `Grade 9/tools/figures/` holds their generators.
- `.github/` contains issue and pull request templates.

Use labelled graphics for diagrams and tables for tabular data. Keep each topic to two student-facing pages.

## Who the student is

A Grade 8 student preparing for Grade 9 entry. They open the README, find today's assignment, and follow a link to a category. The bank should build **transferable reasoning**: a student who has drilled container volume should recognize which dimensions matter when the container, diagram, or requested quantity changes; a student who has drilled a lightbulb puzzle should handle an unfamiliar problem governed by several conditions.

Students track first-attempt accuracy on fresh questions, guesses, and recurring mistakes. **Never claim a home practice score predicts an admissions percentile.**

## Practice design

Write original questions for any student preparing for Grade 9 entry. Use A–E choices throughout, with equal math and science coverage across the bank. The 60-minute session is a practice setting.

## The per-category contract

Each category issue delivers:

- One complete `1. Learning.md` with **exactly one** worked A–E question.
- One complete `2. Doing.md` with **exactly 30** original A–E drills, `<ID>-Q01` to `<ID>-Q30`.
- **Exactly 18 Medium and 12 Challenge** drills.
- **Six consecutive five-question blocks** (Q01–05, Q06–10, Q11–15, Q16–20, Q21–25, Q26–30). Each block contains **3 Medium + 2 Challenge** in varied order.
- A separate answer key at the bottom. **Tier labels appear only in the key.**
- **Q26–Q30 reserved** for first exposure on the final weekend.

Repository totals when finished: 300 drills (150 math, 150 science), 180 Medium and 120 Challenge, plus 10 worked examples that never count toward the 300.

## Tier definitions

**Medium:** the student recognizes a relationship and applies it in a fresh setting. It may require several steps, calculations, or careful reading.

**Challenge:** the student must make an additional reasoning decision: choose between plausible models, combine constraints, work backward, distinguish competing explanations, or determine whether the information is sufficient. **Large numbers and long wording alone do not qualify.**

Tiers are separate from **question styles**. Across the 30 items, cover all four styles: direct items, close variants, reverse problems, and unfamiliar transfer problems.

## 1. Learning.md format

1. **Key ideas.** Explain terms, symbols, and rules in plain language before the student needs them. Start with a familiar example.
2. **Three or four core patterns.** Show what to look for, how to decide, and how to check the answer.
3. **One worked A–E question** with the decisive step and an explanation of the most tempting wrong answer.
4. **A direct link to `2. Doing.md`.**

Remove the scaffold-status note when the page is complete.

## 2. Doing.md format

- Stable visible IDs `M2-Q01` … `M2-Q30`, each preceded by an explicit lowercase anchor: `<a id="m2-q01"></a>`. Calendar links depend on these anchors.
- Neutral headings: just the ID. Never a hint such as "Use LCM here."
- Exactly five distinct choices labelled A–E, and exactly one defensible answer.
- Use a short, familiar setup. Build difficulty through the reasoning and supply unfamiliar facts or rules in the stem.
- All solutions go after the entire question set, in an answer key with: ID, correct letter, tier, short reasoning, and the clue that rules out the closest distractor.
- Believable distractors derived from real mistakes. For a volume problem, choices might represent water present, empty capacity, and total capacity.
- Vary answer positions; avoid any obvious letter pattern. Aim for each letter to be correct roughly 5–7 times out of 30.
- Every question is independently solvable. A student who gets one item wrong must still have everything needed for the next.
- Use real, readable visuals when interpreting the visual is the skill: supply dimensions, units, arrow legends, switch states, junctions, or pivot positions.
- Q26–Q30 must be genuinely fresh applications. Do not give away final-weekend answers through near-duplicates earlier in the bank.
- Remove the scaffold-status note when the page is complete.

### Question template

```markdown
<a id="m1-q01"></a>
### M1-Q01

Question stem, including any diagram or table.

A. …

B. …

C. …

D. …

E. …
```

Put a blank line between choices. GitHub Markdown joins consecutive lines into one paragraph, so choices on adjacent lines run together.

### Answer key template

```markdown
## Answer key

| ID | Answer | Tier | Reasoning | Closest distractor ruled out by |
|---|---|---|---|---|
| M1-Q01 | C | Medium | GCF(18, 30) = 6 bags. | B (8) is tiles per bag, not the number of bags. |
```

### Worked example (model)

From S3, showing the expected finished form:

> A cylinder contains 40 mL of water. A student fully submerges a stone without spilling water. The cylinder now reads 55 mL. What is the stone's volume?
>
> A. 15 cm³
>
> B. 27.5 cm³
>
> C. 40 cm³
>
> D. 55 cm³
>
> E. 95 cm³
>
> **Answer: A.** The stone displaces 55 − 40 = 15 mL, and 1 mL = 1 cm³. Choice D includes the original water.

## ID conventions

| Thing | Convention | Example |
|---|---|---|
| Category ID | Subject letter + number | `M2`, `S4` |
| Question ID | `<category>-Q<two digits>` | `M2-Q07` |
| Anchor | lowercase question ID | `<a id="m2-q07"></a>` |
| Deep link | `<path>/2. Doing.md#<anchor>` | `Grade 9/1. Math/M2-geometry-and-measurement/2. Doing.md#m2-q07` |
| Branch | `content/<lowercase dir name>` | `content/m2-geometry-and-measurement` |
| Asset folder | `Grade 9/assets/<category-id>/` | `Grade 9/assets/S4/` |

## Verification requirements (before opening a PR)

- [ ] Exactly 30 questions, IDs Q01–Q30 in order, each with a matching anchor.
- [ ] Exactly five distinct choices (A–E) per question.
- [ ] Exactly one defensible correct answer per question.
- [ ] 18 Medium / 12 Challenge overall; each block of five is 3 Medium + 2 Challenge.
- [ ] Tier labels appear only in the answer key.
- [ ] You solved every item again from the stem alone, without looking at your key, and the answers matched.
- [ ] Distractors are distinct and each reflects a plausible mistake.
- [ ] Answer positions are varied with no obvious pattern.
- [ ] Each question is independently solvable.
- [ ] Every diagram renders correctly in GitHub's Markdown preview and contains the information needed (dimensions, units, switch states, junctions, pivot positions).
- [ ] Q26–Q30 are fresh and not near-duplicates of Q01–Q25.
- [ ] `1. Learning.md` has 3–4 patterns, exactly one worked A–E example, and a link to `2. Doing.md`.
- [ ] Only your category's files (and its asset folder) are changed.

## Review, integration, and release roles

- **Subject reviewers** (math: M1–M5; science: S1–S5) can start as soon as any category PR opens. Solve every item from the stem **before** reading the key, record defects by question ID, and route fixes to the owning category PR or a focused follow-up PR. Final sign-off waits for all five category PRs in the subject.
- **Integration** owns the README calendar and the final-weekend mixed ordering. It can prepare the ordering immediately and verify links once authoring lands. Mixed sessions link to question IDs so each question keeps one canonical home; questions are never copied.
- **Release audit** runs after both subject reviews and integration are done. It confirms the totals, upgrades or verifies the calendar deep links, removes scaffold notices, and publishes the student-ready README.

## Category briefs

### M1 — Number theory

Directory: `Grade 9/1. Math/M1-number-theory/`

**Teach:**
- Find factors, multiples, and prime factorizations.
- Use divisibility rules (2, 3, 4, 5, 6, 8, 9, 10, 11) to test numbers and recover missing digits.
- Recognize GCF situations: splitting several totals into the greatest number of identical groups.
- Recognize LCM situations: matching totals from packs of different sizes, and recurring events that coincide.
- Decide which unknown is asked for (number of groups, items per group, or the shared total) and check it.

**Planned question families** (develop several; examples show the decisions to test):
- Identical groups from several totals (GCF), asking for the number of groups or the contents of each group.
- Matching totals bought in packs of different sizes (LCM), asking for the total or the number of packs.
- Recurring events that coincide: buses, blinking lights, rotating schedules, calendar days.
- Divisibility tests and missing-digit problems.
- Prime factorization and counting factors.
- Reverse problems: recover a number from a given GCF, LCM, or remainder condition.
- Remainders and leftovers when items are shared or packed.

**Model example:** Use 18 red tiles and 30 blue tiles to make the greatest number of identical mixed bags. Ask for bags (6), then tiles per bag (8). Change the setup to buying packs of 18 and 30 and ask for the smallest equal total of each colour (90). The numbers stay familiar while the role of the unknown changes.

**Boundaries:**
- Stay within whole numbers; no modular-arithmetic notation.
- Each item must force the student to choose between GCF and LCM reasoning rather than signalling it in the heading.

**Diagram approach:** Inline tables or labelled text.

### M2 — Geometry and measurement

Directory: `Grade 9/1. Math/M2-geometry-and-measurement/`

**Teach:**
- Read dimensions from a labelled diagram and identify which region is being measured.
- Distinguish radius from diameter; use circumference and circle area with the stated value of π.
- Find volume of rectangular prisms and cylinders, and separate water present, empty space, and total capacity.
- Work backward from a volume to a missing depth or dimension.
- Choose and convert units: cm, cm², cm³, mL, L.

**Planned question families** (develop several; examples show the decisions to test):
- Circle diagrams: radius, diameter, circumference, area, and half/quarter circles.
- Rectangular tank: water present, capacity remaining, total capacity.
- Reverse depth problems: depth after pouring a given volume into an empty or partly filled container.
- Cylindrical cup or bottle volume and capacity.
- Unit conversion between cm³, mL, and L.
- Composite figures: area versus perimeter of combined shapes.
- Scaling: effect of doubling a radius or a side on length, area, and volume.

**Model example:** Draw a rectangular tank with inside base 10 cm by 8 cm, inside height 12 cm, and water depth 5 cm. Ask for water present (400 cm³), capacity remaining (560 cm³), or water depth when an empty tank of that size receives 240 cm³ (3 cm). Include a separate circle-diagram family.

**Boundaries:**
- State the value of π in every circle item (for example, use 3.14, or leave the answer in terms of π).
- Displacement measurements from cylinder readings belong to S3; M2 may pour known volumes into containers.
- Diagrams must label inside dimensions when capacity is asked.

**Diagram approach:** Use labelled drawings or tables that state every dimension and unit. Mark inside dimensions explicitly.

### M3 — Algebra

Directory: `Grade 9/1. Math/M3-algebra/`

**Teach:**
- Translate a situation into an expression or equation.
- Substitute values into expressions, including with brackets and exponents.
- Solve one- and two-step linear equations and check by substitution.
- Match a rule to a table of values and a table to a rule.
- Change the unknown: use the same rule to find input from output.

**Planned question families** (develop several; examples show the decisions to test):
- Fixed fee plus rate per unit: choose the expression.
- Match a rule to a table, or a table to a rule.
- Reverse problems: find the input that produces a given output.
- Simplify expressions and combine like terms.
- Build and solve an equation from a word problem (ages, perimeter, consecutive numbers).
- Compare two plans and find where they cost the same.
- Direct substitution and order of operations.

**Model example:** A trip costs $4 plus $3 per kilometre. Ask which expression represents the price, which table matches the rule, or how far someone travelled for $25 (7 km).

**Boundaries:**
- Linear relationships only; squares may appear in substitution but not as equations to solve.
- Include direct algebra questions as well as applications.

**Diagram approach:** Inline tables or labelled text.

### M4 — Patterns and sequences

Directory: `Grade 9/1. Math/M4-patterns-and-sequences/`

**Teach:**
- Find constant differences and write the nth term of an arithmetic sequence.
- Spot ratios (geometric growth), second differences, and alternating or interleaved rules.
- Model growing diagrams and count the parts of the nth figure.
- Decide whether a target value belongs to a sequence, and at which position.
- Find missing terms in the middle of a sequence.

**Planned question families** (develop several; examples show the decisions to test):
- Arithmetic sequences: nth term and a far term.
- Geometric (multiplying) sequences.
- Second-difference sequences (differences that themselves grow).
- Interleaved or alternating sequences.
- Figure growth with sticks or tiles, with construction rules fully stated.
- Target membership: can this number appear, and where?
- Cyclic patterns: what is in position 100?
- Justification: which explanation correctly accounts for the rule?

**Model example:** A row of squares is made from sticks, each new square sharing one side. Ask how many sticks make 10 squares (31), whether 46 sticks can make a row (yes, 15 squares), or which explanation justifies the rule.

**Boundaries:**
- Give enough terms or construction information that exactly one rule fits; avoid sequences with several defensible continuations.

**Diagram approach:** Draw the first few figures and state the construction rule in words.

### M5 — Logic and constraints

Directory: `Grade 9/1. Math/M5-logic-and-constraints/`

**Teach:**
- Trace supplied rules forward from inputs to outputs.
- Recover possible inputs from observed outputs.
- Combine several constraints and eliminate impossible cases.
- Distinguish what could be true from what must be true.
- Decide whether given information is sufficient.

**Planned question families** (develop several; examples show the decisions to test):
- Indicator rules: abstract on/off inputs controlling lights by stated rules (limit to about one fifth of the bank).
- Ordering and line-up clues.
- Route or map restrictions: which stop must come first.
- Seating or grid placement.
- Scheduling with conflicts.
- Binary-style states: rows of on/off switches representing values.
- Sufficiency: which additional clue would determine the answer.

**Model example:** Given indicator rules, choose the one input arrangement that activates both. Given ordering clues, choose the only valid line-up. Given route restrictions, determine which destination must be visited first.

**Boundaries:**
- Rules are supplied abstractly; no electrical knowledge is needed. Electrical connectivity belongs to S4.
- The lightbulb puzzle must not dominate the category.

**Diagram approach:** Use tables of rules and states. For on/off puzzles, show each input as ON/OFF in a table.

### S1 — Ecology and ecosystems

Directory: `Grade 9/2. Science/S1-ecology-and-ecosystems/`

**Teach:**
- Identify roles relative to another organism: an animal can be predator to one and prey to another.
- Read arrow direction in food chains as the direction energy flows.
- Use producer, consumer, herbivore, carnivore, omnivore, decomposer, habitat.
- Identify resources (water, light, shelter, space, nutrients) and competition for them.
- Separate direct effects from indirect effects in a food web.

**Planned question families** (develop several; examples show the decisions to test):
- Predator and prey identification (its own family).
- Food chain ordering and arrow direction (its own family).
- Ecological resources: water, light, shelter, space (its own family).
- Food web removal and population effects, direct and indirect.
- Competition between organisms for a shared resource.
- Terminology applied in context.
- Reading a simple population table or graph.

**Model example:** Snails eat algae, fish eat snails, and herons eat fish. Ask which organism is both predator and prey in the described chain (fish), which sequence shows energy transfer, or which organism directly loses a food source if snails decline. Add separate resource examples involving water, light, or shelter.

**Boundaries:**
- Use plausible organisms but state the feeding relationships in the item; do not rely on outside knowledge of diets.

**Diagram approach:** Mermaid flowcharts work well for food chains and webs. Arrows point from the organism eaten to the eater.

### S2 — Cells, DNA, and inheritance

Directory: `Grade 9/2. Science/S2-cells-dna-and-inheritance/`

**Teach:**
- Use a labelled diagram to show where DNA is stored in a typical cell and how a gene is a stretch of DNA.
- Introduce nucleic acids and the four DNA bases. Apply the A–T and C–G pairing rules.
- Compare plant and animal cell structures (cell wall, chloroplast, membrane, nucleus).
- Separate inherited traits from acquired traits.
- Apply a simple inheritance rule that is supplied in the passage.
- Decide what an observation or experiment actually supports.

**Planned question families** (develop several; examples show the decisions to test):
- Labelled hierarchy diagrams: identify a highlighted gene, chromosome, or nucleus.
- Plant versus animal cell structures and functions.
- Inherited versus acquired traits.
- Passage-supplied inheritance rules (dominant/recessive stated in the item).
- Evidence and experiments: does the observation establish an inherited cause?
- DNA terminology, base pairing, and function in context.

**Model example:** Use the stated A–T and C–G rules to fill in missing labels on a short DNA ladder. Compare plant and animal cells by identifying a labelled structure and explaining its job.

**Boundaries:**
- Any inheritance rule must be stated in the item; do not assume prior knowledge of Punnett squares.
- Keep DNA at the level of its role in cells, base names and pairing, and simple traits. Supply any vocabulary or additional rule that an item needs.

**Diagram approach:** Use labelled cell drawings or a short DNA ladder when a visual helps the student locate a part or apply a rule.

### S3 — Matter, fluids, and temperature

Directory: `Grade 9/2. Science/S3-matter-fluids-and-temperature/`

**Teach:**
- Find an object's volume by displacement from two readings.
- Calculate density from mass and volume and compare objects.
- Predict floating and sinking by comparing density with the liquid's.
- State the direction of heat transfer (warmer to cooler).
- Separate final temperature from temperature change, including on graphs.

**Planned question families** (develop several; examples show the decisions to test):
- Displacement from two cylinder readings.
- Density calculation and comparison.
- Equal-volume objects with different masses (and equal-mass objects with different volumes).
- Floating and sinking.
- Direction of heat transfer between objects in contact.
- Cooling or heating curves: which was warmer versus which changed more.
- Optional, at most a few items: changes of state and temperature plateaus.

**Model example:** A cylinder contains 40 mL of water. A student fully submerges a stone without spilling water. The cylinder now reads 55 mL. What is the stone's volume? A. 15 cm³ B. 27.5 cm³ C. 40 cm³ D. 55 cm³ E. 95 cm³. Key: A. The stone displaces 55 − 40 = 15 mL. Choice D includes the original water. Extend to equal-volume objects with different masses, or two cooling curves where the warmer object and the object that cooled more need to be identified separately.

**Boundaries:**
- Use 1 mL = 1 cm³ and state the density of water when needed.
- Changes of state are optional and should not exceed a small share of the bank.

**Diagram approach:** Show cylinder readings and cooling data as labelled tables.

### S4 — Circuits and switches

Directory: `Grade 9/2. Science/S4-circuits-and-switches/`

**Teach:**
- Decide whether a closed path exists from one battery terminal to the other.
- Read open and closed switches on a shared path and on separate branches.
- Compare series and parallel arrangements.
- Infer which switches must, could, or cannot be closed from observed bulbs.
- Recognize conductors and insulators completing or breaking a path.

**Planned question families** (develop several; examples show the decisions to test):
- Single loop with one or more switches.
- Bulbs in series.
- Parallel branches with a master switch on the shared path.
- Which setting lights only a chosen bulb.
- Observed bulb states → which switch must be closed.
- Could versus must for switch states.
- Conductors and insulators placed in a gap.

**Model example:** Draw a battery, a master switch on the shared path, and two parallel branches, each with a bulb and switch. Ask which setting lights only bulb 2. Then show an observed bulb state and ask which switch must be closed.

**Boundaries:**
- S4 tests electrical connectivity. Abstract rule puzzles belong to M5.
- Every circuit must be drawn so each connection and junction is unambiguous; verify every option by tracing.

**Diagram approach:** Draw circuits as labelled schematics with a legend for open and closed switches, bulbs, batteries, and junctions.

### S5 — Forces and balance

Directory: `Grade 9/2. Science/S5-forces-and-balance/`

**Teach:**
- Identify the pivot and the turning direction of each load.
- Compare turning effects using load × distance from the pivot.
- Find a missing load or distance that balances a beam.
- Predict which side drops when a load or position changes.
- Read force arrows to decide whether forces are balanced.

**Planned question families** (develop several; examples show the decisions to test):
- Numerical beam balance: find the distance.
- Numerical beam balance: find the load.
- Which side drops after a change.
- Several loads on one side.
- Qualitative seesaw diagrams without numbers.
- Levers in everyday tools: pivot, load, and effort.
- Balanced versus unbalanced force arrows.

**Model example:** A 4-unit weight sits three equal marks left of the pivot on a weightless level beam. Where should a 2-unit weight go on the right to balance it? Six marks from the pivot. Move the first weight one mark toward the pivot and ask which side drops with the second weight unchanged (right).

**Boundaries:**
- State the beam assumptions clearly: ignore the beam’s own weight, use equally spaced marks, and hang loads at the marked positions. Put shared assumptions before the questions and state any exceptions in the individual item.

**Diagram approach:** Draw beams with numbered marks and a clearly labelled pivot.

