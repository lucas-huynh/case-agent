from backend.case_loader import CaseLoader
from backend.engine.persona_engine import PersonaEngine
from backend.engine.persona_router import PersonaRouter


loader = CaseLoader()
case = loader.load_case("hospital_surge_v1")

engine = PersonaEngine(case)
router = PersonaRouter()


questions = [
    "What happens if we are short one nurse during a shift?",
    "What about during a surge in arrivals?",
    "Why is surge staffing expensive?",
    "How do you usually predict ED arrivals?"
]


for q in questions:

    print("\n-----------------------------------")
    print("STUDENT QUESTION:")
    print(q)

    persona = router.route(q)

    print("\nRouted to:", persona)

    response = engine.ask_persona(persona, q)

    print(f"\n[{persona.upper()} RESPONSE]\n")

    print(response)