import json
from pathlib import Path
import unittest

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
MAPPING_SCHEMA_PATH = ROOT / "packages" / "schemas" / "direct-source-mapping.schema.json"
MAPPING_PATH = ROOT / "packages" / "tax_engine" / "definitions" / "direct_source_to_form.federal.2025.json"


class DirectMappingContractTests(unittest.TestCase):
    def test_direct_mapping_file_validates_against_schema(self):
        schema = json.loads(MAPPING_SCHEMA_PATH.read_text())
        payload = json.loads(MAPPING_PATH.read_text())

        jsonschema.validate(payload, schema)

    def test_direct_mappings_have_unique_ids_and_destinations(self):
        payload = json.loads(MAPPING_PATH.read_text())
        mapping_ids = [mapping["mapping_id"] for mapping in payload["mappings"]]
        destinations = [mapping["destination_field_id"] for mapping in payload["mappings"]]

        self.assertEqual(len(mapping_ids), len(set(mapping_ids)))
        self.assertEqual(len(destinations), len(set(destinations)))

    def test_direct_mappings_cover_w2_and_1099_int(self):
        payload = json.loads(MAPPING_PATH.read_text())
        document_types = {mapping["source_document_type"] for mapping in payload["mappings"]}

        self.assertEqual(document_types, {"w2", "1099-int"})


if __name__ == "__main__":
    unittest.main()
