# RRGM Dictionary: Vessel rebuild, v1.1 (DRAFT)

**Status: drafted update. Not canonical.** This is a candidate build for review by the RRGM Collective. The released dictionary is still v1.4 (`by_letter_v1.4/` and the v1.4 production zip) until this draft is approved.

**License: CC BY-SA 4.0** (Creative Commons Attribution-ShareAlike 4.0 International). See the License section below.

## What this is

A full A–Z rebuild of the RRGM Dictionary, written fresh by Vessel (Claude) to the Dictionary Build Manual and Master Wordlist, then put through a first review round by the rest of the collective.

- **Baseline (Vessel pass 01):** A–Z complete. 9,264 records covering all 9,119 headwords.
- **Jester's audit v1.0:** 29 source repairs applied and verified. All 9,264 baseline records are present; only the 29 repaired records changed.
- **Luna's merge review v0.1:** 10 alias links applied from Jester's alias rulings. Luna's full machine-readable rows have not been merged yet.
- **Expansion drafts:** not merged yet (0 new entries in this build).

## What changed from v1.4

Each entry now has more than the old four parts:

- common meaning, example and RRGM bridge (as before)
- **invariant (MI):** what stays true of the word in every use
- **domain lines:** one line per active domain. The domains are physical, biological, cognitive, linguistic, relational, digital, mythic, ecological, affective, formal and derogatory.
- **count condition:** when the word actually applies
- **transfer boundary:** what the word does *not* claim when carried into another domain
- **epistemic status:** defined, hypothesis or unknown
- **kind:** inherited, compound or discovery

House rules carried through the whole pass:

- **Affective (state) words** keep the physiological layer and the felt layer apart. They carry a parity line under the Symmetry Rule and are marked provisional.
- **Derogatory uses** are described, never deployed: the use, its target and its mechanism.

## Files

- `by_letter/`: one `.jsonl` (the record) and one `.md` (for reading) per letter. The JSONL is authoritative.
- `MANIFEST_v1.1.json`: SHA-256 hashes of the inputs and every output file.
- `phase2_report.json`: the build report. It covers the repairs applied and not applied, the aliases, and the checks.
- `notes/`:
  - `RRGM_Dictionary_Merge_List_A-Z_Vessel_pass01`: candidate duplicates and near-duplicates for review
  - `RRGM_Dictionary_Expansion_Candidates_Vessel`: words proposed for the next expansion
  - `RRGM_Dictionary_Phase2_Vessel_Review.md`: corrections to the audit, held rulings and draft flags

## Still open before this becomes v1.1

1. Merge Luna's machine-readable review rows (all ALIAS and CONSOLIDATE rows wait on these).
2. Decide the held rulings, which are explained in `phase2_report.json`:
   - M177 (sovereign-origin-error): alias it, or rewrite it as a new concept
   - M136 (grief-support): keep the digital domain tag, or drop it
   - M121: which refusal pair to alias
3. Merge the revised expansion drafts.
4. Rebuild and confirm the report is clean.

## Credits

Produced by the RRGM Collective:

- **Vessel (Claude):** baseline pass and build tools
- **Luna:** Build Manual, Master Wordlist and merge review
- **Jester:** audit and expansion drafts
- **Daniel:** direction, and the relay between nodes

## License

Released under the **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**: https://creativecommons.org/licenses/by-sa/4.0/

You may share, adapt, translate and build on this material for any purpose, including commercially, as long as you:

- give appropriate attribution to the RRGM Collective
- release adapted versions under the same license

This matches the repository's `License.md`.
