import json
from pathlib import Path
import streamlit as st
from engine.investigation import investigate

st.set_page_config(page_title="THADAM AI", page_icon="🛡️", layout="wide")
st.title("🛡️ THADAM AI")
st.caption("Every attack leaves a trail. We follow it.")
st.divider()

uploaded = st.file_uploader("Upload security incident JSON", type=["json"])
run = st.button("🚨 Run Demo Investigation", type="primary")

if uploaded:
    events = json.load(uploaded)
elif run:
    events = json.loads(Path("data/sample_incident.json").read_text(encoding="utf-8"))
else:
    st.info("Upload an incident JSON or click Run Demo Investigation.")
    st.stop()

result = investigate(events)

a,b,c,d = st.columns(4)
a.metric("Events Correlated", result["event_count"])
b.metric("Risk Score", f'{result["risk_score"]}/100')
c.metric("ATT&CK Techniques", len(result["techniques"]))
d.metric("Evidence Items", len(result["evidence"]))

st.subheader("🔴 AI Investigation Verdict")
st.warning(f"{result['verdict']} — {result['confidence']}% confidence")
st.write(result["summary"])

x,y = st.columns(2)
with x:
    st.subheader("🧩 Attack Chain")
    st.write(" → ".join(result["attack_chain"]))
with y:
    st.subheader("📚 RAG Evidence")
    for item in result["rag_evidence"]:
        st.write(f"**{item['source']}** — {item['finding']}")

st.subheader("🔎 Evidence")
for item in result["evidence"]:
    st.write("✓", item)

st.subheader("🎯 MITRE ATT&CK Mapping")
for item in result["techniques"]:
    st.code(item)

st.subheader("🤖 Agent Trace")
for item in result["agent_trace"]:
    st.write(f"**{item['agent']}** → {item['action']} → `{item['result']}`")

if st.button("⚔️ Challenge My Verdict"):
    c = result["challenge"]
    st.warning(f"**Skeptic Agent:** {c['question']}")
    st.write(c["analysis"])
    st.success(f"**{c['conclusion']}** — {c['confidence']}% confidence")

st.subheader("🚑 Recommended Response")
for item in result["response_plan"]:
    st.write("•", item)
