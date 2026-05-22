# med-research-digest

A personalized medical research newsletter generator. Searches PubMed for recent papers matching your specialty, grades the evidence, scores relevance to your practice, and writes a synthesized digest — powered by a multi-agent Claude pipeline.

**What you get:** A markdown file in `outputs/` with papers organized by relevance and evidence level, each with a synthesized paragraph written from the perspective of a clinician, methodologist, and specialist.

---

## How it works

```
PubMed (free API)
       ↓
  Discovery agent    — searches by your MeSH terms + date range
       ↓
  Evidence grader    — classifies study design, flags methodology concerns
       ↓
  Relevance filter   — scores 1-10 for your specific profile, drops irrelevant papers
       ↓
  Voices (parallel)  — clinician / methodologist / specialist / researcher / educator
       ↓
  Synthesizer        — one cohesive paragraph per paper blending all perspectives
       ↓
  outputs/YYYY-MM-DD.md
```

---

## Requirements

- Python 3.10 or later
- An [Anthropic API key](https://console.anthropic.com) (Claude powers all analysis agents)
- Internet access (PubMed is free, no account needed)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/med-research-digest.git
cd med-research-digest
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
```

Activate it:

- **Mac / Linux:** `source venv/bin/activate`
- **Windows:** `venv\Scripts\activate`

Then install:

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

Copy the example file:

```bash
cp .env.example .env
```

Open `.env` and fill in your Anthropic key:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

The `NCBI_API_KEY` line is optional. Leave it blank for standard PubMed access (3 requests/second), or add a free NCBI key for higher limits (10/second). Get one at [account.ncbi.nlm.nih.gov/settings](https://account.ncbi.nlm.nih.gov/settings/).

---

## Configure your profile

Open `context/physician.py` and fill in your details. Every field is optional, but the more you fill in, the more relevant your digest will be.

```python
PROFILE = {
    "name": "Dr. Ana Torres",
    "specialties": ["cardiology", "internal medicine"],
    "subspecialties": ["heart failure", "electrophysiology"],
    "role": ["clinician", "researcher"],     # see options below
    "practice_setting": "academic",          # see options below
    "country": "Mexico",
    "research_interests": ["SGLT2 inhibitors", "cardiac resynchronization"],
    "credentials": ["MD", "PhD", "FACC"],
    "patient_population": "adult",           # "adult", "pediatric", or "geriatric"
    "newsletter_preferences": {
        "max_papers": 10,                    # maximum papers per digest
        "min_evidence_level": "pilot",       # minimum study type to include
        "include_preprints": False,          # include bioRxiv / medRxiv?
        "language": "english",
    },
}
```

**`role` options** (you can have more than one):

| Value | Effect |
|---|---|
| `"clinician"` | Prioritizes RCTs, systematic reviews, guidelines |
| `"researcher"` | Includes broader article types; activates researcher voice |
| `"educator"` | Emphasizes reviews and guidelines; activates educator voice |
| `"resident"` | Includes case reports and clinical trials |
| `"fellow"` | Emphasizes RCTs and meta-analyses |

**`practice_setting` options:** `"academic"`, `"private"`, `"public_hospital"`, `"community"`

**Supported specialties and subspecialties** (use these exact strings in your profile):

```
Specialties:       cardiology, internal medicine, oncology, neurology, psychiatry,
                   pediatrics, surgery, emergency medicine, infectious disease,
                   rheumatology, endocrinology, gastroenterology, pulmonology,
                   nephrology, hematology, dermatology, ophthalmology, orthopedics,
                   geriatrics, obstetrics, gynecology, urology, radiology, anesthesiology

Subspecialties:    heart failure, electrophysiology, interventional cardiology,
                   neuro-oncology, child psychiatry, neonatology
```

Any specialty not in this list will be searched by free text in PubMed titles and abstracts.

---

## Run it

Make sure your virtual environment is active, then run from the project root.

### Basic usage

```bash
# Digest for the last 7 days (default)
python main.py

# Digest for the last 30 days
python main.py --days 30

# Focus on a single specialty, ignoring your profile specialties
python main.py --specialty oncology

# Preview what PubMed queries would run — no API calls made
python main.py --dry-run
```

### Recommended first run

Start with `--dry-run` to confirm your profile produces the queries you expect:

```bash
python main.py --dry-run
```

Then do a wider window to make sure papers are found:

```bash
python main.py --days 30
```

---

## Output

Each run saves a file to `outputs/YYYY-MM-DD.md`. Open it in any markdown viewer (VS Code, Obsidian, Typora, or paste into Notion).

Example structure:

```
# Medical Research Digest
2026-05-14 to 2026-05-21 | Dr. Ana Torres | cardiology, internal medicine | clinician, researcher

## Summary
| Tier | Papers |
| 🔴 High relevance, Level A evidence       | 2 |
| 🟡 Moderate relevance, Level A-B evidence | 4 |
| 🔵 Worth watching, Level C / early stage  | 3 |

---

## 🔴 High Relevance | Evidence Level A

🔴 **Dapagliflozin in Heart Failure with Mildly Reduced Ejection Fraction**
*McMurray JJ, Solomon SD, Inzucchi SE et al. — N Engl J Med (2026-May-15)*
[A Evidence | RCT] ⚠ industry funding

This multi-center RCT of 6,263 patients with HFmrEF demonstrates that dapagliflozin
reduces the composite of worsening heart failure or cardiovascular death by 18%...

[PubMed →](https://pubmed.ncbi.nlm.nih.gov/...)
```

**Evidence tiers:**
- 🔴 High relevance + Level A (meta-analysis or large RCT)
- 🟡 Moderate relevance + Level A or B
- 🔵 Worth watching (early stage, case series, or lower relevance score)

**Methodology flags** appear when a paper has concerns worth noting: `small sample`, `no control group`, `industry funding`, `single center`, `surrogate outcome`, etc.

---

## Console summary

After each run you'll see:

```
==================================================
med-research-digest complete
  Papers found:    47
  Papers included: 8
  🔴 High:         2
  🟡 Moderate:     4
  🔵 Watching:     2
  Saved to:        outputs/2026-05-21.md
==================================================
```

---

## Model configuration

Open `config.py` to control which Claude model each stage uses:

```python
# High-volume steps: evidence grading, relevance scoring, all voices
MODEL_FAST = "claude-haiku-4-5-20251001"

# Final synthesis only: the paragraph the physician actually reads
MODEL_SMART = "claude-sonnet-4-6"
```

The pipeline is split so cheaper, faster models handle the structured classification work (grading, scoring, short voice paragraphs), while the stronger model is reserved for the one output that matters most — the synthesized narrative per paper.

To find current model IDs: [docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)

---

## Troubleshooting

**"No specialties configured"**
Fill in `specialties` in `context/physician.py`, or use `--specialty cardiology` on the command line.

**"All papers filtered out"**
Try `--days 30` for a wider window, or `--specialty` to focus on one area. The relevance filter is strict when your profile is sparse — add more details (subspecialties, research interests) to improve scoring.

**Papers found but no 🔴 entries**
The 🔴 tier requires both relevance score ≥ 8 AND evidence level A. This is intentional — high-tier entries represent truly practice-relevant meta-analyses or large RCTs.

**Rate limit warning from PubMed**
Add an `NCBI_API_KEY` to your `.env` file (free registration). This raises the limit from 3 to 10 requests per second.

**`ModuleNotFoundError`**
Make sure your virtual environment is active (`source venv/bin/activate` or `venv\Scripts\activate`) before running.

---

## Privacy

This tool queries PubMed with your specialty terms only — your physician profile stays local and is never sent to PubMed. The profile is sent to Claude (Anthropic API) as context for relevance scoring and synthesis. Do not include patient data of any kind in the profile.

---

## Cost estimate

Each paper goes through approximately 9 Claude calls: 1 for evidence grading, 1 for relevance scoring, up to 6 voices (depending on your role configuration), and 1 for synthesis. The number of voices active depends on the `role` field in your profile — a clinician-only profile activates 3 voices (clinician, methodologist, gremial); adding researcher, educator, and specialties can reach 6–7.

**Measured reference** (110 papers processed, 5 active voices):

| Configuration | Cost |
|---|---|
| Default — `MODEL_FAST` = Haiku, `MODEL_SMART` = Sonnet | **~$4.82** |
| All Sonnet — both `MODEL_FAST` and `MODEL_SMART` = Sonnet | **~$7.60** |

**What can make your actual cost higher or lower:**

- **Number of papers.** Cost scales roughly linearly. 55 papers ≈ half the price; 220 papers ≈ double.
- **Number of active voices.** Each role you add to your profile activates more voices. A researcher + educator + 2 specialties profile runs ~7 voice calls per paper instead of 3.
- **Abstract length.** Longer abstracts mean more input tokens per call. Review articles and meta-analyses tend to have longer abstracts than brief reports.
- **Prompt length changes.** If you customize the system prompts in any of the voice or pipeline files, token counts will shift accordingly.
- **Model pricing changes.** Anthropic adjusts pricing over time. Check current rates at [anthropic.com/pricing](https://www.anthropic.com/pricing).
- **Lookback window.** A `--days 30` run will pull more papers from PubMed, most of which get filtered out before reaching Claude — but papers that pass the relevance filter all incur the full voice + synthesis cost.
