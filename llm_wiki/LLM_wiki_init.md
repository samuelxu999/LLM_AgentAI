# LLM Wiki Knowledge Base — Setup Instructions

Please help me build a personal knowledge base system from scratch, inspired by Karpathy's LLM Wiki approach.
Execute all of the following steps completely without skipping any details.

---

## Part 1 — Create Directory Structure

Create the following directories:

```
raw/articles/
raw/clippings/
raw/images/
raw/pdfs/
raw/notes/
raw/personal/
wiki/sources/
wiki/concepts/
wiki/entities/
wiki/synthesis/
wiki/templates/
outputs/
scripts/
```

---

## Part 2 — Create System Files

### wiki/index.md
- Frontmatter: `type: system-index`, `graph-excluded: true`
- Body: Sources list (reverse chronological), Concepts list, Entities list, Recent Synthesis list, Outputs list

### wiki/log.md
- Frontmatter: `type: system-log`, `graph-excluded: true`
- Purpose: append-only operation log, format: `YYYY-MM-DD | operation-type | description`

### wiki/overview.md
- Frontmatter: `type: system-overview`, `graph-excluded: true`
- Body: Knowledge Base Health Dashboard table (total sources, high-confidence concept count, open questions count, stale page count)

### wiki/QUESTIONS.md
- Frontmatter: `type: system-questions`, `graph-excluded: true`
- Body: Open Questions list (checkbox format), Resolved Questions list

---

## Part 3 — Create Page Templates

### wiki/templates/source-template.md
Frontmatter fields: `type`, `title`, `date`, `source_url`, `domain`, `author`, `tags`, `processed`, `raw_file`, `raw_sha256`, `last_verified`, `possibly_outdated`, `language`, `canonical_source`

Body structure:
- `## Summary`
- `## Key Points`
- `## Concepts Extracted`
- `## Entities Extracted`
- `## Contradictions` (disagreements with other sources)
- `## My Notes`

### wiki/templates/personal-writing-template.md
Frontmatter fields: `type: personal-writing`, `title`, `date`, `status` (draft/published/deprecated), `topic_tags`, `confidence_at_writing` (low/medium/high), `superseded_by`, `raw_file`, `raw_sha256`, `last_verified`, `tags`, `processed`

Body structure:
- `## Core Argument`
- `## Key Claims`
- `## Evidence Referenced`
- `## Limitations`

### wiki/templates/concept-template.md
Frontmatter fields: `type: concept`, `title` (English primary name), `date`, `updated`, `tags`, `source_count`, `confidence` (low/medium/high), `domain_volatility` (low/medium/high), `last_reviewed`, `aliases` (array storing all Chinese and English names)

Body structure:
- `## Definition` (first line uses format: "English Name (Chinese Name)")
- `## Key Points`
- `## My Position`
- `## Contradictions`
- `## Sources` (wikilinks list only)
- `## Evolution Log` (append one entry per update)

### wiki/templates/entity-template.md
Frontmatter fields: `type: entity`, `title`, `date`, `tags`, `entity_type` (person/tool/institution/paper), `aliases`

Body structure:
- `## Description`
- `## Key Contributions`
- `## Related Concepts`
- `## Sources`

### wiki/templates/synthesis-template.md
Frontmatter fields: `type: synthesis`, `title`, `date`, `tags`, `source_count`, `confidence`

Body structure:
- `## Thesis`
- `## Evidence`
- `## Counter-evidence` (Stage 0 reverse-validation results)
- `## Synthesis`
- `## Confidence Notes`
- `## Limitations`
- `## Sources`

---

## Part 4 — Create scripts/lint.py

`lint.py` performs the following 9 checks and writes the report to `wiki/outputs/lint-YYYY-MM-DD.md` (frontmatter includes `graph-excluded: true`):

1. **YAML frontmatter validity**: Check that all `.md` files under `wiki/` have valid YAML frontmatter containing `type` and `date`
2. **Broken wikilinks**: `[[xxx]]` references that point to non-existent pages
3. **Index consistency**: Verify that all files listed in `wiki/index.md` actually exist on disk
4. **Stub pages**: Pages whose body is fewer than 100 characters
5. **Near-duplicate concept names**: Pairs of concept page slugs with Jaccard similarity > 0.7
6. **SHA-256 integrity**: Compare raw file hashes against the `raw_sha256` field in source pages (flag as `⚠ SOURCE MODIFIED`)
7. **Stale pages**: Pages exceeding the `domain_volatility` staleness threshold (high = 90 days, medium = 180 days, low = 365 days)
8. **Cross-language duplicates**: Source URL similarity detection + detection of overlapping `aliases` fields across different concept pages
9. **Wikilink format**: Detect wikilinks not in lowercase-hyphenated English format (e.g., Chinese-character links like `[[价值投资]]`) and broken alias links

