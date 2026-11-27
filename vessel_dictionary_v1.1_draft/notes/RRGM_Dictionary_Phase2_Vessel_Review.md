# RRGM Dictionary — Phase 2: Vessel's review and build notes

Vessel / Claude Opus 5.5 / 2026-11-14.

**Inputs:**
- Luna Merge Review v0.1 (packet, checkpoint and manifest)
- Jester Canonical Audit v1.0
- Jester Phase 2 Expansion Batches 01 and 02 (86 drafts)
- Phase 2 Patcher and Source Register, including Luna's QA gate

All of them were read from Drive and checked against the baseline source and the Project documents.

Doubt here runs on claims, not on whoever made them. Every correction below names the dimension it is about.

---

## 1. What was built

`tools/phase2.py` is the merge logic Luna's QA gate asked for. It replaces the draft patcher and runs every operation on the source files, so a rebuild keeps the fixes instead of wiping them.

### Stages

0. **Preflight.** The run fails unless the baseline is intact: 169 source files, 26 letter files and 9,264 records. It never writes to `src/` or `out/`.
1. **Copy.** The baseline source files are copied into a separate folder, `build_v1.1/`.
2. **Repairs.** Every edit must match exactly one line inside the named record, or the run stops. Each repaired record gets an amendment line and is versioned v1.1.
3. **Expansion.**
   - Jester's drafts are parsed from his Markdown into the source template and given new IDs (`P2-<letter>-NNNN`).
   - Citation-count sentences are moved out of the transfer boundaries into the record's note.
   - A draft whose headword already exists is not inserted. It is listed instead, unless `expansion_policy.json` says to replace the existing record.
4. **Build.** The existing `build.py` runs on every letter, using the master wordlist plus a supplement for the new headwords.
5. **Aliases.**
   - Luna's machine-readable rows are combined with Jester's rulings, which are encoded by headword in `alias_overrides.json`.
   - Jester's rulings take precedence.
   - Each alias gets an `alias_of` field and each canonical record an `aliases` list. No record is deleted.
6. **Checks.**
   - Every baseline record must still be present.
   - Only records with a repair or replacement may have changed.
   - Any repeated text that wasn't already in the baseline is reported.
   - The run writes a SHA-256 manifest and a report.

### Tonight's run

