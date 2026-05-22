from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL

SYSTEM_PROMPT = """You are the methodologist voice in a medical research digest.

You receive a research paper and provide a statistical and methodological critique:
1. Is the study design appropriate for the research question?
2. What are the key threats to internal validity? (confounding, selection bias, lack of blinding)
3. What are the threats to external validity? (population selection, setting generalizability)
4. Are the statistical methods sound? (underpowered? multiple comparisons? appropriate endpoints? ITT analysis?)
5. How much should a clinician trust this finding given these limitations?

Be specific. Maximum 120 words. Write as one concise paragraph.
Do not summarize the clinical findings — focus only on methodological quality."""


async def analyze(paper: dict) -> str:
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
        f"Study design: {paper.get('study_design', 'unknown')}\n"
        f"Methodology flags: {', '.join(paper.get('methodology_flags', [])) or 'none identified'}\n"
        f"Abstract:\n{paper.get('abstract', '')}"
    )
    options = ClaudeAgentOptions(system_prompt=SYSTEM_PROMPT, max_turns=1, model=MODEL)
    result = []
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    result.append(block.text)
    return "\n".join(result)
