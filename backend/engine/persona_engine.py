from typing import List, Dict

from backend.llm_adapter import generate_response
from backend.config import MAX_CHUNKS_PER_RESPONSE
from backend.retrieval.semantic_retriever import SemanticRetriever


class PersonaEngine:
    """
    Stakeholder simulation engine.

    Combines:
    - persona disclosure rules
    - persona knowledge
    - semantic retrieval (RAG)
    """

    def __init__(self, case_data: dict):

        self.case = case_data["case"]
        self.chunks = case_data["chunks"]
        self.personas = case_data["personas"]

        self.retriever = SemanticRetriever(self.chunks)

        self.history = []

    # MAIN ENTRY

    def ask_persona(self, persona_id: str, question: str) -> str:

        persona = self.personas[persona_id]

        rules = persona.get("disclosure_rules", [])

        rule_chunks = self._match_rules(rules, question)

        known_chunks = self._get_persona_known_chunks(persona)

        semantic_chunks = self.retriever.search(question, top_k=5)

        combined_chunks = list(set(rule_chunks + known_chunks + semantic_chunks))

        chunk_texts = self._retrieve_chunks(combined_chunks)

        prompt = self._build_prompt(persona, chunk_texts, question)

        response = generate_response(prompt)

        if response is None:
            response = "I'm not sure I can answer that directly, but staffing decisions usually involve balancing demand uncertainty, staffing costs, and patient waiting times."

        citations = self._build_citations(combined_chunks)

        if citations:

            citation_text = "\n\nSources:\n"

            for c in citations:
                citation_text += f"- {c}\n"

            response += citation_text

        self.history.append({"speaker": "student", "text": question})
        self.history.append({"speaker": persona_id, "text": response})

        return response

    # RULE MATCHING

    def _match_rules(self, rules: List[Dict], question: str) -> List[str]:

        question_lower = question.lower()

        chunk_ids = []

        for rule in rules:

            keywords = rule.get("trigger_keywords", [])

            for word in keywords:

                if word.lower() in question_lower:

                    chunk_ids.extend(rule.get("reveal_chunk_ids", []))
                    break

        return list(set(chunk_ids))

    # PERSONA KNOWLEDGE

    def _get_persona_known_chunks(self, persona):

        chunk_ids = []

        for fact in persona.get("known_facts", []):

            cid = fact.get("chunk_id")

            if cid:
                chunk_ids.append(cid)

        return chunk_ids

    # CHUNK RETRIEVAL

    def _retrieve_chunks(self, chunk_ids: List[str]) -> List[str]:

        texts = []

        chunk_dict = self._normalize_chunks()

        for cid in chunk_ids[:MAX_CHUNKS_PER_RESPONSE]:

            if cid in chunk_dict:

                text = chunk_dict[cid].get("text")

                if text:
                    texts.append(text)

        # safety fallback
        if not texts:

            texts.append(
                "Emergency department staffing decisions involve balancing patient demand, staffing cost, and service quality."
            )

        return texts

    # ------------------------------------------------
    # NORMALIZE YAML CHUNKS
    # ------------------------------------------------

    def _normalize_chunks(self):

        if isinstance(self.chunks, dict):

            if "chunks" in self.chunks:
                return {c["id"]: c for c in self.chunks["chunks"]}

            return self.chunks

        else:
            return {c["id"]: c for c in self.chunks}

    # ------------------------------------------------
    # CITATION BUILDER
    # ------------------------------------------------

    def _build_citations(self, chunk_ids):

        sources = self.case.get("source_documents", [])

        source_map = {s["source_id"]: s["label"] for s in sources}

        citations = set()

        chunk_dict = self._normalize_chunks()

        for cid in chunk_ids:

            if cid in chunk_dict:

                source_id = chunk_dict[cid].get("source_id")

                if source_id in source_map:

                    citations.add(source_map[source_id])

        return list(citations)

    # PROMPT BUILDER

    def _build_prompt(self, persona, chunk_texts, question):

        identity = persona["identity"]

        objectives = persona.get("objectives", [])
        constraints = persona.get("hard_constraints", [])
        concerns = persona.get("concerns", [])
        unknowns = persona.get("unknowns", [])

        objective_text = "\n".join([f"- {o['text']}" for o in objectives])
        constraint_text = "\n".join([f"- {c['text']}" for c in constraints])
        concern_text = "\n".join([f"- {c}" for c in concerns])
        unknown_text = "\n".join([f"- {u}" for u in unknowns])
        chunk_text = "\n".join([f"- {c}" for c in chunk_texts])

        history_lines = []

        for h in self.history[-6:]:

            if h["speaker"] == "student":

                label = "Student"

            else:

                label = self.personas[h["speaker"]]["identity"]["title"]

            history_lines.append(f"{label}: {h['text']}")

        history_text = "\n".join(history_lines)

        prompt = f"""
You are participating in a stakeholder meeting simulation.

ROLE
You are {identity['title']} named {identity['name']}.

OBJECTIVES
{objective_text}

CONCERNS
{concern_text}

CONSTRAINTS
{constraint_text}

WHAT YOU KNOW
{chunk_text}

WHAT YOU DO NOT KNOW
{unknown_text}

MEETING HISTORY
{history_text}

RULES
- Stay in character
- Speak naturally as a professional stakeholder
- Do not solve the optimization problem
- Share relevant operational insights

STUDENT QUESTION
{question}
"""

        return prompt.strip()