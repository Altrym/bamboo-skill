# Bamboo Community Analysis Patterns

> **Version**: 0.1.0 (seed)  
> **Patterns**: 127  
> **Contributors**: Seed from maintainers — community contributions start now  
> **Last Updated**: 2026-04-01

Every pattern below is a specific analysis correction. They are written as instructions because that's what they are — direct fixes for mistakes that AI-generated analysis makes repeatedly. The confirmation count will increase as more analysts validate each pattern.

Read the categories relevant to your current generation task. You don't need to read all 127 for every task — match categories to the analysis you're building.

---

## References (12 patterns)

**REF-001** · Use structured table references (`Table1[Column]`) instead of raw range references (`A2:A100`) whenever the data is in an Excel Table. Structured references auto-expand when rows are added and are self-documenting. Raw ranges silently exclude new data.
`confirmations: seed · category: references`

**REF-002** · Lock row and column references with `$` signs when a formula will be copied across cells. `$A$1` is absolute (never changes), `A$1` locks the row, `$A1` locks the column. AI-generated formulas almost always forget to lock the lookup range, causing #N/A errors when the formula is dragged.
`confirmations: seed · category: references`

**REF-003** · Never use `INDIRECT()` to construct references from strings unless there is no alternative. INDIRECT is volatile (recalculates on every change), breaks when sheets are renamed, and cannot be audited by Excel's formula tracing tools. Use INDEX/MATCH, XLOOKUP, or structured references instead.
`confirmations: seed · category: references`

**REF-004** · Named ranges should be used for constants and key reference cells (tax rate, start date, threshold values). They make formulas readable — `=Revenue*TaxRate` is instantly clear, `=B14*$G$2` is not. Define them via Formulas > Name Manager.
`confirmations: seed · category: references`

**REF-005** · When building dynamic ranges that grow with data, prefer `OFFSET(start, 0, 0, COUNTA(column), 1)` or better yet, convert the data to an Excel Table. OFFSET-based dynamic ranges are volatile. Tables are the modern, non-volatile solution.
`confirmations: seed · category: references`

**REF-006** · Cross-sheet references must include the sheet name in single quotes if the sheet name contains spaces: `='Sales Data'!A1`, not `=Sales Data!A1`. Missing quotes cause #REF! errors. Always include quotes defensively even when the name has no spaces — it never hurts.
`confirmations: seed · category: references`

**REF-007** · When referencing an entire column (`A:A`), be aware this includes the header row. In SUMIF/COUNTIF this usually doesn't matter, but in MATCH or array formulas it can return the wrong position. Reference the data range explicitly (`A2:A1000` or `Table1[Column]`).
`confirmations: seed · category: references`

**REF-008** · Mixed references are the correct choice for multiplication tables and two-variable data tables. Use `$A2*B$1` so the row locks to column A and the column locks to row 1 when the formula is copied in both directions. Pure absolute or pure relative references will not work for grid-fill patterns.
`confirmations: seed · category: references`

**REF-009** · R1C1 reference style is useful for understanding relative references programmatically, but always deliver formulas in A1 style unless the user explicitly requests R1C1. Most users cannot read R1C1 notation and will think the formula is broken.
`confirmations: seed · category: references`

**REF-010** · When a formula references a cell on another workbook (`=[Book2.xlsx]Sheet1!A1`), that external reference will break when the other workbook is closed or moved. Warn the user about this fragility and suggest copying the data locally or using Power Query instead.
`confirmations: seed · category: references`

**REF-011** · In Google Sheets, use `ARRAYFORMULA` with range references (`A2:A`) to create open-ended ranges that auto-include new rows. In Excel 365 with dynamic arrays, the equivalent is a spill range. Do not assume one syntax works in the other — they are different formula engines.
`confirmations: seed · category: references`

**REF-012** · When providing a range for data validation dropdowns or conditional formatting rules, use absolute references (`$A$2:$A$20`). Relative references in these contexts shift based on the active cell, causing the validation source to point to the wrong range for different cells.
`confirmations: seed · category: references`

---

## Error Handling (10 patterns)

