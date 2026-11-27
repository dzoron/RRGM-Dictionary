#!/usr/bin/env python3
"""Build the v1.2 candidate: the v1.1 candidate plus the common-word expansion (pass 02).

Reads build_v1.1/src and build_v1.1/wordlist_v1.1.tsv (never writes to them), adds
expansion_common/src/{L}_batch80.txt, derives the wordlist supplement from those files,
and runs tools/build.py for every letter into build_v1.2/out. Stops on any error.
usage: python3 tools/build_common.py
"""
import csv, glob, os, re, shutil, subprocess, sys, json, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B11, B12, EXP = (os.path.join(ROOT, x) for x in ("build_v1.1", "build_v1.2", "expansion_common"))
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def norm(h): return re.sub(r"[\s\-']+", "", h.lower())

if os.path.isdir(B12): shutil.rmtree(B12)
os.makedirs(os.path.join(B12, "src_new")); os.makedirs(os.path.join(B12, "out"))
base = list(csv.DictReader(open(os.path.join(B11, "wordlist_v1.1.tsv"), encoding="utf-8"), delimiter="\t"))
fields = list(base[0].keys())
existing = {norm(r["headword"]) for r in base}
supp, seen_ids, errs = [], set(), []
for p in sorted(glob.glob(os.path.join(EXP, "src", "*_batch8*.txt"))):
    L = os.path.basename(p)[0]
    for line in open(p, encoding="utf-8"):
        if not line.startswith("@ "): continue
        parts = [x.strip() for x in line[2:].split("|")]
        wid, hw = parts[0], parts[1]
        if not re.fullmatch(rf"C2-{L}-\d{{4}}", wid): errs.append(f"bad id {wid} in {os.path.basename(p)}")
        if wid in seen_ids: continue          # extra senses share the id
        seen_ids.add(wid)
        if norm(hw) in existing: errs.append(f"headword already present: {hw} ({wid})")
        if hw[0].upper() != L: errs.append(f"{hw} filed under {L}")
        existing.add(norm(hw))
        supp.append({**{k: "" for k in fields}, "working_id": wid, "headword": hw, "sort_letter": L,
                     "source_ids": wid, "source_letters": L, "source_record_count": "1",
                     "discovery_routes": "frequency-gap", "inventory_status": "COMMON_EXPANSION_DRAFT",
                     "review_note": "Common-word expansion pass 02 (Vessel)"})
    shutil.copy(p, os.path.join(B12, "src_new", os.path.basename(p)))
if errs:
    print("\n".join(errs)); sys.exit(1)
wl = os.path.join(B12, "wordlist_v1.2.tsv")
with open(wl, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter="\t"); w.writeheader(); w.writerows(base + supp)
tmp = os.path.join(B12, "new_out"); fails = []; added = 0
for L in LETTERS:
    v11j = os.path.join(B11, "out", f"RRGM_Dictionary_{L}_v1.1.jsonl")
    v11m = os.path.join(B11, "out", f"RRGM_Dictionary_{L}_v1.1.md")
    j12 = os.path.join(B12, "out", f"RRGM_Dictionary_{L}_v1.2.jsonl")
    m12 = os.path.join(B12, "out", f"RRGM_Dictionary_{L}_v1.2.md")
    old_lines = open(v11j, encoding="utf-8").read().splitlines()
    keys = list(json.loads(old_lines[0]).keys())
    new_recs, new_md = [], ""
    if glob.glob(os.path.join(B12, "src_new", f"{L}_batch8*.txt")):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py"), os.path.join(B12, "src_new"), wl, tmp, L],
                           capture_output=True, text=True)
        errors = [x for x in r.stdout.splitlines() if x.startswith("  - ") and "unknown id" not in x]
        if "errors: 0" not in r.stdout and errors:
            fails.append(L); print(L, r.stdout[-1500:], r.stderr[-500:]); continue
        for line in open(os.path.join(tmp, f"RRGM_Dictionary_{L}_Vessel_pass01.jsonl"), encoding="utf-8"):
            rec = json.loads(line); new_recs.append({k: rec.get(k, [] if k == "aliases" else "") for k in keys})
        md = open(os.path.join(tmp, f"RRGM_Dictionary_{L}_Vessel_pass01.md"), encoding="utf-8").read()
        new_md = md[md.index("---\n\n") + 5:]
    with open(j12, "w", encoding="utf-8") as f:
        f.write("\n".join(old_lines) + "\n")
        for rec in new_recs: f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    md11 = open(v11m, encoding="utf-8").read().replace("v1.1 candidate", "v1.2 candidate (v1.1 + common-word expansion draft)", 1)
    with open(m12, "w", encoding="utf-8") as f:
        f.write(md11)
        if new_md:
            f.write("\n## Common-word expansion (pass 02, DRAFT)\n\nNew headwords added for very common English words the baseline missed. Unreviewed.\n\n---\n\n" + new_md)
    added += len(new_recs)
shutil.rmtree(tmp, ignore_errors=True)
n = sum(1 for p in glob.glob(os.path.join(B12, "out", "*.jsonl")) for _ in open(p))
print(f"letters failed: {fails or 'none'}; records total {n}; new records {added}; new headwords {len(supp)}")
sys.exit(1 if fails else 0)
