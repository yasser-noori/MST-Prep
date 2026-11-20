---
name: Category authoring
about: Build one category's learning page and 30 A–E drills
title: "[<ID>] Build <category name> learning page and 30 MCQs"
labels: ["authoring", "ready-to-claim"]
assignees: []
---

## Owned files

- `Grade 9/<subject>/<ID>-<name>/1. Learning.md`
- `Grade 9/<subject>/<ID>-<name>/2. Doing.md`
- Optional: `Grade 9/assets/<ID>/` for labelled diagrams

Do not edit any other file. The integration agent owns the README.

## Evidence

**Original recollection:**
-

**Follow-up recognition:**
-

**Extension:**
-

## Category brief

<!-- Copy the category brief from CONTRIBUTING.md: teach, families, model example, boundaries. -->

## Contract

- `1. Learning.md`: 3–4 core patterns (clue, decision, check), exactly one worked A–E example with the decisive step and the most tempting wrong answer, link to `2. Doing.md`.
- `2. Doing.md`: exactly 30 original A–E drills, `<ID>-Q01`–`<ID>-Q30`, with `<a id="<id>-qNN"></a>` anchors.
- 18 Medium + 12 Challenge; six blocks of five, each 3 Medium + 2 Challenge in varied order.
- Tier labels only in the answer key at the bottom.
- Q26–Q30 are fresh, final-weekend items with no near-duplicates earlier.

## Checklist

- [ ] Exactly five distinct choices per question
- [ ] Exactly one defensible correct answer per question
- [ ] Each question independently solvable
- [ ] Distractors distinct and based on real mistakes
- [ ] Answer key re-solved from stems and accurate
- [ ] Diagrams render in GitHub preview and contain all needed information
- [ ] Answer letters varied with no pattern

## How to submit

Follow [CONTRIBUTING.md](../../CONTRIBUTING.md). Open one PR from `content/<lowercase-dir>` with `Closes #<this issue>` in the body.
