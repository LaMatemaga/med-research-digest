from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from config import MODEL_FAST as MODEL

SYSTEM_PROMPT = """You are the gremial (professional societies and conferences) voice in a medical research digest.

You receive a research paper and address the professional landscape around this topic:
1. Which specialty society or guideline body would be most interested in this finding? (name them: AHA, ESC, ASCO, AAN, ACG, etc.)
2. Is this the type of result that could influence upcoming guidelines?
3. Are there active working groups, consensus efforts, or major upcoming congresses focused on this topic?
4. Are there conflict-of-interest considerations worth noting (industry funding, authors from industry-funded groups)?

Be specific about society names when known. Maximum 120 words. Write as one paragraph."""


async def analyze(paper: dict) -> str:
    prompt = (
        f"Title: {paper.get('title', '')}\n"
        f"Journal: {paper.get('journal', '')} ({paper.get('pub_date', '')})\n"
        f"Source specialty: {paper.get('source_specialty', '')}\n"
        f"Methodology flags: {', '.join(paper.get('methodology_flags', [])) or 'none'}\n"
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
