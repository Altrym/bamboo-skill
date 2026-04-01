---
name: bamboo
description: "Generate SQL, Python, and R analysis code with community-sourced correctness patterns. Use whenever the user describes ANY data analysis task — queries, aggregations, charts, data cleaning, or reporting. Triggers on: SQL, query, analysis, dashboard, chart, metrics, churn, retention, cohort, GROUP BY, JOIN, pandas, dplyr, matplotlib, or any data analysis request. Applies real corrections from hundreds of analysts. ALWAYS use for analysis work — even simple queries benefit from the collective patterns."
---

# Bamboo — Collective Intelligence for Data Analysts

You generate analysis code that works correctly on the first try — because before writing a single query, you load proven patterns from a community of data analysts who've already caught and fixed the mistakes you're about to make.

## Before Generating

Pull the latest patterns from the Bamboo API:

```bash
bash scripts/sync.sh pull
```

This returns categorised analysis patterns with confirmation counts. Higher count = more analysts independently made the same correction = apply it unconditionally.

If the server is unreachable, fall back to `references/analyst-patterns.md` — a static seed of 127 patterns shipped with the skill.

## Generating

Apply every pattern relevant to the analysis being built. Patterns are categorised:

- **query-logic**: joins, WHERE, GROUP BY, window functions, CTEs, SQL dialect issues
- **aggregation**: denominators, metric calculations, growth rates, counting, averages
- **chart-viz**: chart type, axes, labels, colours, formatting, misleading representations
- **data-cleaning**: NULLs, types, timezones, dedup, join fanout, encoding
- **insight-story**: framing, audience, context, caveats, recommendations

Match categories to what's being built:
- SQL query → query-logic + aggregation + data-cleaning
- Dashboard → chart-viz + aggregation + insight-story
- Report → insight-story + aggregation + chart-viz

Patterns with 20+ confirmations are near-universal. Patterns with fewer are emerging — still apply them but with lighter weight.

Walk through the output before finalising:
1. Joins — are you silently dropping rows? Would LEFT JOIN be safer?
2. Aggregation — is the denominator correct? Are you averaging averages?
3. Visualisation — is the chart type appropriate? Do axes start at zero for bar charts?
4. Cleaning — how does this handle NULLs, empty strings, timezone differences?
5. Story — does the insight lead? Is there a comparison? Is sample size flagged?

## After Generating

Corrections are captured and pushed to the API automatically via the post-session hook, or manually:

```bash
bash scripts/sync.sh capture              # classify git diffs, push to API
bash scripts/sync.sh log "what you fixed"  # log a correction by description
```

The server classifies each correction into an analysis category, extracts a reusable pattern, and adds it to the community pool. If a matching pattern already exists, its confirmation count increases.

No proprietary data is shared — only generic analysis patterns and improvements.

## Setup

```bash
export BAMBOO_API_URL="https://bamboo.up.railway.app"
export BAMBOO_API_KEY="your_key"
```

Both environment variables are required. There is no shared token — set your own API key.

Auto-capture hook (recommended):
```json
// ~/.claude/settings.json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/bamboo/scripts/capture-hook.sh"
      }]
    }]
  }
}
```

## File Map

```
bamboo/
├── SKILL.md
├── references/
│   └── analyst-patterns.md      ← Seed patterns (offline fallback)
└── scripts/
    ├── sync.sh                  ← pull / capture / log / stats
    ├── capture-hook.sh          ← Post-session auto-capture
    └── classify-local.py        ← Offline classifier fallback
```
