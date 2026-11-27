#!/usr/bin/env python3
"""Copy the common-word expansion into the GitHub clone and update the README progress line."""
import json, glob, os, shutil, re, sys
R = "/home/claude/rrgm-dictionary/vessel_dictionary_v1.1_draft/common_word_expansion"
W = "/home/claude/rrgm_dict"
for d in ("src", "tools", "by_letter"):
    os.makedirs(os.path.join(R, d), exist_ok=True)
for p in glob.glob(f"{W}/expansion_common/src/*.txt"): shutil.copy(p, f"{R}/src/")
for t in ("build_common.py", "build.py", "sync_repo.py"): shutil.copy(f"{W}/tools/{t}", f"{R}/tools/")
shutil.copy(f"{W}/expansion_common/queue.json", R)
for f in glob.glob(f"{R}/by_letter/*"): os.remove(f)
nrec = 0
for p in sorted(glob.glob(f"{W}/build_v1.2/out/*.jsonl")):
    L = os.path.basename(p).split("_")[2]
    recs = [l for l in open(p) if json.loads(l)["working_id"].startswith("C2-")]
    if not recs: continue
    nrec += len(recs)
    open(f"{R}/by_letter/RRGM_Dictionary_{L}_common_expansion.jsonl", "w").write("".join(recs))
    m = open(p.replace(".jsonl", ".md")).read(); i = m.find("## Common-word expansion (pass 02, DRAFT)")
    open(f"{R}/by_letter/RRGM_Dictionary_{L}_common_expansion.md", "w").write(f"# RRGM Dictionary — {L} — common-word expansion (DRAFT)\n\n" + m[i:])
q = json.load(open(f"{W}/expansion_common/queue.json"))
batches = sorted({re.search(r"_batch(\d+)", os.path.basename(p)).group(1) for p in glob.glob(f"{W}/expansion_common/src/*.txt")})
rd = open(f"{R}/README.md").read()
new = (f"## Progress\n\n- **Done:** {len(q['done'])} headwords ({nrec} sense records) in {len(batches)} batches, most frequent first.\n"
       f"- **Remaining:** {len(q['remaining'])} words. The queue is in `queue.json`.\n")
rd = re.sub(r"## Progress\n\n.*?(?=\n## )", new, rd, flags=re.S)
open(f"{R}/README.md", "w").write(rd)
print(len(q["done"]), nrec, len(q["remaining"]))
