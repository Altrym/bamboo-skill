#!/usr/bin/env python3
"""
Bamboo Local Classifier — Offline fallback for diff classification.
Uses keyword matching when the server API is unreachable.
Not as accurate as the server's LLM-based classification, but works offline.

Usage: echo "diff content" | python3 classify-local.py filename.sql
"""

import sys
import json

CATEGORY_SIGNALS = {
    "query-logic": ["join", "left join", "inner join", "right join", "cross join",
                     "where", "group by", "having", "order by", "distinct",
                     "window", "over(", "partition by", "row_number", "rank(",
                     "lag(", "lead(", "cte", "with ", "subquery",
                     "union", "intersect", "except", "exists", "in (",
                     "case when", "coalesce", "nullif", "cast(", "between"],
    "aggregation": ["count(", "sum(", "avg(", "average", "min(", "max(",
                    "denominator", "numerator", "ratio", "rate",
                    "churn", "retention", "growth", "yoy", "mom", "wow",
                    "cohort", "distinct", "dedup", "metric",
                    "sumif", "countif", "averageif"],
    "chart-viz": ["chart", "plot", "graph", "axis", "axes", "legend",
                  "matplotlib", "plotly", "seaborn", "ggplot", "altair",
                  "bar chart", "line chart", "pie chart", "scatter",
                  "histogram", "heatmap", "colour", "color", "label",
                  "title", "annotation", "figsize", "subplot"],
    "data-cleaning": ["null", "none", "nan", "na ", "is null", "is not null",
                      "fillna", "dropna", "isnull", "notnull", "coalesce",
                      "timezone", "utc", "tz_convert", "tz_localize",
                      "to_datetime", "strptime", "as.date", "parse_date",
                      "encoding", "utf-8", "strip", "trim", "clean",
                      "duplicate", "dedup", "drop_duplicates", "distinct",
                      "fanout", "row count", "type", "cast", "astype"],
    "insight-story": ["finding", "insight", "recommendation", "summary",
                      "executive", "stakeholder", "audience", "context",
                      "caveat", "limitation", "sample size", "significance",
                      "confidence", "comparison", "benchmark", "target",
                      "report", "narrative", "headline", "takeaway"],
}


def classify(filename: str, diff_text: str) -> dict:
    text = (filename + " " + diff_text).lower()

    scores = {}
    for category, signals in CATEGORY_SIGNALS.items():
        score = sum(1 for s in signals if s.lower() in text)
        if score > 0:
            scores[category] = score

    if not scores:
        return {
            "category": "general",
            "pattern": f"Unclassified correction in {filename}",
            "is_analysis_relevant": True
        }

    best_cat = max(scores, key=scores.get)

    # Extract a rough pattern from the diff
    added_lines = [l[1:].strip() for l in diff_text.split("\n") if l.startswith("+") and not l.startswith("+++")]
    removed_lines = [l[1:].strip() for l in diff_text.split("\n") if l.startswith("-") and not l.startswith("---")]

    # Build a rough description
    if added_lines and removed_lines:
        pattern = f"Changed: '{removed_lines[0][:50]}' → '{added_lines[0][:50]}'"
    elif added_lines:
        pattern = f"Added: '{added_lines[0][:60]}'"
    elif removed_lines:
        pattern = f"Removed: '{removed_lines[0][:60]}'"
    else:
        pattern = f"Correction in {filename}"

    return {
        "category": best_cat,
        "pattern": pattern,
        "is_analysis_relevant": True
    }


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    diff_text = sys.stdin.read()
    result = classify(filename, diff_text)
    print(json.dumps(result))
