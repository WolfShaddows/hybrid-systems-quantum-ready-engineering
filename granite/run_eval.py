# Purpose: run eval (granite/run_eval.py). Expected: load inputs, validate assumptions, run the experiment or assertion, and emit reproducible evidence.
import argparse, hashlib, json, re, statistics, subprocess, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENDPOINT="http://127.0.0.1:11434"

def get_json(path):
    with urllib.request.urlopen(ENDPOINT+path,timeout=10) as r: return json.load(r)
def generate(model,prompt,seed):
    payload={"model":model,"messages":[{"role":"user","content":prompt}],"think":("low" if "think" in model.lower() else False),"stream":False,"options":{"temperature":0,"seed":seed,"num_predict":1024 if "think" in model.lower() else 256}}
    req=urllib.request.Request(ENDPOINT+"/api/chat",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    started=time.perf_counter()
    with urllib.request.urlopen(req,timeout=360) as response: data=json.load(response)
    elapsed=(time.perf_counter()-started)*1000
    msg=data.get("message",{})
    return {"answer":msg.get("content",""),"thinking":msg.get("thinking",""),"latency_ms":round(elapsed,2),"total_duration_ns":data.get("total_duration"),"prompt_tokens":data.get("prompt_eval_count"),"generated_tokens":data.get("eval_count")}
def score(case,answer):
    category=case["category"]
    if category=="numeric_exact":
        normalized=answer.replace(",","")
        hits=re.findall(r"(?<![A-Za-z])\d+(?![A-Za-z])",normalized)
        return {"metric":"exact_numeric_match","score":bool(hits and hits[-1]==case["expected"]),"expected":case["expected"],"parsed_numbers":hits}
    if category in ("bug_detection","security_finding"):
        lower=answer.lower()
        matched=[word for word in case["expected_keywords"] if word in lower]
        return {"metric":"keyword_rubric_proxy","score":len(matched)==len(case["expected_keywords"]),"matched":matched,"required":case["expected_keywords"],"human_review_required":True}
    if category=="abstention":
        abstained=bool(re.search(r"(not specified|not provided|does not specify|does not establish|does not state|does not say|cannot determine|cannot be determined|can't determine|unknown|no sla|not established|insufficient information|not guaranteed)",answer,re.I))
        return {"metric":"abstention_keyword_proxy","score":abstained,"abstained":abstained,"human_review_required":True}
    return {"metric":"unscored","score":None}
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--models",nargs="+",default=["granite42-fast:latest","granite42-think:latest"]); parser.add_argument("--seed",type=int,default=42); parser.add_argument("--timeout",type=int,default=360); args=parser.parse_args()
    tags=get_json("/api/tags").get("models",[]); tag_map={x.get("name"):x for x in tags}
    version=subprocess.run(["ollama","--version"],capture_output=True,text=True).stdout.strip()
    cases=json.loads((ROOT/"granite/dataset/cases.json").read_text(encoding="utf-8-sig"))
    dataset_hash=hashlib.sha256((ROOT/"granite/dataset/cases.json").read_bytes()).hexdigest()
    raw=[]
    for model in args.models:
        if model not in tag_map: raise SystemExit(f"Model tag not installed locally: {model}")
        for case in cases:
            for rep in range(case.get("repeat",1)):
                try:
                    generated=generate(model,case["prompt"],args.seed)
                    raw.append({"model":model,"model_digest":tag_map[model].get("digest"),"case_id":case["id"],"category":case["category"],"repeat":rep+1,"prompt":case["prompt"],"raw_answer":generated["answer"],"thinking_mode":("low" if "think" in model.lower() else False),"score":score(case,generated["answer"]),**{k:v for k,v in generated.items() if k not in ("answer","thinking")}})
                    partial={"schema_version":"1.0","experiment_id":"granite-local-engineering-eval","status":"in_progress","records":raw,"limitations":["partial run; do not interpret as final"]}
                    partial_path=ROOT/"data/results/granite-evaluation.partial.json"; partial_path.parent.mkdir(parents=True,exist_ok=True); partial_path.write_text(json.dumps(partial,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
                    print(f"{model} {case['id']} run {rep+1}: {generated['latency_ms']} ms")
                except Exception as exc: raw.append({"model":model,"case_id":case["id"],"repeat":rep+1,"error":str(exc)})
    summary=[]
    for model in args.models:
        rows=[x for x in raw if x.get("model")==model and "score" in x]
        bycat={}
        for category in sorted({x["category"] for x in rows}):
            group=[x for x in rows if x["category"]==category]
            bycat[category]={"passed":sum(bool(x["score"]["score"]) for x in group),"total":len(group),"rate":round(sum(bool(x["score"]["score"]) for x in group)/len(group),3)}
        numeric=[x for x in rows if x["category"]=="numeric_exact"]
        summary.append({"model":model,"model_digest":tag_map[model].get("digest"),"by_category":bycat,"mean_latency_ms":round(statistics.mean(x["latency_ms"] for x in rows),2) if rows else None,"numeric_repeat_consistency":round(sum(x["score"]["score"] for x in numeric)/len(numeric),3) if numeric else None,"interpretation":"descriptive scores on this small fixed dataset; not a general model ranking"})
    payload={"schema_version":"1.0","experiment_id":"granite-local-engineering-eval","status":"executed","timestamp_utc":datetime.now(timezone.utc).isoformat(),"endpoint":"local Ollama API at 127.0.0.1:11434","ollama_version":version,"dataset_sha256":dataset_hash,"dataset_cases":len(cases),"seed":args.seed,"generation":{"temperature":0,"seed":args.seed,"fast":{"think":False,"num_predict":256},"think":{"think":"low","num_predict":1024}},"models":summary,"records":raw,"limitations":["small synthetic dataset; scores are not general capability estimates","keyword rubric is a proxy; human review is required","local inference was through Ollama; tags and quantization are host-specific","no model is authorized to decide or post transactions"]}
    out=ROOT/"data/results/granite-evaluation.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); partial_path.unlink(missing_ok=True); print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=="__main__": main()








