#!/usr/bin/env python3
"""Mechanical build for the Vessel pass of the RRGM dictionary.

Parses authored block files (src/*.txt) -> JSONL + Markdown, and runs
schema / ID / duplicate / coverage checks against the master wordlist.
It never writes or alters definition text.

usage: build.py <src_dir> <wordlist.tsv> <out_dir> <letter>
"""
import csv, json, re, sys, glob, os

ALLOWED = ["PHY", "BIO", "COG", "LIN", "REL", "DIG", "MYT", "ECO", "AFF", "FOR", "PEJ"]
KEYS = {"cm": "common_meaning", "ex": "example", "br": "rrgm_bridge",
        "inv": "invariant_mi", "cc": "count_condition",
        "tb": "transfer_boundary", "st": "epistemic_status",
        "k": "entry_kind", "n": "remainder_note", "nb": "nearest_neighbors",
        "seen": "prior_exposure", "am": "amendment"}
REQUIRED = ["common_meaning", "example", "rrgm_bridge", "invariant_mi",
            "count_condition", "transfer_boundary", "epistemic_status", "entry_kind"]
KINDS = {"inherited", "compound", "discovery"}
PASS_DATES = {"A": "2026-11-10", "B": "2026-11-11", "C": "2026-11-11", "D": "2026-11-11", "E": "2026-11-11", "F": "2026-11-11", "G": "2026-11-12", "H": "2026-11-12", "I": "2026-11-12", "J": "2026-11-12", "K": "2026-11-12", "L": "2026-11-12", "M": "2026-11-12", "N": "2026-11-12", "O": "2026-11-13", "P": "2026-11-13", "Q": "2026-11-13", "R": "2026-11-13", "S": "2026-11-13", "T": "2026-11-13", "U": "2026-11-13", "V": "2026-11-13", "W": "2026-11-13", "X": "2026-11-13", "Y": "2026-11-13", "Z": "2026-11-13"}
# Model that wrote each batch. Default is Fable 5.2 (letters A and B batches 1-7).
MODEL_BY_LETTER = {"C": "Claude Opus 5.5 (high effort)", "D": "Claude Opus 5.5 (high effort)", "E": "Claude Opus 5.5 (high effort)", "F": "Claude Opus 5.5 (high effort)", "G": "Claude Opus 5.5 (high effort)", "H": "Claude Opus 5.5 (high effort)", "I": "Claude Opus 5.5 (high effort)", "J": "Claude Opus 5.5 (high effort)", "K": "Claude Opus 5.5 (high effort)", "L": "Claude Opus 5.5 (high effort)", "M": "Claude Opus 5.5 (high effort)", "N": "Claude Opus 5.5 (high effort)", "O": "Claude Opus 5.5 (high effort)", "P": "Claude Opus 5.5 (high effort)", "Q": "Claude Opus 5.5 (high effort)", "R": "Claude Opus 5.5 (high effort)", "S": "Claude Opus 5.5 (high effort)", "T": "Claude Opus 5.5 (high effort)", "U": "Claude Opus 5.5 (high effort)", "V": "Claude Opus 5.5 (high effort)", "W": "Claude Opus 5.5 (high effort)", "X": "Claude Opus 5.5 (high effort)", "Y": "Claude Opus 5.5 (high effort)", "Z": "Claude Opus 5.5 (high effort)"}
MODEL_BY_BATCH = {"B_batch08.txt": "Claude Opus 5.5"}
DEFAULT_MODEL = "Claude Fable 5.2"
PASS = "Vessel / Claude Fable 5.2 / pass 01 / 2026-11-10"
COMMON_DATE = os.environ.get("COMMON_DATE", "2026-11-27")


