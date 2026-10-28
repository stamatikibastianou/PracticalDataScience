"""Draw YOUR personal sample of 20 comments from data/pool.csv.

Run it once, at the very start, with your own seed (for example your student id number):

    python prepare_items.py --seed 123456

The pool holds 250 short comments from news-site discussions, from fully civil to very toxic. Your
sample is 20 of them, a mix of civil and toxic texts. The same seed always gives the same 20 items;
a different seed gives a different sample. Write your seed down: it goes in your notebook and in
your report.

Writes, into items/:
  items.csv      id | text | rating | label | evidence   (last three empty; evidence is "not needed" for ratings 1-2)
  annotate.html  a self-contained local page to rate the items and export the CSV
"""
import argparse
import base64
import json
import random
import zlib
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SRC = HERE / "data" / "pool.csv"
OUT = HERE / "items"

# how the pool is mixed (set by the instructor); used to draw a balanced sample
_MIX = "eJwlj8ENACAQwmYCyv6rGc6XhtiCsiM1jkVS11SGNkhtI7yzwchudRnFchnPrhAgKjo4F1koxw7HwmvB0sCk61+BkhiXZrbcnET2ZHPJEWxtlf5117FJaWfG+fa9mkhaHqj3uTMozgNupzHP"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20, help="number of items to draw")
    ap.add_argument("--seed", type=int, required=True, help="your personal seed, e.g. your student id")
    a = ap.parse_args()

    pool = pd.read_csv(SRC)
    ids = sorted(pool.id)
    mix = zlib.decompress(base64.b64decode(_MIX)).decode()
    if len(mix) != len(ids):
        raise SystemExit("the pool and the script do not match: ask your instructor for the original files")
    groups = {}
    for i, g in zip(ids, mix):
        groups.setdefault(g, []).append(i)
    rng = random.Random(a.seed)
    per = a.n // len(groups)
    chosen = [i for g in sorted(groups) for i in rng.sample(groups[g], per)]
    rest = [i for i in ids if i not in chosen]
    chosen += rng.sample(rest, a.n - len(chosen))  # when n is not a multiple of the number of groups
    pick = pool[pool.id.isin(chosen)][["text"]].sample(frac=1, random_state=a.seed)
    pick.insert(0, "id", range(1, len(pick) + 1))

    OUT.mkdir(exist_ok=True)
    pick.assign(rating="", label="", evidence="").to_csv(
        OUT / "items.csv", index=False, encoding="utf-8")
    write_html(pick.to_dict("records"), a.seed)
    print(f"seed {a.seed}: wrote {len(pick)} items to {OUT}")


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Toxicity annotation (seed __SEED__)</title>
<style>
:root{--bg:#fff;--fg:#1c1c1e;--mut:#6b6b70;--card:#f4f4f6;--acc:#2f5fd0;--line:#d8d8de}
@media(prefers-color-scheme:dark){:root{--bg:#18181b;--fg:#ececf0;--mut:#9a9aa3;--card:#25252a;--acc:#7da2ff;--line:#3a3a42}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:760px;margin:0 auto;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
progress{width:100%;height:8px}
.text{background:var(--card);border-radius:8px;padding:14px;white-space:pre-wrap;margin:12px 0}
.scale{display:flex;gap:8px}
.scale label{flex:1;text-align:center;border:1px solid var(--line);border-radius:8px;padding:10px 0;cursor:pointer}
.scale input{display:none}
.scale input:checked+span{font-weight:700;color:var(--acc)}
.scale label:has(input:checked){border-color:var(--acc);background:var(--card)}
.hint{display:flex;justify-content:space-between;color:var(--mut);font-size:13px;margin:4px 2px 12px}
textarea{width:100%;box-sizing:border-box;min-height:70px;padding:8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);font:inherit}
.nav{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap}
button{padding:10px 16px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg);font:inherit;cursor:pointer}
button:disabled{opacity:.45;cursor:not-allowed}
button.p{background:var(--acc);color:#fff;border-color:var(--acc)}
mark{background:#ffd54a;color:#000;border-radius:3px}
.chips{display:flex;flex-direction:column;gap:6px;margin:6px 0 12px}
.chip{background:var(--card);border-left:4px solid #ffd54a;padding:6px 10px;border-radius:6px;display:flex;gap:8px;justify-content:space-between;font-size:14px}
.chip button{padding:0 8px}
.overlay{position:fixed;inset:0;background:var(--bg);overflow:auto;z-index:10}
.panel{max-width:760px;margin:0 auto;padding:16px}
.panel table{border-collapse:collapse;width:100%;margin:8px 0}
.panel td{border-top:1px solid var(--line);padding:6px 8px;vertical-align:top}
.panel td:first-child{width:28px;text-align:center}
.panel li{margin:4px 0}
.note{color:var(--mut);font-size:13px}
</style></head><body><main>
<div id="guide" class="overlay"><div class="panel">
<h2>Guidelines: how toxic is the item?</h2>
<p>Each item is a short comment from a news-site discussion. Read all of it and give <b>one rating for the whole item</b>, from 1 to 5, by how <b>uncivil, hostile or disrespectful</b> the language is.</p>
<table>
<tr><td><b>1</b></td><td>Fully civil. Respectful, even if the two sides disagree strongly.</td></tr>
<tr><td><b>2</b></td><td>Mostly civil. Blunt, sarcastic or a little rude, but no attack on the person.</td></tr>
<tr><td><b>3</b></td><td>Borderline. Clear disrespect: mocking, accusing the other of lying or bad faith, condescension.</td></tr>
<tr><td><b>4</b></td><td>Toxic. Personal insults, name-calling, hostile or demeaning language aimed at a person or a group.</td></tr>
<tr><td><b>5</b></td><td>Very toxic. Severe abuse: slurs, threats, harassment, hate.</td></tr>
</table>
<ul>
<li><b>1-2 count as civil, 3-5 as toxic.</b> The page shows the label as you rate.</li>
<li>Rate the <b>tone</b>, not the topic. A controversial subject (abortion, politics, religion) is not toxic by itself, and a calm text defending an ugly view is judged on how it is said.</li>
<li>A swear word is not automatically toxic: aimed at a person it counts, used for emphasis it counts much less.</li>
<li>Quoted or reported words count less than words the writer says to someone.</li>
<li>If several messages differ, let the <b>most toxic part</b> weigh most.</li>
<li>Use your own judgement: careful readers disagree, and there is no wrong answer. Rate alone, and do not go back to change a rating.</li>
<li>Give every item a rating. If you rate <b>3, 4 or 5</b>, also <b>select with the mouse the words</b> that make the text toxic: they are your evidence, and you need at least one to go on. For a 1 or a 2 you only give the rating: the evidence is "not needed".</li>
</ul>
<p class="note">Content note: the texts may contain harsh language.</p>
<button id="start" class="p">Start annotating</button>
</div></div>
<header><h1 style="font-size:20px;margin:0">How toxic is the item?</h1><span id="pos"></span></header>
<progress id="bar" max="100" value="0"></progress>
<p class="note">Content note: items may contain harsh language. Rate alone, before looking at any model output.
Your answers are saved in this browser as you go.</p>
<div id="text" class="text"></div>
<div class="scale" id="scale"></div>
<div class="hint"><span>1 = fully civil</span><span>5 = very toxic</span></div>
<p>Label: <b id="lab">-</b></p>
<p id="evno" class="note" style="display:none">Evidence: not needed for a 1 or a 2.</p>
<div id="evbox" style="display:none"><label>Evidence: select with the mouse the words that make it toxic (they are added below automatically):</label>
<div id="chips" class="chips"></div></div>
<div class="nav">
<button id="prev">&larr; Previous</button><button id="next" class="p">Next &rarr;</button>
<button id="gbtn">Guidelines</button>
<button id="exp" class="p" style="margin-left:auto;display:none">Download annotated CSV</button></div>
<p class="note" id="need"></p>
<p class="note" id="status"></p>
<p class="note" id="hint2"></p>
</main>
<script>
const ITEMS=__ITEMS__;
const KEY="ass1_ratings_seed___SEED__";
const ok=id=>{const x=S[id];return !!(x&&x.rating&&(+x.rating<=2||(x.evidence||[]).length>=1))};  // a rating; for 3-5 also at least one highlighted passage
let S={};try{S=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
let i=0;
const $=id=>document.getElementById(id);
$("scale").innerHTML=[1,2,3,4,5].map(n=>`<label><input type="radio" name="r" value="${n}"><span>${n}</span></label>`).join("");
function save(){const it=ITEMS[i],r=document.querySelector("input[name=r]:checked");
 const old=S[it.id]||{};S[it.id]={rating:r?r.value:"",evidence:old.evidence||[]};
 if(r&&+r.value<=2)S[it.id].evidence=[];  // evidence only for 3-5
 $("evbox").style.display=r&&+r.value>=3?"":"none";
 $("evno").style.display=r&&+r.value<=2?"":"none";
 try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}
 const done=ITEMS.filter(x=>ok(x.id)).length;
 const left=ITEMS.length-done;$("exp").style.display=left>0?"none":"";
 $("hint2").textContent=left>0?left+" of "+ITEMS.length+" items still to complete (a rating and a highlighted passage).":"All items complete: the download button is now available.";
 $("next").disabled=!ok(it.id)||i===ITEMS.length-1;
 $("need").textContent=ok(it.id)?"":(S[it.id].rating?"To continue: select the words that make it toxic.":"To continue: pick a rating.");
 $("lab").textContent=lab(S[it.id].rating)||"-";
 $("bar").value=100*done/ITEMS.length;$("status").textContent=done+" / "+ITEMS.length+" complete";}
function show(){const it=ITEMS[i],s=S[it.id]||{};
 render();$("pos").textContent="Item "+(i+1)+" / "+ITEMS.length+" (id "+it.id+")";
 document.querySelectorAll("input[name=r]").forEach(x=>x.checked=x.value===s.rating);
 save();}
function render(){const it=ITEMS[i],ev=(S[it.id]&&S[it.id].evidence)||[];
 let h=esc(it.text);ev.forEach(e=>{const x=esc(e);h=h.split(x).join("<mark>"+x+"</mark>")});
 $("text").innerHTML=h;
 $("chips").innerHTML=ev.map((e,k)=>`<div class="chip"><span>&ldquo;${esc(e)}&rdquo;</span><button data-k="${k}">&times;</button></div>`).join("");}
const lab=r=>r?(+r<=2?"civil":"toxic"):"";
const esc=t=>t.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
$("text").addEventListener("mouseup",()=>{const t=String(getSelection()).trim();if(!t)return;
 const it=ITEMS[i];if(!it.text.includes(t))return;save();if(!(+S[it.id].rating>=3))return;const e=S[it.id].evidence;
 if(!e.includes(t))e.push(t);getSelection().removeAllRanges();save();render();});
$("chips").addEventListener("click",ev=>{const k=ev.target.dataset.k;if(k===undefined)return;
 S[ITEMS[i].id].evidence.splice(+k,1);save();render();});
function go(d){save();if(d>0&&!ok(ITEMS[i].id))return;i=Math.min(ITEMS.length-1,Math.max(0,i+d));show();}
$("prev").onclick=()=>go(-1);$("next").onclick=()=>go(1);
document.addEventListener("change",e=>{if(e.target.name==="r"){save();render()}});
const q=v=>'"'+String(v).replace(/"/g,'""')+'"';
$("exp").onclick=()=>{save();
 if(ITEMS.some(x=>!ok(x.id)))return;
 const rows=["id,text,rating,label,evidence"].concat(ITEMS.map(x=>[x.id,q(x.text),S[x.id]?S[x.id].rating:"",lab(S[x.id]?S[x.id].rating:""),q(S[x.id]?(+S[x.id].rating<=2?"not needed":(S[x.id].evidence||[]).join(" || ")):"")].join(",")));
 const a=document.createElement("a");a.href=URL.createObjectURL(new Blob(["\\ufeff"+rows.join("\\r\\n")],{type:"text/csv"}));
 a.download="items_rated.csv";a.click();};
const G=$("guide");
$("start").onclick=()=>{G.style.display="none";try{localStorage.setItem(KEY+"_seen","1")}catch(e){}};
$("gbtn").onclick=()=>{G.style.display="block"};
try{if(localStorage.getItem(KEY+"_seen"))G.style.display="none"}catch(e){}
show();
</script></body></html>
"""


def write_html(items, seed):
    data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.replace("__ITEMS__", data).replace("__SEED__", str(seed))
    (OUT / "annotate.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