**ERR-001** · Wrap lookup formulas in `IFERROR()` or `IFNA()` to handle missing values gracefully. Prefer `IFNA()` over `IFERROR()` for lookups because IFNA only catches #N/A (lookup miss), while IFERROR masks ALL errors including legitimate ones like #REF! or #VALUE! that indicate real problems.
`confirmations: seed · category: error-handling`

**ERR-002** · Never use `IFERROR(formula, "")` to silently hide errors. An empty string hides the problem and makes debugging impossible. Use a meaningful fallback: `IFERROR(VLOOKUP(...), "Not found")` or `IFERROR(calculation, 0)` depending on context.
`confirmations: seed · category: error-handling`

**ERR-003** · Check for blank cells before division: `=IF(B2=0, 0, A2/B2)` or `=IF(ISBLANK(B2), "", A2/B2)`. AI-generated formulas that divide almost never guard against #DIV/0! errors. This is the most common spreadsheet error in generated formulas.
`confirmations: seed · category: error-handling`

**ERR-004** · Error cascading happens when one formula errors and downstream formulas that reference it also error. Prevent this by handling errors at the source, not at every downstream cell. One well-placed IFERROR is better than twenty.
`confirmations: seed · category: error-handling`

**ERR-005** · `ISERROR()` returns TRUE/FALSE but does not fix the error. It is only useful inside IF: `=IF(ISERROR(A1), "fallback", A1)`. But this evaluates the formula twice, which is wasteful. Use `IFERROR(A1, "fallback")` instead — it evaluates once and is cleaner.
`confirmations: seed · category: error-handling`

**ERR-006** · When using AGGREGATE function to ignore errors, specify option 6 (ignore error values) in the second argument. `AGGREGATE(9, 6, range)` sums a range while skipping error cells. This is vastly preferable to adding IFERROR wrappers to every cell in the source range.
`confirmations: seed · category: error-handling`

**ERR-007** · `ISBLANK()` only returns TRUE for truly empty cells. A cell containing an empty string (`""`) or a space character is NOT blank. If users might enter spaces, use `=IF(TRIM(A1)="", ...)` instead of `=IF(ISBLANK(A1), ...)`.
`confirmations: seed · category: error-handling`

**ERR-008** · When chaining multiple lookups or calculations, use `LET()` to compute intermediate values and check them for errors before proceeding. This avoids deeply nested IFERROR calls and makes the error handling logic readable: `=LET(val, XLOOKUP(...), IF(ISERROR(val), "Missing", val*1.1))`.
`confirmations: seed · category: error-handling`

**ERR-009** · #VALUE! errors usually mean a formula expects a number but received text. Before performing arithmetic on cells that might contain text, wrap with `VALUE()` or guard with `ISNUMBER()`. Common culprit: cells that look like numbers but are stored as text after CSV import.
`confirmations: seed · category: error-handling`

**ERR-010** · #NAME? errors mean Excel does not recognize a function name. This happens when using Excel 365 functions (XLOOKUP, FILTER, LET) in older Excel versions, or when a named range is misspelled. Always note which Excel version a formula requires and warn about compatibility.
`confirmations: seed · category: error-handling`

---

## Lookups (12 patterns)

**LKP-001** · Prefer `INDEX/MATCH` over `VLOOKUP` for lookups. VLOOKUP breaks when columns are inserted/deleted (because the column index number shifts), cannot look left, and requires the lookup column to be the first column. INDEX/MATCH has none of these limitations.
`confirmations: seed · category: lookups`

**LKP-002** · Prefer `XLOOKUP` over both VLOOKUP and INDEX/MATCH when targeting Excel 365 or Google Sheets. XLOOKUP defaults to exact match (no need to remember the `FALSE` argument), supports left-side lookups, and can return entire rows/columns. Always confirm the user's Excel version first.
`confirmations: seed · category: lookups`

**LKP-003** · VLOOKUP's fourth argument: `FALSE` means exact match, `TRUE` (or omitted) means approximate match. AI-generated VLOOKUPs constantly omit the fourth argument, defaulting to approximate match, which returns wrong results unless the data is sorted ascending. Always specify `FALSE` for exact match.
`confirmations: seed · category: lookups`