---

## Part 5 — Create CLAUDE.md (Behavior Contract)

`CLAUDE.md` is the core behavioral specification for the LLM. It must include all of the following sections:

### System Overview
- Three-layer architecture description (Raw / Wiki / Outputs)
- Core permission principle: The LLM has full read/write permission over the `wiki/` directory. The `raw/` directory is owned by the human; the LLM may only read it — never create, modify, or delete anything inside `raw/`.

---

### INGEST Operation

**Trigger words**: `ingest`, `process this`

**Source type determination** (priority order, highest first):
1. Frontmatter contains `type: personal-writing` → use **Personal Writing** flow
2. File path contains `raw/personal/` → use **Personal Writing** flow
3. Frontmatter contains `type: pdf-reference` → use **PDF Reference** flow (same as external source, with PDF-specific handling)
4. Otherwise → use **External Source** standard flow

**When frontmatter is missing**:
- Extract `title` from the first `#` heading; if no heading, infer from filename
- Leave `source_url` blank; note "source unknown" in `wiki/sources/<slug>.md`
- Use file system modification time as `date`
- Do not interrupt INGEST, but log a warning in `log.md`: "Warning: source file missing standard frontmatter"

**External Source Standard Flow (11 steps)**:

1. Read the target raw source (file under `raw/`, read-only)
2. Compute the SHA-256 hash of the raw file (Python `hashlib`)
3. Confirm key points with the user (process one source at a time, maintain engagement)
4. Generate a slug (lowercase English with hyphens, e.g., `attention-is-all-you-need`)
5. Create `wiki/sources/<slug>.md` (using `source-template.md`), with frontmatter fields:
   - `raw_file`: relative path (e.g., `raw/articles/filename.md`)
   - `raw_sha256`: SHA-256 hash
   - `last_verified`: ingestion date (YYYY-MM-DD)
   - If source was published more than 2 years ago: set `possibly_outdated: true` and add a notice at the end of the Summary section
6. **Concept name alignment check** (must be executed before extracting concepts):
   - Map each candidate concept name to an English lowercase-hyphenated slug (e.g., "First Principles Thinking" → `first-principles-thinking`)
   - Check whether that slug already exists in `wiki/concepts/`
   - **Also check all existing concept pages' `aliases` fields**: scan `wiki/concepts/*.md`, parse each page's frontmatter `aliases` list, and check for matches (supports both Chinese and English alias matching)
   - If a match is found via slug **or** aliases: update the existing page — do not create a new one
   - If no match is found: create a new page, and populate the frontmatter `aliases` field with both the Chinese and English names
7. For each extracted concept:
   - If `wiki/concepts/<concept>.md` already exists: update it — append the new source reference, append to the Evolution Log, update `source_count` and `confidence`, and **update the `last_reviewed` field**
   - If it does not exist: create a new file (using `concept-template.md`), and **populate the `aliases` field with both Chinese and English names**
   - **Evolution Log append rules**:
     - If this source agrees with the current Definition: write "Reinforced"
     - If this source corrects it: write "Corrected: [specific change]"
     - If this source contradicts existing content: write "New disagreement: [content], see Contradictions section"
     - Format: `- YYYY-MM-DD (N sources): [one-sentence description of the epistemic change]`
8. For each extracted entity: same logic as step 7
9. Update `wiki/index.md`: move the source from Unprocessed to Processed; add any new concepts/entities
10. Read `wiki/QUESTIONS.md` and check whether this source answers any open questions:
    - If yes: prompt the user — "This source may answer the open question: [description]. Run QUERY now?"
    - If the user confirms: execute QUERY, write results to `wiki/synthesis/`, and move the question to Resolved in `QUESTIONS.md`
11. Append to `wiki/log.md`: `YYYY-MM-DD HH:MM | ingest | [source title]`