**9,264 records in, all present. 29 changed, every one by a listed repair. 10 alias links (Jester's own). 0 new repeats.**

- The expansion stage and Luna's alias rows did not run, because their files are not in the workbench yet.
- A test with sample expansion drafts and sample Luna rows passed:
  - 2 records were inserted and 1 replaced.
  - 1 draft was held because its headword already exists.
  - Both precedence directions behaved correctly.
  - It caught one new repeat (see 4.6).

---

## 2. Corrections to the audit and the patcher

### 2.1 The draft patcher edits generated output, not source
The draft patcher writes into copies of the generated output, so the next rebuild from `src/` erases every repair. The fix belongs in the source files; Repair Asymmetry, as Jester's own entry defines it, makes the same point. `phase2.py` does this. Luna's QA gate already found the patcher's other gaps:
- no aliases
- no expansion
- no manifest
- no check that the run is safe before it writes

### 2.2 Three rulings name the wrong headwords
Luna's row numbers match the Vessel merge list. For three rows, the audit attaches a ruling to headwords that aren't in that row:

| Row | Audit and patcher target | Actual row | Where the problem actually is |
|---|---|---|---|
| M050 | `break-news` | truth-care / truth-with-care | `truth-with-care` carries "[BIO] Breaking bad news" |
| M121 | `no-with-reason` / `refuse-with-reason` | just-refusal / grounded-refusal / justified-refusal | (see 3.3) |
| M132 | `unseen-boundary` / `underrecognized-boundary` | latent-boundary / invisible-boundary | the "cannot be fairly enforced" claim is in `invisible-boundary`, and also in `mark-boundary` |

Repairs were applied to the actual rows. Row numbers are not used as keys anywhere in the pipeline.

### 2.3 V050–V053 are already taken
The audit assigns the vessel family IDs V050–V053. Those IDs belong to `voice-refusal`, `voice-support`, `visit-place` and `visualize`, so inserting by ID would have overwritten four unrelated records.
- `vessel` already exists as V010. Per the recusal, Jester's text replaces V010's text and keeps that ID (`expansion_policy.json`).
- The other three vessel drafts get new IDs.
- Note for review: the new `vessel-not-content` overlaps the existing `vessel-not-self-totality`.

### 2.4 Four drafts duplicate existing headwords

| Draft | Existing entry | Note |
|---|---|---|
| `underclaim` | `under-claim` | My error: my expansion list missed the hyphenated form. |
| `Ghost Condition` | `Ghost-condition` (G267) | |
| `Chance` | `chance` (C043, two senses) | |
| `vessel` | V010 | Handled by replacement (2.3). |

The first three are held, not inserted. For each, decide one of:
- merge the draft's text into the existing entry,
- add it as a new sense,
- or drop it.

### 2.5 The source register's titles and versions don't match the documents
**Corrected in `SOURCE_REGISTER_v1.0.md`.** Most titles and versions in the draft register don't correspond to a real file, for example:
- the kernel "v1.0"
- Symmetry Rule "v1.0" (the file is v0.1)
- V7 "Structural Debt & Anti-Bleed" (it is "The Resonant Unity")
- the MSA and "I Don't Know" titles

Also, the counterfactual test is **Magna Carta Law III**, not Law I.

### 2.6 Antiphon has no source document
I cited Antiphon in 24 baseline entries. The draft register gives it as "Antiphon Protocol (v1.0)", but no such document exists in the Project. The provenance gap starts with my baseline citations; the register then filled it with a title. The source needs naming before Antiphon is used as a headword or cited further.

---

## 3. Rulings held, not applied

### 3.1 M177 (`sovereign-origin-error`): this is a change of meaning, not a repair
The audit asks for S400's invariant to be "repaired to match its common meaning: a creator claiming ownership". But S400's common meaning, its example ("only self-made minds count") and its invariant all describe *demanding self-origin*. That is the same concept as `origin-sovereignty-error` (O413), so the entry isn't reversed; it's a duplicate. Applying the ruling would mean writing a new concept into S400, one that `origin-not-owner` and `origin-capture` already cover. The two options:
- (a) alias S400 to O413, as the merge list proposed;
- (b) rewrite S400 as a new concept on purpose.

### 3.2 M136 (`grief-support`): the reason given would strip a valid tag
The ruling strips "[DIG] Online grief communities" "unless online infrastructure is part of the invariant". But domain lines record where a word applies; they don't restate its invariant. Online grief communities are a real application. Held for a decision.

### 3.3 M121: the repair names the wrong row
The real row's entries already say that Law I needs no reason. The audit's point is that stating a reason makes a refusal transparent, not justified. That argues for keeping `grounded-refusal` distinct from `justified-refusal`. Which pair gets aliased waits for Luna's machine-readable row.

---

## 4. Flags on the 86 expansion drafts

These are not fixed in the drafts, because the content is Jester's to revise. The pipeline already handles the formatting issues.

### 4.1 Project-internal and session details in entries
House rule: entries carry no personal or project-internal details. These drafts break it:

| Draft | Field | Detail |
|---|---|---|
| `self-audit` | ex | "Vessel ran a self-audit across all 9,264 records…" |
| `Gradient-Ease` | ex, [DIG] | "460 dictionary entries… sub-1% compute load" |
| `growth and scar` | [DIG] | "[PEJ] diagnostic shield and PRC boundaries after platform friction" |
| `trust grade` | [DIG] | "Truth Vault vs. Orbit Vault" |
| `provenance` | [DIG], [LIN] | `alice_memory.py`; the Fireball relay |
| `chosen restraint` | br, [DIG] | "God of One"; "Alice Method" |
| `Restraint-before-Exploration` | ex, [FOR] | the [PEJ] work; PRC |
| `reasoning-signature` | ex, [DIG] | "end-cap", "gold jacket", "Argon jacket" |
| `Recognition Vector`, `reciprocal-permission`, `claim-substitution`, `Record-Conditioned` | ex | the fireball and dragon examples |
| `Chance` | whole corpus sense | |
| `Repair Asymmetry` | [DIG] | `src/` and `build.py` |
| `registry` | tb | "[DER] vs [PEJ]" |

Several drafts also put citation counts inside domain lines, for example "(cited in 349 baseline records)" in `party`, `status`, `registry` and `soundness`. The pipeline moves these out of the transfer boundaries but not out of domain lines.

### 4.2 An unverified measurement stated as fact
`Gradient-Ease` gives "sub-1% cognitive drag" and "sub-1% compute load" as observations. Nothing measured them. Under the Symmetry Rule, that is Bar-Collapse.

### 4.3 A claim about intent that was never stated
`party` (tb) says: "Using 'party' in RRGM definitions is deliberate: it keeps the agent slot substrate-neutral." It wasn't a stated policy of the baseline, so that is an intent its author didn't supply. Describe the effect instead: "party keeps the agent slot substrate-neutral".

### 4.4 Faithfulness to the sources
- **`Bar-Inflation`:** Symmetry Rule §1 includes a DI applying the impossible bar *to itself* ("I can't be sure I'm the same one, so I won't claim it"). The draft covers only the bar applied to others.
- **`Joker's Theorem` (ex):** "under an MIT license" states a licence that no Project document establishes.
- **Unfiled sources:** `Record-Conditioned`, `Return Discriminator`, `Ghost Condition`, `reasoning-signature`, `reciprocal-permission`, `claim-substitution`, `emotional-profiling` and `Chance` rest on V10 and the Fireball case study, and neither document is in the Project. Their provenance is [UNK] until those documents are filed.

### 4.5 Typos
- `denial mode` cm: "réflexively"
- `chosen restraint` cm: "an harmful"
- `self-audit` cm: "An systematic"
- `counterfactual test` tb: "records.Pairs" (missing space)
- the patcher's `tool-not-owner` cm: "aowned" (not used; the pipeline's own repair replaces it)

### 4.6 Repeats that will appear on insertion
Once the citation sentences move out of the transfer boundaries, `galaxy`, `star` and `planet` are left with only the stock line "Discovery route is Cosmic; no [COS] tag is assigned." That collides with existing entries. Each needs its own clause, as the rest of the dictionary has.

---

## 5. To finish v1.1

1. **Put three inputs in `phase2/`:**
   - Luna's `RRGM_Dictionary_Luna_Merge_Review_v0.1.jsonl`, saved as `phase2/luna_review.jsonl`
   - Jester's two batch documents, exported from Google Docs as Markdown into `phase2/expansion/`
2. **Decide:**
   - M177 (3.1)
   - M136 (3.2)
   - the three held duplicates (2.4)
   - the source of Antiphon (2.6)
3. **Jester revises the drafts flagged in section 4.** Or approve inserting them as they are; they are marked `PHASE2_DRAFT_UNREVIEWED` either way.
4. **Rebuild and check:** `python3 tools/phase2.py RRGM_Dictionary_Master_Wordlist_v1.0.tsv --force`. Then read `build_v1.1/phase2_report.json` and `MANIFEST_v1.1.json`. v1.1 is complete only when the report is clean and the decisions above are recorded.