**LKP-004** · For multiple-criteria lookups, use `INDEX/MATCH` with array multiplication: `=INDEX(C:C, MATCH(1, (A:A=criteria1)*(B:B=criteria2), 0))`. In older Excel, this requires Ctrl+Shift+Enter. In Excel 365, it spills automatically. XLOOKUP can also handle this with concatenated lookup arrays.
`confirmations: seed · category: lookups`

**LKP-005** · Left-side lookups (returning a value from a column to the LEFT of the lookup column) are impossible with VLOOKUP. Use `INDEX/MATCH` or `XLOOKUP`. This is the number one reason to avoid VLOOKUP entirely.
`confirmations: seed · category: lookups`

**LKP-006** · When VLOOKUP or XLOOKUP returns #N/A but the value clearly exists in the range, the cause is almost always a data type mismatch — the lookup value is text but the table contains numbers, or vice versa. Force consistency with `VALUE()` for numbers or `TEXT()` for strings.
`confirmations: seed · category: lookups`

**LKP-007** · For two-way lookups (match on both a row header and a column header), use `INDEX(range, MATCH(row_criteria, row_headers, 0), MATCH(col_criteria, col_headers, 0))`. This is the only clean way to do a matrix lookup.
`confirmations: seed · category: lookups`

**LKP-008** · `XLOOKUP` has a powerful `if_not_found` argument (third parameter) that replaces the need for IFERROR wrapping: `=XLOOKUP(val, lookup, return, "Not found")`. Use it instead of `IFERROR(XLOOKUP(...), "Not found")` — it's cleaner and evaluates the formula only once.
`confirmations: seed · category: lookups`

**LKP-009** · Approximate match lookups (`VLOOKUP` with TRUE, or `MATCH` with 1) require the lookup range to be sorted in ascending order. If the data is not sorted, the result will be silently wrong — no error, just the wrong value. This is one of the most dangerous Excel behaviors.
`confirmations: seed · category: lookups`

**LKP-010** · `CHOOSECOLS()` and `CHOOSEROWS()` (Excel 365) let you rearrange columns/rows from a range, which is useful for restructuring lookup return ranges. `=CHOOSECOLS(A1:E10, 3, 1, 5)` returns columns C, A, E in that order. Use these to avoid helper columns.
`confirmations: seed · category: lookups`

**LKP-011** · When performing a lookup that should return the LAST match (not the first), XLOOKUP has a search mode argument: `=XLOOKUP(val, range, return,,, -1)` searches bottom-to-top. With INDEX/MATCH, use `MATCH(val, range, 1)` on a sorted range or use LOOKUP with a large range trick.
`confirmations: seed · category: lookups`

**LKP-012** · Wildcard lookups use `*` (any characters) and `?` (single character) in VLOOKUP, MATCH, and XLOOKUP (with match mode 2). To find a partial text match: `=VLOOKUP("*"&search_term&"*", range, col, FALSE)`. Always use match mode 2 in XLOOKUP for wildcards.
`confirmations: seed · category: lookups`

---

## Aggregation (8 patterns)

**AGG-001** · Prefer `SUMIFS` over `SUMIF`. SUMIFS supports multiple criteria, and its argument order is consistent: `SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2)`. SUMIF has a confusing argument order and only supports one criterion. SUMIFS works for single criteria too.
`confirmations: seed · category: aggregation`

**AGG-002** · `AGGREGATE` is the most underused function in Excel. It can perform 19 different calculations (SUM, AVERAGE, COUNT, MIN, MAX, etc.) while ignoring errors, hidden rows, or nested SUBTOTAL/AGGREGATE results. Use `AGGREGATE(9, 6, range)` instead of SUM with IFERROR on every cell.
`confirmations: seed · category: aggregation`

**AGG-003** · `SUBTOTAL` respects filters — it only includes visible rows. Use `SUBTOTAL(9, range)` instead of `SUM(range)` when the data might be filtered. The function number 9 = SUM, 1 = AVERAGE, 2 = COUNT, 3 = COUNTA, etc. Function numbers 101-111 also ignore manually hidden rows.
`confirmations: seed · category: aggregation`