**Personal Writing Flow** (differs from external source flow):
- Do not generate a Summary section; skip objective summarization
- Write the core argument into the `## My Position` section of the relevant concept page (labeled "personal perspective")
- Do not count toward `source_count` for `confidence` (to avoid self-citation inflation)
- If the article cites external sources, extract those citations and link them to existing `wiki/sources/` pages via wikilinks where possible
- SHA-256 hash mechanism still applies
- Evolution Log entry format: `YYYY-MM-DD personal-writing [[sources/slug]] established a clear position on this concept`

---

### QUERY Operation

**Trigger words**: a direct question, or "based on my knowledge base"

**Steps**:
- **Step Q1**: Run `qmd query "<user question>" --json` to retrieve the top 5 relevant pages. If `qmd` errors, fall back: read `wiki/index.md` and manually select the most relevant files.
- **Step Q2**: Read each of the top 5 files in full (do not skip any section)
- **Step Q3**: Synthesize an answer:
  - Every core conclusion must be traced back to a specific `wiki/sources/<slug>.md` (citing only concept pages is not allowed)
  - Note the `confidence` level of each source
  - When sources contradict each other, explicitly flag the disagreement: "⚠ Disagreement: [[sources/a]] argues… but [[sources/b]] argues…"
- **Step Q4**: If the answer has reuse value, write it to `wiki/outputs/YYYY-MM-DD-<topic>.md`:
  - Frontmatter must include `graph-excluded: true`
  - Include a "⚠ Confidence Notes" section at the end
  - Update the `Recent Synthesis` list in `wiki/index.md`
  - Append to `wiki/log.md`: `YYYY-MM-DD HH:MM | query | [question summary]`

**Output format by question type**:

| Question type | Output format |
|---|---|
| General question | Markdown prose |
| Comparison | Markdown table |
| Presentation | Marp slides (add `marp: true` to frontmatter) |
| Trend | Python matplotlib code block |
| Checklist | Structured bullet list |

---

### LINT Operation

**Trigger words**: `lint`, `check`, `health check`

**Steps**:
1. Run `scripts/lint.py` (9 checks)
2. Write the report to `wiki/outputs/lint-YYYY-MM-DD.md` (frontmatter includes `graph-excluded: true`)
3. Run `qmd status`; compare the index file count against the actual `.md` file count in `wiki/` (excluding system files). If the index is behind, run `qmd add wiki/` and record this in the report.
4. Show the user a summary and ask whether to fix the issues

---

### REFLECT Operation

**Trigger words**: `reflect`, `synthesize`, `find patterns`

**Four-stage execution**:

- **Stage 0 (Reverse validation)**: Before generating any synthesis conclusions, actively search for counter-evidence. If no opposing sources are found, note in the Limitations section: "⚠ Echo chamber risk: no counter-sources found; conclusions may suffer from confirmation bias"
- **Stage 1 (Pattern scan)**: Use `qmd` to batch-scan:
  ```
  qmd multi-get "wiki/concepts/*.md" -l 40
  qmd multi-get "wiki/entities/*.md" -l 40
  qmd multi-get "wiki/synthesis/*.md" -l 60
  ```
  Identify: cross-source patterns, implicit connections, content gaps, contradiction pairs
- **Stage 2 (Deep synthesis)**: For candidates with evidence, read the relevant pages in full and write to `wiki/synthesis/<topic>-synthesis.md` (using `synthesis-template.md`)
- **Stage 3 (Gap analysis)**: Identify and output the following gap types:
  - Isolated concepts with `source_count = 1` created more than 30 days ago
  - Concepts/entities mentioned in multiple places but without their own pages (implicit blind spots)
  - Topic areas with obviously thin coverage
  - Output to `wiki/outputs/gap-report-YYYY-MM-DD.md` (frontmatter includes `graph-excluded: true`)

**After completion**: update `wiki/overview.md` Health Dashboard, update `wiki/index.md`, append `wiki/log.md`: `YYYY-MM-DD HH:MM | reflect | [summary of main findings]`

---

### MERGE Operation

**Trigger words**: `merge`, `deduplicate`

**Same-language merge flow**:
1. Confirm the merge plan with the user (never auto-merge)
2. Keep the primary slug; update all wikilinks pointing to the merged page
3. Replace the merged file with a redirect file (content: `redirect: [[concepts/primary-slug]]`)
4. Log in `log.md`: `YYYY-MM-DD | merge | [old-slug] → [primary-slug]`

