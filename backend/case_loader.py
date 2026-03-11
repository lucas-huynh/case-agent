from pathlib import Path
import yaml

class CaseLoader:
    """
    Loads a case pack from the cases/ directory and validates references.

    Expected structure:

    cases/
        case_id/
            case.yaml
            chunks.yaml
            personas/
                *.yaml
    """

    def __init__(self, cases_root: str = "cases"):
        self.cases_root = Path(cases_root)

    # public API

    def load_case(self, case_id: str) -> dict:
        """
        Load a full case pack.

        Returns:
            {
                "case": case_yaml,
                "chunks": {chunk_id: chunk_data},
                "personas": {persona_id: persona_yaml}
            }
        """

        case_dir = self.cases_root / case_id

        if not case_dir.exists():
            raise FileNotFoundError(f"Case folder not found: {case_dir}")

        case_data = self._load_yaml(case_dir / "case.yaml")
        chunks_data = self._load_yaml(case_dir / "chunks.yaml")
        personas_data = self._load_personas(case_dir / "personas")

        chunk_index = self._index_chunks(chunks_data)

        self._validate_persona_chunk_refs(personas_data, chunk_index)

        return {
            "case": case_data,
            "chunks": chunk_index,
            "personas": personas_data,
        }

    # internal Helpers

    def _load_yaml(self, path: Path):
        """Load a YAML file safely."""
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")

        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _load_personas(self, persona_dir: Path):
        """Load all persona YAML files."""
        if not persona_dir.exists():
            raise FileNotFoundError(f"Missing persona folder: {persona_dir}")

        personas = {}

        for file in persona_dir.glob("*.yaml"):
            data = self._load_yaml(file)

            persona_id = data.get("persona_id")

            if not persona_id:
                raise ValueError(f"Persona file missing persona_id: {file}")

            personas[persona_id] = data

        return personas

    def _index_chunks(self, chunks_yaml):
        """
        Convert chunk list into dictionary for fast lookup.
        """

        if "chunks" not in chunks_yaml:
            raise ValueError("chunks.yaml must contain a 'chunks' list")

        chunk_index = {}

        for chunk in chunks_yaml["chunks"]:
            cid = chunk.get("id")

            if not cid:
                raise ValueError("Chunk missing id field")

            if cid in chunk_index:
                raise ValueError(f"Duplicate chunk id detected: {cid}")

            chunk_index[cid] = chunk

        return chunk_index

    def _validate_persona_chunk_refs(self, personas, chunk_index):
        """
        Ensure persona known_facts refer to valid chunks.
        """

        for persona_id, persona in personas.items():

            facts = persona.get("known_facts", [])

            for fact in facts:
                chunk_id = fact.get("chunk_id")

                if chunk_id not in chunk_index:
                    raise ValueError(
                        f"Persona '{persona_id}' references missing chunk '{chunk_id}'"
                    )
                
# when you run:
"""
loader = CaseLoader()
case = loader.load_case("hospital_surge_v1")
"""

# you get:
"""
case = {
    "case": {...case.yaml...},
    "chunks": {
        "ed_001": {...},
        "ed_002": {...}
    },
    "personas": {
        "cfo": {...},
        "physician": {...},
        "operations_manager": {...}
    }
}
"""