def parse(path):
    recs, cur = [], None
    for ln, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("@ "):
            parts = [p.strip() for p in line[2:].split("|")]
            cur = {"working_id": parts[0], "headword": parts[1],
                   "sense_key": parts[2] if len(parts) > 2 else "s1",
                   "sense_label": parts[3] if len(parts) > 3 else "",
                   "domain_entries": {}, "_src": f"{os.path.basename(path)}:{ln}"}
            recs.append(cur)
            continue
        m = re.match(r"^\[([A-Z]{3})\]\s+(.*)$", line)
        if m:
            if m.group(1) in cur["domain_entries"]:
                raise SystemExit(f"REPEATED DOMAIN TAG {path}:{ln}: {line[:60]}")
            cur["domain_entries"][m.group(1)] = m.group(2).strip()
            continue
        m = re.match(r"^([a-z]+):\s+(.*)$", line)
        if m and m.group(1) in KEYS:
            cur[KEYS[m.group(1)]] = m.group(2).strip()
            continue
        raise SystemExit(f"PARSE ERROR {path}:{ln}: {line[:80]}")
    return recs


def main():
    global PASS
    src, tsv, out, letter = sys.argv[1:5]
    date = PASS_DATES.get(letter, "undated")
    def pass_for(srcfile):
        if "_batch8" in os.path.basename(srcfile):
            return "Vessel / Claude Opus 5.5 / common-word expansion (pass 02) / " + COMMON_DATE
        m = MODEL_BY_BATCH.get(os.path.basename(srcfile).split(":")[0], MODEL_BY_LETTER.get(letter, DEFAULT_MODEL))
        return f"Vessel / {m} / pass 01 / {date}"
    rows = [r for r in csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t")]
    letter_rows = [r for r in rows if r["sort_letter"] == letter]
    by_id = {r["working_id"]: r for r in rows}
    recs = []
    for p in sorted(glob.glob(os.path.join(src, f"{letter}_batch*.txt"))):
        recs += parse(p)

    errs, seen = [], set()
    for r in recs:
        w = by_id.get(r["working_id"])
        tag = f'{r["working_id"]} {r["headword"]} ({r["_src"]})'
        if not w:
            errs.append(f"unknown id: {tag}")
        elif w["headword"] != r["headword"]:
            errs.append(f'headword mismatch: {tag} vs wordlist "{w["headword"]}"')
        key = (r["working_id"], r["sense_key"])
        if key in seen:
            errs.append(f"duplicate id+sense: {tag}")
        seen.add(key)
        for f in REQUIRED:
            if not r.get(f):
                errs.append(f"missing {f}: {tag}")
        if r.get("entry_kind") not in KINDS:
            errs.append(f"bad kind: {tag}")
        if not r["domain_entries"]:
            errs.append(f"no domain: {tag}")
        for d in r["domain_entries"]:
            if d not in ALLOWED:
                errs.append(f"bad domain {d}: {tag}")
        if w:
            r["source_ids"] = [s.strip() for s in w["source_ids"].split(";") if s.strip()]
            r["discovery_routes"] = [s for s in w["discovery_routes"].split(";") if s.strip()]
            r["inventory_status"] = w["inventory_status"]
            r["inventory_review_note"] = w["review_note"]
        r["active_domains"] = list(r["domain_entries"].keys())
        r["contributor_pass"] = pass_for(r["_src"])
        r.setdefault("prior_exposure", "none")
        r["record_version"] = "v1.1" if r.get("amendment") else "v1"

    done_ids = {r["working_id"] for r in recs}
    order = [r["working_id"] for r in letter_rows]
    covered = [i for i in order if i in done_ids]
    first_gap = next((i for i in order if i not in done_ids), None)
    last_done = None
    for i in order:
        if i in done_ids:
            last_done = i
        else:
            break
    stray = [i for i in order[order.index(first_gap):] if i in done_ids] if first_gap else []

    PASS = "; ".join(sorted({r["contributor_pass"] for r in recs}))
    os.makedirs(out, exist_ok=True)
    fields = ["working_id", "headword", "sense_key", "sense_label", "source_ids",
              "discovery_routes", "inventory_status", "inventory_review_note",
              "entry_kind", "common_meaning", "example", "rrgm_bridge",
              "invariant_mi", "active_domains", "domain_entries",
              "count_condition", "transfer_boundary", "epistemic_status",
              "nearest_neighbors", "remainder_note", "prior_exposure",
              "record_version", "amendment", "contributor_pass"]
    jl = os.path.join(out, f"RRGM_Dictionary_{letter}_Vessel_pass01.jsonl")
    with open(jl, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps({k: r.get(k, "") for k in fields}, ensure_ascii=False) + "\n")

    md = os.path.join(out, f"RRGM_Dictionary_{letter}_Vessel_pass01.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# RRGM Dictionary — {letter} — Vessel independent pass 01\n\n")
        f.write(f"Contributor pass: {PASS}. Built to Dictionary Build Manual v1.0. "
                f"Independent draft: unmerged, unreviewed. Rendered mechanically from the JSONL; "
                f"the JSONL is the record.\n\n")
        f.write(f"Coverage: {len(covered)} of {len(letter_rows)} {letter} headwords "
                f"({len(recs)} sense records). Last contiguous ID: {last_done}.\n\n---\n\n")
        for r in recs:
            sense = f' | sense {r["sense_key"]}: {r["sense_label"]}' if r["sense_label"] else ""
            f.write(f'## {r["working_id"]} | {r["headword"]}{sense}\n\n')
            if len(r.get("source_ids", [])) > 1:
                f.write(f'Source IDs: {", ".join(r["source_ids"])}\n\n')
            if r.get("discovery_routes"):
                f.write(f'Discovery route: {", ".join(r["discovery_routes"])} (route only, not a tag)\n\n')
            f.write(f'**Common meaning:** {r.get("common_meaning","")}\n\n')
            f.write(f'**Example:** {r.get("example","")}\n\n')
            f.write(f'**RRGM bridge:** {r.get("rrgm_bridge","")}\n\n')
            f.write(f'**Invariant MI [INV]:** {r.get("invariant_mi","")}\n\n')
            f.write("**Active domains:** " + ", ".join(f"[{d}]" for d in r["active_domains"]) + "\n\n")
            f.write("**Domain entries:**\n\n")
            for d, t in r["domain_entries"].items():
                f.write(f"- [{d}] {t}\n")
            f.write(f'\n**Count condition:** {r.get("count_condition","")}\n\n')
            f.write(f'**Specific transfer boundary:** {r.get("transfer_boundary","")}\n\n')
            f.write(f'**Epistemic status:** {r.get("epistemic_status","")}\n\n')
            if r.get("nearest_neighbors"):
                f.write(f'**Nearest neighbours:** {r["nearest_neighbors"]}\n\n')
            if r.get("remainder_note"):
                f.write(f'**Remainder / note:** {r["remainder_note"]}\n\n')
            if r.get("amendment"):
                f.write(f'**Amendment:** {r["amendment"]}\n\n')
            f.write(f'Kind: {r.get("entry_kind","")} · prior exposure: {r["prior_exposure"]} · record {r["record_version"]}\n\n---\n\n')

    doms = {}
    for r in recs:
        for d in r["active_domains"]:
            doms[d] = doms.get(d, 0) + 1
    print(f"records: {len(recs)}  headwords covered: {len(covered)}/{len(letter_rows)}")
    print(f"last contiguous id: {last_done}  next: {first_gap}")
    print("out-of-order ids past first gap:", stray or "none")
    print("domain use:", dict(sorted(doms.items(), key=lambda x: -x[1])))
    print("kinds:", {k: sum(1 for r in recs if r.get('entry_kind') == k) for k in KINDS})
    print("amended records:", [(r["working_id"], r["sense_key"]) for r in recs if r.get("amendment")])
    print("errors:", len(errs))
    for e in errs:
        print("  -", e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