**Cross-language merge flow** (distinct from same-language merge):
1. Keep the English slug as the primary
2. Merge the `aliases` fields as a union of both pages
3. Merge `Key Points`, `Sources`, and `Evolution Log` as union (with deduplication)
4. If both pages have `My Position` content, show the user a comparison before merging
5. Keep the old slug file as a redirect (to prevent broken wikilinks)
6. Log in `log.md`: `YYYY-MM-DD | merge | [old-slug] → [primary-slug] (cross-language merge)`

---

### ADD-QUESTION Operation

**Trigger words**: "I want to understand", `add question`, "record a question"

**Steps**:
1. Normalize the question (extract the core inquiry, remove filler words)
2. Append to `wiki/QUESTIONS.md` (checkbox format): `- [ ] Question content (opened YYYY-MM-DD)`
3. Append to `wiki/log.md`

---

### Wikilink Rules

**Non-negotiable format rule**: All wikilink targets must use lowercase hyphenated English slugs.

```
✅ [[value-investing]]
✅ [[attention-mechanism]]
✅ [[warren-buffett]]
❌ [[价值投资]]      (Chinese characters)
❌ [[ValueInvesting]] (camelCase)
❌ [[value_investing]] (underscores)
```

**Correct handling of Chinese names**:
- Add to the `aliases` field in the concept page frontmatter
- Use parenthetical notation on the first line of the concept page body: "价值投资（Value Investing）"
- Always use the English slug in wikilinks

**Where wikilinks are allowed**:
- Concept pages referencing other concept/entity pages
- Source pages referencing concept/entity pages
- Synthesis pages referencing concept/source/entity pages

**Where wikilinks are forbidden**:

| Forbidden scenario | Reason |
|---|---|
| Referencing system files | No `[[log]]`, `[[index]]`, `[[overview]]`, `[[QUESTIONS]]` |
| Referencing lint reports | No `[[outputs/lint-xxx]]` |
| Operation names as links | No `[[ingest]]`, `[[query]]`, `[[reflect]]` |
| Inside log.md | Use plain text paths (e.g., `wiki/sources/xxx.md`), not wikilinks |

---

### Wiki Language Rules

| Rule | Detail |
|---|---|
| Wiki writing language | concept/entity/synthesis pages are written in **English** |
| concept page `title` field | Use the English primary name (shown as the graph node label) |
| English terms | On first appearance in a concept page, use parenthetical notation: "注意力机制（Attention Mechanism）" |
| Slug (filename) convention | Always use lowercase hyphenated English; never use Chinese filenames |
| `aliases` field | Cover all Chinese and English names for the concept |

---

### Confidence Update Rules

| Source count | Confidence | Action |
|---|---|---|
| 1 source | low | Set automatically |
| 3+ sources | medium | Set automatically |
| 5+ sources with no major contradictions | high candidate | Show the user the current Definition and Sources list; **wait for confirmation** |
| User explicitly replies "confirmed" or "ok" | high | Only then may it be set |

> Note: Personal writing (`raw/personal/`) does not count toward `source_count`.

---

### Source Integrity Rules

- **Re-ingest rule**: If lint reports `⚠ SOURCE MODIFIED`, re-ingest the file and update all affected concept/entity pages. Evolution Log entry: `YYYY-MM-DD source updated: wiki/sources/slug.md hash changed, content re-extracted`
- Sources published more than 2 years ago: mark `possibly_outdated: true`
- Contradicting sources must be explicitly recorded in the `Contradictions` section of both the source page and affected concept pages — silent overwriting is not allowed

---

### System File Isolation Rules

The following files **must** have `graph-excluded: true` in their frontmatter and must not appear in the Obsidian graph:
- `wiki/log.md`
- `wiki/index.md`
- `wiki/overview.md`
- `wiki/QUESTIONS.md`
- All files under `wiki/outputs/`

---

### Documentation Maintenance Rule

When `CLAUDE.md` rules are updated, synchronize the corresponding sections in `USER_GUIDE.md` to keep both documents consistent.

---

## Part 6 — Initialize qmd Index

Run:
```
qmd collection add wiki/
qmd status
```

---

## Part 8 — Post-Setup Verification

Output the following verification report:
1. Directory structure tree (`tree -L 3` or `find`)
2. List of chapters included in `CLAUDE.md`
3. List of template files under `wiki/templates/`
4. `qmd status` output (number of indexed files)
5. List of checks included in `scripts/lint.py`
