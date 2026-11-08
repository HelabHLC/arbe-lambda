# FP Prompt Blueprint

This blueprint shows how to convert compact FP code strings into deterministic image prompts.

## Quick start

```bash
python fp_prompt_blueprint.py
```

## Python usage

```python
from fp_prompt_blueprint import parse_fp_code, build_image_prompt

code = "FP::H340_L050_C040::a+37.60::b-13.68::Δλ_-109.702::HEX_#AB5C90::RGB_171_92_144"
parsed = parse_fp_code(code)
prompt = build_image_prompt(parsed)
print(prompt)
```

## Design

- `parse_fp_code` parses the `FP::...` payload into typed fields (H/L/C, Lab metrics, wavelengths, color values).
- `build_image_prompt` maps parsed values to stable visual instructions that can be sent to an image model.
- Unknown tokens are preserved under `extras` to keep the parser forward-compatible.
