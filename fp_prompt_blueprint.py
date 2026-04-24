"""Blueprint parser for ARBE FP color codes and prompt generation.

This module converts compact strings like
`FP::H340_L050_C040::...::HEX_#AB5C90::RGB_171_92_144`
into structured data and a deterministic image prompt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class FPCode:
    """Structured representation of an FP code payload."""

    raw: str
    hue: int | None = None
    lightness: int | None = None
    chroma: int | None = None
    lab_l: float | None = None
    a: float | None = None
    b: float | None = None
    lambda_v2: float | None = None
    lambda_ee: float | None = None
    delta_lambda: float | None = None
    mu2: float | None = None
    sigma: float | None = None
    mu3: float | None = None
    hex_color: str | None = None
    rgb: Tuple[int, int, int] | None = None
    extras: Dict[str, str] | None = None


def parse_fp_code(code: str) -> FPCode:
    """Parse an FP code into a typed object.

    Parameters
    ----------
    code:
        Full FP string with `::` separators.

    Returns
    -------
    FPCode
        Parsed representation.
    """
    parts = [p.strip() for p in code.split("::") if p.strip()]
    if not parts or parts[0] != "FP":
        raise ValueError("FP code must start with 'FP::'")

    data: Dict[str, str] = {}
    extras: Dict[str, str] = {}

    for part in parts[1:]:
        if "_" in part:
            key, value = part.split("_", 1)
            if key == "RGB":
                data["RGB"] = value
            else:
                data[key] = value
        else:
            extras[part] = ""

    h, l, c = _parse_hlc(data.get("H340"), data.get("L050"), data.get("C040"), parts)

    rgb = None
    if "RGB" in data:
        values = data["RGB"].split("_")
        if len(values) == 3:
            rgb = tuple(int(v) for v in values)  # type: ignore[assignment]

    return FPCode(
        raw=code,
        hue=h,
        lightness=l,
        chroma=c,
        lab_l=_to_float(data.get("LabL")),
        a=_to_float(data.get("a")),
        b=_to_float(data.get("b")),
        lambda_v2=_to_float(data.get("λV2")),
        lambda_ee=_to_float(data.get("λEE")),
        delta_lambda=_to_float(data.get("Δλ")),
        mu2=_to_float(data.get("μ2")),
        sigma=_to_float(data.get("σ")),
        mu3=_to_float(data.get("μ3")),
        hex_color=data.get("HEX"),
        rgb=rgb,
        extras=extras or None,
    )


def _parse_hlc(h_token: str | None, l_token: str | None, c_token: str | None, parts: List[str]) -> Tuple[int | None, int | None, int | None]:
    """Extract H/L/C whether encoded standalone or merged (H340_L050_C040)."""
    h = int(h_token) if h_token and h_token.isdigit() else None
    l = int(l_token) if l_token and l_token.isdigit() else None
    c = int(c_token) if c_token and c_token.isdigit() else None

    if all(v is not None for v in (h, l, c)):
        return h, l, c

    for part in parts:
        if part.startswith("H") and "_L" in part and "_C" in part:
            chunks = part.split("_")
            for chunk in chunks:
                if chunk.startswith("H") and chunk[1:].isdigit():
                    h = int(chunk[1:])
                elif chunk.startswith("L") and chunk[1:].isdigit():
                    l = int(chunk[1:])
                elif chunk.startswith("C") and chunk[1:].isdigit():
                    c = int(chunk[1:])
    return h, l, c


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def build_image_prompt(parsed: FPCode) -> str:
    """Build a deterministic English image prompt from parsed FP values."""
    lines = [
        "Create a single abstract color-study image with no text or logos.",
        "Focus on smooth material gradients and subtle spectral transitions.",
    ]

    if parsed.hex_color:
        lines.append(f"Use {parsed.hex_color} as the dominant hue.")
    if parsed.rgb:
        lines.append(f"Target RGB balance near {parsed.rgb[0]}, {parsed.rgb[1]}, {parsed.rgb[2]}.")
    if parsed.hue is not None:
        lines.append(f"Hue anchor around {parsed.hue} degrees.")
    if parsed.lightness is not None:
        lines.append(f"Overall lightness around {parsed.lightness} on a 0-100 scale.")
    if parsed.chroma is not None:
        lines.append(f"Keep chroma restrained around {parsed.chroma} for a muted-modern look.")
    if parsed.a is not None and parsed.b is not None:
        lines.append(
            f"CIELAB drift: a* {parsed.a:+.2f}, b* {parsed.b:+.2f}; preserve this warm-magenta to cool-violet tension."
        )
    if parsed.delta_lambda is not None:
        mood = "asymmetric" if abs(parsed.delta_lambda) > 50 else "balanced"
        lines.append(f"Spectral behavior should feel {mood}, guided by Δλ {parsed.delta_lambda:+.3f}.")
    if parsed.sigma is not None:
        lines.append(f"Texture variance should stay fine-grained with sigma near {parsed.sigma:.3f}.")

    lines.append("Studio lighting, high fidelity, soft shadows, premium product-visual style.")
    return " ".join(lines)


if __name__ == "__main__":
    sample = (
        "FP::H340_L050_C040::H340::L050::C040::LabL_49.996::a+37.60::b-13.68::"
        "λV2_474.352::λEE_584.054::Δλ_-109.702::μ2_11714.359::σ_108.233::"
        "μ3_-494197.664::HEX_#AB5C90::RGB_171_92_144"
    )
    parsed = parse_fp_code(sample)
    print(build_image_prompt(parsed))
