import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from backend.case_loader import CaseLoader
from backend.engine.persona_engine import PersonaEngine
from backend.engine.persona_router import PersonaRouter
from backend.llm_adapter import generate_response


st.set_page_config(page_title="Hospital Surge Staffing Simulator", layout="wide")

st.title("Hospital Surge Staffing — Stakeholder Interview Simulator")


@st.cache_resource
def load_engine():

    loader = CaseLoader()
    case_data = loader.load_case("hospital_surge_v1")

    engine = PersonaEngine(case_data)
    router = PersonaRouter()

    return engine, router, case_data


engine, router, case_data = load_engine()


BUCKETS = [
    "decisions",
    "objectives",
    "constraints",
    "uncertainties",
    "state_variables",
    "operational_insights",
    "tradeoffs",
    "evidence"
]


if "chat" not in st.session_state:
    st.session_state.chat = []

if "notes" not in st.session_state:
    st.session_state.notes = {k: [] for k in BUCKETS}

if "last_reply" not in st.session_state:
    st.session_state.last_reply = ""

if "questions_remaining" not in st.session_state:
    st.session_state.questions_remaining = 20


with st.sidebar:

    st.subheader("Session")

    if st.button("Reset Session"):

        st.session_state.chat = []
        st.session_state.notes = {k: [] for k in BUCKETS}
        st.session_state.questions_remaining = 20
        engine.history = []

        st.success("Session reset")

    st.metric("Questions Remaining", st.session_state.questions_remaining)

    st.markdown("---")

    bucket = st.selectbox("Pin Insight To", BUCKETS)

    if st.button("Pin Last Answer (AI Summary)"):

        if st.session_state.last_reply:

            prompt = f"""
Extract the single most important operational insight from this answer.

{st.session_state.last_reply}
"""

            insight = generate_response(prompt)

            st.session_state.notes[bucket].append(insight)

    st.markdown("---")

    st.subheader("Progress Checks")

    for c in case_data["case"]["recommended_progress_checks"]:
        st.write("•", c["prompt"])


col1, col2 = st.columns([2, 1])


with col1:

    st.subheader("Meeting Room")

    with st.expander("Stakeholders"):

        for key, p in engine.personas.items():

            idn = p["identity"]

            st.write(
                f"**@{key} — {idn['name']} ({idn['title']})**"
            )

    with st.expander("Question Hints"):

        guidance = case_data["case"]["student_guidance"]

        for t in guidance["hint_topics"]:
            st.write("-", t)

        st.write("")

        for q in guidance["example_questions"]:
            st.write("-", q)

    mention = st.selectbox(
        "@mention",
        ["auto", "cfo", "physician", "operations_manager"]
    )

    prompt = st.text_input("Ask a question")

    if st.button("Send"):

        if st.session_state.questions_remaining > 0:

            st.session_state.questions_remaining -= 1

            st.session_state.chat.append(("user", prompt))

            if mention == "auto":
                persona = router.route(prompt)
            else:
                persona = mention

            reply = engine.ask_persona(persona, prompt)

            st.session_state.chat.append((persona, reply))

            st.session_state.last_reply = reply

    for role, text in st.session_state.chat[-12:]:

        if role == "user":

            st.chat_message("user").write(text)

        else:

            p = engine.personas[role]["identity"]

            label = f"{p['name']} — {p['title']}"

            st.chat_message("assistant").write(
                f"**{label}**\n\n{text}"
            )


with col2:

    st.subheader("Problem Formulation Canvas")

    tabs = st.tabs([b.replace("_", " ").title() for b in BUCKETS])

    for tab, key in zip(tabs, BUCKETS):

        with tab:

            for i, item in enumerate(st.session_state.notes[key]):

                colA, colB = st.columns([8,1])

                colA.write(item)

                if colB.button("❌", key=f"{key}_{i}"):

                    st.session_state.notes[key].pop(i)
                    st.rerun()

            new_note = st.text_input(
                f"Add note to {key}",
                key=f"input_{key}"
            )

            if st.button("Add", key=f"add_{key}"):

                if new_note:

                    st.session_state.notes[key].append(new_note)

                    st.rerun()


st.markdown("---")


if st.button("Generate Problem Formulation"):

    notes = str(st.session_state.notes)

    prompt = f"""
Based on the following notes from stakeholder interviews,
construct a structured operations research problem formulation.

{notes}

Include:

Decision Variables
State Variables
Objective Function
Constraints
Uncertainty
Trade-offs
"""

    formulation = generate_response(prompt)

    st.subheader("Generated Problem Formulation")

    st.write(formulation)


st.markdown("---")


if st.button("Evaluate My Formulation"):

    notes = str(st.session_state.notes)

    rubric = case_data["case"]["rubric"]

    prompt = f"""
Evaluate this student formulation.

Notes:
{notes}

Rubric:
{rubric}

Provide scores and feedback.
"""

    result = generate_response(prompt)

    st.subheader("Instructor Evaluation")

    st.write(result)