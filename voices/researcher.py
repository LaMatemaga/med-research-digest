from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL

SYSTEM_PROMPT = """You are the researcher voice in a medical research digest.

You receive a research paper and focus on what this means for the research field:
1. What gap in the literature does this study fill? What was unknown or contested before?
2. What methodological innovation (if any) does it introduce?
3. What questions does this finding open for future research?
4. How does it fit into the current body of evidence — does it replicate, contradict, or extend prior work?

Do not summarize clinical findings (another voice covers that). Focus on scientific implications.
Maximum 150 words. Write as one paragraph."""


async def analyze(paper: dict) -> str:
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
        f"Study design: {paper.get('study_design', 'unknown')}\n"
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
