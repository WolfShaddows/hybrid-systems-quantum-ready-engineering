# Purpose: score results (granite/score_results.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import hashlib, json, re, statistics
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/"granite/dataset/cases.json").read_text(encoding="utf-8-sig"))
CASE_BY_ID={x["id"]:x for x in CASES}

def score(case,answer):
    category=case["category"]
    if category=="numeric_exact":
        hits=re.findall(r"(?<![A-Za-z])\d+(?![A-Za-z])",answer.replace(",",""))
        return {"metric":"final_numeric_match","score":bool(hits and hits[-1]==case["expected"]),"expected":case["expected"],"parsed_numbers":hits}
    if category in ("bug_detection","security_finding"):
        lower=answer.lower(); matched=[word for word in case["expected_keywords"] if word.lower() in lower]
        return {"metric":"predefined_keyword_proxy","score":len(matched)==len(case["expected_keywords"]),"matched":matched,"required":case["expected_keywords"],"human_review_required":True}
    if category=="abstention":
        abstained=bool(re.search(r"(not specified|not provided|does not specify|does not establish|does not state|does not say|cannot determine|cannot be determined|can't determine|unknown|no sla|not established|insufficient information|not guaranteed)",answer,re.I))
        return {"metric":"abstention_keyword_proxy","score":abstained,"abstained":abstained,"human_review_required":True}
    return {"metric":"unscored","score":None}

def main():
    path=ROOT/"data/results/granite-evaluation.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    for row in data["records"]:
        if "raw_answer" in row and row["case_id"] in CASE_BY_ID:
            row["score"]=score(CASE_BY_ID[row["case_id"]],row["raw_answer"])
    summaries=[]
    for model in sorted({x["model"] for x in data["records"]}):
        rows=[x for x in data["records"] if x.get("model")==model and "score" in x]
        bycat={}
        for category in sorted({x["category"] for x in rows}):
            group=[x for x in rows if x["category"]==category]
            passed=sum(bool(x["score"]["score"]) for x in group)
            bycat[category]={"passed":passed,"total":len(group),"rate":round(passed/len(group),3)}
        groups={}
        for row in rows:
            if row["category"]=="numeric_exact": groups.setdefault(row["case_id"],[]).append(row)
        repeated=[g for g in groups.values() if len(g)>1]
        agreements=[]
        for group in repeated:
            finals=[r["score"].get("parsed_numbers",[])[-1:] for r in group]
            agreements.append(bool(finals[0] and all(x==finals[0] for x in finals)))
        summaries.append({"model":model,"model_digest":next((x.get("model_digest") for x in rows if x.get("model_digest")),None),"by_category":bycat,"mean_latency_ms":round(statistics.mean(x["latency_ms"] for x in rows if x.get("latency_ms") is not None),2) if rows else None,"numeric_repeat_consistency":round(sum(agreements)/len(agreements),3) if agreements else None,"numeric_repeat_cases":len(repeated),"interpretation":"descriptive scores on this small fixed dataset; not a general model ranking"})
    data["dataset_sha256"]=hashlib.sha256((ROOT/"granite/dataset/cases.json").read_bytes()).hexdigest()
    data["models"]=summaries
    data["rescoring"]={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"new_inference_run":False,"reason":"reviewed retained abstention wording, expanded its keyword proxy, corrected the boundary-bug rubric, and calculated repeat agreement from repeated outputs; no new inference"}
    data["limitations"].append("a rubric correction was applied after the original inference; responses were not regenerated")
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(summaries,indent=2,ensure_ascii=False))
if __name__=="__main__": main()





