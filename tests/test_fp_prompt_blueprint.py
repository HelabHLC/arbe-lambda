from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fp_prompt_blueprint import build_image_prompt, parse_fp_code


def test_parse_fp_code_extracts_core_fields():
    code = (
        "FP::H340_L050_C040::H340::L050::C040::LabL_49.996::a+37.60::b-13.68::"
        "λV2_474.352::λEE_584.054::Δλ_-109.702::μ2_11714.359::σ_108.233::"
        "μ3_-494197.664::HEX_#AB5C90::RGB_171_92_144"
    )
    parsed = parse_fp_code(code)

    assert parsed.hue == 340
    assert parsed.lightness == 50
    assert parsed.chroma == 40
    assert parsed.hex_color == "#AB5C90"
    assert parsed.rgb == (171, 92, 144)
    assert parsed.lambda_v2 == 474.352
    assert parsed.delta_lambda == -109.702


def test_build_image_prompt_contains_expected_guidance():
    parsed = parse_fp_code(
        "FP::H340_L050_C040::a+37.60::b-13.68::Δλ_-109.702::σ_108.233::HEX_#AB5C90::RGB_171_92_144"
    )
    prompt = build_image_prompt(parsed)

    assert "#AB5C90" in prompt
    assert "171, 92, 144" in prompt
    assert "asymmetric" in prompt
    assert "no text or logos" in prompt