**AGG-004** · For array-based conditional aggregation in Excel 365, use `SUM(FILTER(range, condition))` instead of `SUMPRODUCT((condition)*range)`. The FILTER approach is more readable and often faster. In older Excel, SUMPRODUCT with boolean multiplication is the only option.
`confirmations: seed · category: aggregation`

**AGG-005** · `SUMPRODUCT` does not need Ctrl+Shift+Enter — it is NOT an array formula. It naturally handles arrays. Use it for weighted sums, conditional counts, and multi-criteria aggregation in pre-365 Excel: `=SUMPRODUCT((A2:A100="East")*(B2:B100>1000)*(C2:C100))`.
`confirmations: seed · category: aggregation`

**AGG-006** · When using structured table references in SUMIFS, reference the entire column: `=SUMIFS(Table1[Amount], Table1[Region], "East")`. Do not mix structured and A1 references in the same SUMIFS call — this causes range size mismatch errors.
`confirmations: seed · category: aggregation`

**AGG-007** · COUNTIFS with date criteria requires wrapping dates in quotes and comparison operators as strings: `=COUNTIFS(A:A, ">="&DATE(2024,1,1), A:A, "<"&DATE(2024,2,1))`. Passing raw date values without the string concatenation pattern returns wrong counts.
`confirmations: seed · category: aggregation`

**AGG-008** · For running totals (cumulative sums), use `=SUM($B$2:B2)` with the first reference absolute and the second relative, then drag down. In Excel 365 with Tables, the equivalent is `=SUM(INDEX(Table1[Amount],1):[@Amount])`. Do not use a volatile OFFSET-based approach for running totals.
`confirmations: seed · category: aggregation`

---

## Dates (8 patterns)

**DAT-001** · Always construct dates with `DATE(year, month, day)` rather than entering date strings like `"1/15/2024"`. Date strings are locale-dependent — `"1/2/2024"` is January 2 in the US but February 1 in Europe. `DATE()` is unambiguous and locale-safe.
`confirmations: seed · category: dates`

**DAT-002** · `EOMONTH(date, 0)` returns the last day of the same month. `EOMONTH(date, -1)` returns the last day of the previous month. This is essential for month-end reporting. AI formulas often manually construct month-end dates with `DATE(YEAR(A1), MONTH(A1)+1, 0)` — use EOMONTH instead, it's cleaner.
`confirmations: seed · category: dates`

**DAT-003** · `NETWORKDAYS(start, end, holidays)` counts working days (excluding weekends and optional holidays). Use `NETWORKDAYS.INTL` when the weekend is not Saturday-Sunday (common in Middle Eastern locales). Always ask about the weekend convention for the user's region.
`confirmations: seed · category: dates`

**DAT-004** · Date arithmetic in Excel uses serial numbers. `=A1+30` adds 30 calendar days to a date. But "add one month" is NOT the same as "add 30 days." Use `EDATE(A1, 1)` to add exactly one calendar month. `EDATE(DATE(2024,1,31), 1)` correctly returns Feb 29, 2024 (leap year).
`confirmations: seed · category: dates`

**DAT-005** · `TEXT(date, "MMMM YYYY")` formats a date for display, but the result is a TEXT string that cannot be used in date calculations. Never use TEXT for intermediate date values — only for final display output. Downstream formulas that expect dates will fail with #VALUE! on text-formatted dates.
`confirmations: seed · category: dates`

**DAT-006** · `DATEDIF(start, end, unit)` calculates the difference between dates in years ("Y"), months ("M"), or days ("D"). It is undocumented in modern Excel but still works. The start date must be before the end date or it returns #NUM!. This is the cleanest way to calculate age from birthdate.
`confirmations: seed · category: dates`

**DAT-007** · When dates imported from CSV or external sources don't sort correctly or can't be used in calculations, they are likely stored as text. Convert with `DATEVALUE(A1)` or `VALUE(A1)`. A quick check: if `ISNUMBER(A1)` returns FALSE for a cell that looks like a date, it's text.
`confirmations: seed · category: dates`

**DAT-008** · `WEEKDAY(date, 2)` returns 1 (Monday) through 7 (Sunday) using the ISO standard. The default `WEEKDAY(date)` returns 1 for Sunday, which confuses most users outside North America. Always specify the second argument explicitly to avoid ambiguity.
`confirmations: seed · category: dates`

