"""Run REAW Phase 2 directly from existing React definition files (skip Phase 1)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "reaw"))

from parsers.react_definition_parser import ReactDefinitionParser
from generators.phase2.react_code_generator import ReactCodeGenerator

input_path = "application_definitions/job_portal"
output_path = "generated_application/job_portal/react_app"

print(f"[Phase 2] Parsing React definitions from: {input_path}")
react_def = ReactDefinitionParser.parse(input_path)

print(f"[Phase 2] Generating React application to: {output_path}")
files = ReactCodeGenerator.generate(react_def, output_path)
print(f"[Phase 2] Complete. Generated {len(files)} source files.")
