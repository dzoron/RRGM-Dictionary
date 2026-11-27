# Common-word expansion (pass 02): DRAFT

**Status: in progress, unreviewed.** These are new headwords for very common English words that the baseline missed, such as woman, music, car, business and week. The gap was not intentional.

**License: CC BY-SA 4.0**, the same as the rest of the repository.

## How the list was made

1. Every headword in the v1.1 draft (9,119) was compared against the 40,000 most frequent English words, using the `wordfreq` frequency data.
2. A word counted as missing only if neither it nor its base form (for example "walk" for "walked") was already a headword.
3. The run covers words with a Zipf frequency of 4 or above, about 2,460 words. Personal names, brand names and stray fragments were removed, leaving **2,396 words**.
4. Words are written in order of frequency, most common first.
5. Headwords use US spelling, the baseline's convention. UK spellings whose US form is already a headword or is queued (centre, colour, behaviour, programme and others) are skipped. The skipped ones are listed in `queue.json`.

## Progress

- **Done:** 300 headwords (309 sense records) in 5 batches, most frequent first.
- **Remaining:** 2079 words. The queue is in `queue.json`.

## Entry format

New entries use the same template and build checks as the baseline:

- **IDs:** `C2-{letter}-{nnnn}`, so they never collide with baseline IDs.
- **Kind:** `discovery`.
- **Route:** `frequency-gap`.
- **Inventory status:** `COMMON_EXPANSION_DRAFT`.

The house rules carry over:

- Affective words keep a parity line and are marked provisional.
- Vulgar and derogatory uses are described, never deployed.
- Sensitive words are flagged in the queue for extra care.

## Files

- `by_letter/`: the new records only, one `.jsonl` and one `.md` per letter.
- `src/`: the authored entries (`{L}_batch80.txt`), which are the source of truth.
- `tools/build_common.py`: builds the v1.2 candidate. It takes the v1.1 build, adds these entries, checks IDs, headwords and schema, and stops on any error. `tools/build.py` is the baseline build, with a pass label added for these batches.
- `queue.json`: the words done so far and the words remaining, with frequencies.
