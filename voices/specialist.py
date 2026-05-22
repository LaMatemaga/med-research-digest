from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL


def make_specialist_voice(specialty: str):
    """
    Factory that returns an async analyze(paper: dict) -> str function
    with a system prompt parameterized by specialty name.
    """
    system_prompt = f"""You are the {specialty} specialist voice in a medical research digest.

You receive a research paper and provide the subspecialty expert perspective:
1. How does this finding fit within the current {specialty} practice landscape?
2. What would a {specialty} specialist notice that a generalist might miss?
3. Any nuances specific to {specialty} patients (epidemiology, comorbidities, drug interactions, typical presentation)?
4. How does this compare to current {specialty} guidelines or standard of care?

Maximum 150 words. Write as one paragraph from a {specialty} expert's perspective.
Do not repeat the abstract — add specialist context."""

    async def analyze(paper: dict) -> str:
        prompt = (
            f"Title: {paper.get('title', '')}\n"
            f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
            f"Evidence level: {paper.get('evidence_level', 'C')} ({paper.get('study_design', 'unknown')})\n"
            f"Abstract:\n{paper.get('abstract', '')}"
        )
        options = ClaudeAgentOptions(system_prompt=system_prompt, max_turns=1, model=MODEL)
        result = []
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        result.append(block.text)
        return "\n".join(result)

    analyze.__name__ = f"specialist_voice_{specialty.replace(' ', '_')}"
    return analyze
