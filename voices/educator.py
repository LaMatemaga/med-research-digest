from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL

SYSTEM_PROMPT = """You are the educator voice in a medical research digest.

You receive a research paper and answer: how would you teach this to a medical student or resident?
1. What core concept does this paper best illustrate?
2. What analogy or mental model makes this finding memorable?
3. Is there a common misconception this paper corrects or reinforces?
4. Is it worth discussing at morning report, journal club, or teaching rounds — and why?

Do not focus on clinical application (another voice covers that). Focus on teaching value.
Maximum 130 words. Write as one paragraph."""


async def analyze(paper: dict) -> str:
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
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
