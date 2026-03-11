from backend.llm_adapter import generate_response


class PersonaRouter:

    def route(self, question: str) -> str:

        prompt = f"""
You are routing questions in a hospital stakeholder meeting.

Choose which stakeholder should answer.

Stakeholders:

physician
- clinical care
- patient safety
- waiting time
- crowding
- quality of care

cfo
- financial cost
- budgets
- staffing expense
- overtime
- economic tradeoffs

operations_manager
- scheduling
- staffing logistics
- patient arrival forecasts
- operational planning

Return ONLY one word:

physician
cfo
operations_manager

Question:
{question}
"""

        response = generate_response(prompt).strip().lower()

        if "physician" in response:
            return "physician"

        if "cfo" in response:
            return "cfo"

        if "operations" in response:
            return "operations_manager"

        # fallback
        return "operations_manager"