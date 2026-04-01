# Bamboo

Collective intelligence for data analysts. Every correction feeds the next generation.

127 seed patterns. Server-synced community pool. Gets better with every analyst.

## Install

```bash
claude skill install bamboo.skill
```

## Setup

```bash
# Connect to the community server
export BAMBOO_API_URL="https://bamboo.up.railway.app"
export BAMBOO_API_KEY="your_key"

# Auto-capture corrections after every session (optional, recommended)
# Add to ~/.claude/settings.json:
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

## How It Works

1. You describe an analysis → skill loads community patterns from server before generating
2. Output uses correct joins, proper denominators, appropriate chart types from the start
3. You edit the output → post-session hook captures the diff
4. Diff is classified by the server and added to the community pool
5. Next analyst gets better output because of your fix

Works without the server too — falls back to 127 seed patterns in `references/analyst-patterns.md`.

## Commands

```bash
bash scripts/sync.sh pull      # Get latest community patterns
bash scripts/sync.sh capture   # Classify current git diffs & push
bash scripts/sync.sh log "description of what you fixed"
bash scripts/sync.sh stats     # Community stats
```

## Categories

Query Logic · Aggregation · Charts & Viz · Data Cleaning · Insight & Story

## License

MIT
