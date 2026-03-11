from case_loader import CaseLoader

loader = CaseLoader()

case = loader.load_case("hospital_surge_v1")

print("Loaded case:", case["case"]["title"])
print("Chunks:", len(case["chunks"]))
print("Personas:", list(case["personas"].keys()))