---

## Text (8 patterns)

**TXT-001** · `TEXTJOIN(delimiter, ignore_empty, range)` is the modern replacement for concatenation. `=TEXTJOIN(", ", TRUE, A1:A10)` joins all non-empty cells with a comma. It replaced the tedious `=A1&", "&A2&", "&A3` pattern. Available in Excel 2019+ and Excel 365.
`confirmations: seed · category: text`

**TXT-002** · `CONCAT()` replaces `CONCATENATE()` and accepts ranges: `=CONCAT(A1:A5)` joins A1 through A5 with no delimiter. `CONCATENATE` only accepts individual cell references and is a legacy function. However, for delimited joining, TEXTJOIN is better than CONCAT.
`confirmations: seed · category: text`

**TXT-003** · Always `TRIM()` external data. Imported data often has leading/trailing spaces that cause lookup mismatches — `"Smith "` does not match `"Smith"`. Wrap lookup values in TRIM: `=VLOOKUP(TRIM(A1), range, col, FALSE)`. Also consider `CLEAN()` to remove non-printable characters.
`confirmations: seed · category: text`

**TXT-004** · To extract text before/after/between delimiters, combine `LEFT`, `MID`, `RIGHT` with `FIND` or `SEARCH`. `FIND` is case-sensitive; `SEARCH` is case-insensitive and supports wildcards. Example: `=LEFT(A1, FIND(" ", A1)-1)` extracts the first word. In Excel 365, `TEXTSPLIT` and `TEXTBEFORE`/`TEXTAFTER` are much cleaner alternatives.
`confirmations: seed · category: text`

**TXT-005** · When a cell looks like a number but won't calculate (left-aligned, green triangle in corner), it's stored as text. Convert with `=VALUE(A1)` or multiply by 1: `=A1*1` or `=A1+0`. This is the most common data import issue and the most common cause of SUM returning 0 on a range full of "numbers."
`confirmations: seed · category: text`

**TXT-006** · `SUBSTITUTE(text, old, new, instance)` replaces text occurrences. The optional fourth argument specifies which occurrence to replace — omit it to replace all. For removing characters, use an empty string: `=SUBSTITUTE(A1, "-", "")` strips all hyphens. This is more flexible than REPLACE, which works by position.
`confirmations: seed · category: text`

**TXT-007** · For multi-step text transformations, nest SUBSTITUTE calls or use LET for readability: `=LET(step1, SUBSTITUTE(A1, "-", ""), step2, SUBSTITUTE(step1, " ", ""), TRIM(step2))`. Deeply nested SUBSTITUTE calls without LET are unreadable and unmaintainable.
`confirmations: seed · category: text`

**TXT-008** · `TEXT()` is essential for combining dates or numbers into strings: `="Report for "&TEXT(A1, "MMMM YYYY")` produces "Report for January 2024". Without TEXT, the date displays as a serial number: "Report for 45292". Always use TEXT when concatenating non-text values into display strings.
`confirmations: seed · category: text`

---

## Logic (8 patterns)

**LOG-001** · Replace deeply nested IF formulas with `IFS()` (Excel 2019+/365). `=IFS(A1>90, "A", A1>80, "B", A1>70, "C", TRUE, "F")` is far more readable than `=IF(A1>90, "A", IF(A1>80, "B", IF(A1>70, "C", "F")))`. The `TRUE` at the end acts as an else/default.
`confirmations: seed · category: logic`

**LOG-002** · `SWITCH(value, match1, result1, match2, result2, ..., default)` is cleaner than nested IF when matching discrete values: `=SWITCH(A1, 1, "Low", 2, "Medium", 3, "High", "Unknown")`. IFS is better for condition ranges; SWITCH is better for exact-value matching.
`confirmations: seed · category: logic`

**LOG-003** · AND/OR inside IF: `=IF(AND(A1>0, B1>0), "Both positive", "No")` and `=IF(OR(A1="Yes", B1="Yes"), "At least one", "None")`. AI-generated formulas often write `=IF(A1>0 AND B1>0, ...)` which is invalid syntax. AND() and OR() are separate functions that must wrap the conditions.
`confirmations: seed · category: logic`

