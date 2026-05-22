from .clinician import analyze as clinician_voice
from .researcher import analyze as researcher_voice
from .educator import analyze as educator_voice
from .methodologist import analyze as methodologist_voice
from .gremial import analyze as gremial_voice
from .specialist import make_specialist_voice


def select_voices(profile: dict) -> dict[str, callable]:
    """
    Returns a dict mapping voice_name → async callable(paper: dict) -> str.

    Always active: clinician_voice, methodologist_voice, gremial_voice.
    Conditional on physician role and specialties.
    """
    voices: dict[str, callable] = {
        "clinician_voice": clinician_voice,
        "methodologist_voice": methodologist_voice,
        "gremial_voice": gremial_voice,
    }

    roles = [r.lower() for r in profile.get("role", [])]

    if "researcher" in roles:
        voices["researcher_voice"] = researcher_voice

    if "educator" in roles:
        voices["educator_voice"] = educator_voice

    for specialty in profile.get("specialties", []):
        key = f"specialist_voice_{specialty.replace(' ', '_')}"
        voices[key] = make_specialist_voice(specialty)

    return voices
