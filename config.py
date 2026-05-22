# Model configuration for the med-research-digest pipeline.
# To find current model IDs: https://docs.anthropic.com/en/docs/about-claude/models

# --- Available options (as of May 2026) ---
# "claude-haiku-4-5-20251001"   — fastest and cheapest; ideal for high-volume structured tasks
# "claude-sonnet-4-6"           — balanced quality and speed; good default for most tasks
# "claude-opus-4-7"             — highest reasoning quality; best for nuanced synthesis

# High-volume steps: evidence grading, relevance scoring, and all voices.
# These run once per paper and produce short, structured outputs — speed matters more than depth.
MODEL_FAST = "claude-haiku-4-5-20251001"

# Final synthesis step only: one paragraph per paper blending all voice perspectives.
# This is the output the physician actually reads — quality matters most here.
MODEL_SMART = "claude-sonnet-4-6"