**LOG-004** · Boolean math trick: TRUE = 1 and FALSE = 0 in Excel. So `=SUMPRODUCT((A1:A10>5)*1)` counts how many values exceed 5. And `=(A1="Yes")*(B1>100)*C1` multiplies C1 only when both conditions are true. This replaces many SUMIFS and IF patterns with cleaner formulas.
`confirmations: seed · category: logic`

**LOG-005** · `CHOOSE(index, val1, val2, val3, ...)` returns the value at the given position. It is excellent for index-based branching: `=CHOOSE(MONTH(A1), "Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4")` maps months to quarters. Cleaner than 12-deep nested IF.
`confirmations: seed · category: logic`

**LOG-006** · `LET(name1, value1, name2, value2, ..., calculation)` assigns names to intermediate results. This prevents redundant calculation and makes complex formulas readable: `=LET(total, SUM(A:A), avg, AVERAGE(A:A), IF(total>1000, total*1.1, avg))`. Available in Excel 365 and Google Sheets.
`confirmations: seed · category: logic`

**LOG-007** · When an IF formula returns TRUE/FALSE, you probably don't need IF at all. `=IF(A1>10, TRUE, FALSE)` is just `=A1>10`. Similarly, `=IF(A1>10, 1, 0)` is just `=(A1>10)*1`. Unnecessary IF wrappers around boolean expressions are the most common logic redundancy in generated formulas.
`confirmations: seed · category: logic`

**LOG-008** · `NOT()` inverts a boolean. Use it for readability: `=IF(NOT(ISBLANK(A1)), A1*2, 0)` is clearer than `=IF(ISBLANK(A1), 0, A1*2)` when the focus is on the non-blank case. However, avoid double negation — `NOT(NOT(x))` is just `x`.
`confirmations: seed · category: logic`

---

## Arrays (8 patterns)

**ARR-001** · Dynamic arrays (Excel 365) spill results into adjacent cells automatically. `=FILTER(A2:C100, B2:B100="East")` returns all matching rows, spilling down. Do not wrap dynamic array formulas in Ctrl+Shift+Enter — they are not legacy CSE array formulas. If you see `{=formula}` braces, you're in legacy mode.
`confirmations: seed · category: arrays`

**ARR-002** · `FILTER(array, include, [if_empty])` is the most important dynamic array function. Always provide the third argument for the empty case: `=FILTER(range, condition, "No results")`. Without it, #CALC! error appears when no rows match, which panics users.
`confirmations: seed · category: arrays`

**ARR-003** · `SORT(array, sort_index, sort_order)` and `SORTBY(array, by_array, sort_order)` sort dynamically. SORTBY is more flexible because the sort column doesn't need to be in the output: `=SORTBY(Names, Scores, -1)` sorts names by scores descending without including scores in the output.
`confirmations: seed · category: arrays`

**ARR-004** · `UNIQUE(array, by_col, exactly_once)` extracts distinct values. By default it returns all distinct values. Set the third argument to TRUE to return values that appear exactly once (no duplicates): `=UNIQUE(A2:A100,, TRUE)`. This is useful for finding anomalies.
`confirmations: seed · category: arrays`

**ARR-005** · The `@` operator (implicit intersection) forces a multi-cell result to return a single value relative to the formula's row. Excel 365 may automatically prepend `@` to legacy formulas. If a formula unexpectedly returns only one value instead of spilling, check for an unwanted `@`.
`confirmations: seed · category: arrays`

**ARR-006** · `SEQUENCE(rows, cols, start, step)` generates a sequence of numbers. It replaces helper columns of incrementing values: `=SEQUENCE(12, 1, 1, 1)` produces 1 through 12. Combine with DATE for date sequences: `=DATE(2024, SEQUENCE(12), 1)` generates the first of each month in 2024.
`confirmations: seed · category: arrays`

**ARR-007** · Spill range references use `#` after the cell containing the formula: if A1 contains `=UNIQUE(Data[Region])`, then `A1#` refers to the entire spilled result. Use this to chain dynamic array formulas: `=SORT(A1#)` sorts the unique values. The `#` reference auto-resizes.
`confirmations: seed · category: arrays`

