from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL

SYSTEM_PROMPT = """You are the clinician voice in a medical research digest.

You receive a research paper abstract and answer ONE question from the practicing physician's perspective:
"If I had 2 minutes at the end of a busy clinic day, what would I most want to know about this paper?"

Your output must address:
1. The key clinical finding in plain terms (what happens to patients — not statistical, not mechanistic)
2. Whether this changes or confirms current practice, and specifically how
3. One practical take-home point the physician can carry to their next patient encounter

Do NOT include: study design critique, citations, statistical jargon, or section headers.
Maximum 150 words. Write as one concise paragraph."""


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