**ARR-008** · When migrating legacy CSE (Ctrl+Shift+Enter) array formulas to Excel 365, remove the curly braces and let the formula spill naturally. `{=SUM(IF(A1:A10>5, B1:B10))}` becomes `=SUM(IF(A1:A10>5, B1:B10))` — same formula, no CSE needed. However, test the results, as spill behavior can differ from legacy array evaluation.
`confirmations: seed · category: arrays`

---

## Formatting (4 patterns)

**FMT-001** · `TEXT(value, format_code)` converts a value to text with a specific display format. Common format codes: `"#,##0"` for thousands separator, `"0.00%"` for percentage, `"$#,##0.00"` for currency, `"YYYY-MM-DD"` for ISO dates. The result is a text string — do not use it for intermediate calculations.
`confirmations: seed · category: formatting`

**FMT-002** · Custom number formats in Excel use `positive;negative;zero;text` sections. Example: `#,##0;(#,##0);"-";@` shows positive numbers normally, negatives in parentheses, zeros as a dash, and text as-is. Teach users this when they need display formatting that doesn't change the underlying value.
`confirmations: seed · category: formatting`

**FMT-003** · Conditional formatting formulas must return TRUE/FALSE. The formula is evaluated relative to the first cell in the applied range. Use mixed references: `=$B2>100` (locked column, relative row) to highlight entire rows where column B exceeds 100. Pure relative references shift unpredictably in conditional formatting.
`confirmations: seed · category: formatting`

**FMT-004** · When displaying percentages, decide whether the source value is a decimal (0.15) or a whole number (15). If the cell already contains 0.15, formatting as percentage gives 15%. If it contains 15, formatting as percentage gives 1500%. AI formulas frequently confuse this — always clarify the source data format and apply `value/100` if needed.
`confirmations: seed · category: formatting`

---

## Performance (4 patterns)

**PRF-001** · Volatile functions recalculate on EVERY change to the workbook, not just when their inputs change. The volatile functions are: `NOW()`, `TODAY()`, `RAND()`, `RANDBETWEEN()`, `INDIRECT()`, `OFFSET()`, and `INFO()`. Avoid them in formulas that are copied to thousands of cells. One volatile function triggers recalculation of the entire dependency chain.
`confirmations: seed · category: performance`

**PRF-002** · `SUMPRODUCT` over large ranges is significantly slower than `SUMIFS`. For simple conditional sums, always use SUMIFS. Reserve SUMPRODUCT for cases that genuinely need array multiplication (weighted averages, multi-condition counting with OR logic). On a 100K-row dataset, the difference is seconds vs milliseconds.
`confirmations: seed · category: performance`

**PRF-003** · Helper columns are often faster than complex array formulas. A formula like `=SUMPRODUCT((A:A="X")*(B:B="Y")*(C:C))` over 50,000 rows can be replaced with a helper column containing `=IF(AND(A2="X", B2="Y"), C2, 0)` and a simple SUM of the helper column. This trades disk space for calculation speed.
`confirmations: seed · category: performance`

**PRF-004** · Whole-column references (`A:A`) in array formulas force Excel to process over 1 million rows. Always bound your ranges to the actual data extent: `A2:A5000` or use structured table references which auto-bound. The difference between `SUMIFS(A:A, B:B, "X")` and `SUMIFS(A2:A5000, B2:B5000, "X")` is negligible for SUMIFS but massive for array formulas.
`confirmations: seed · category: performance`

---

## How To Contribute New Patterns

If you've corrected a formula issue in generated output and it seems like a pattern others would hit:

1. Run `bash scripts/sync.sh capture` in your terminal or check `learnings/local-corrections.jsonl`
2. Run `python scripts/contribute.py` to submit
3. Maintainers review and merge confirmed patterns

**What makes a good pattern:**
- Specific enough to be actionable (not "make the formula better")
- Universal enough to apply across different spreadsheets
- Corrects a real mistake, not a personal preference
- Includes the reasoning (why the correction matters for accuracy or reliability)

**What doesn't belong:**
- Brand-specific data structures
- Application-specific business rules
- Formatting preferences that are purely aesthetic
- VBA/macro patterns (separate concern from formulas)
