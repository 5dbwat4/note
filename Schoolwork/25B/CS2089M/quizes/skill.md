---
name: pdf-to-markdown-preserve-layout
description: Convert PDF handouts, quizzes, solutions, and course materials into Markdown while preserving bold, italic, mathematical formulas, underlines, tables, and embedded diagrams/images. Use when a PDF has mixed extractable text and visual objects such as E-R diagrams, relational algebra formulas, underlined primary keys, colored answers, or scanned/cropped figures that must survive conversion.
---

# PDF To Markdown Preserve Layout

## Workflow

1. Inspect the PDF before converting.
   - Use PyMuPDF (`fitz`) to check page count, metadata, extractable text, spans, fonts, flags, colors, and bounding boxes.
   - If command-line tools such as `pdftotext` fail due to sandbox or first-run setup, prefer PyMuPDF instead of requesting permission unless the tool is essential.

2. Determine which content is text and which content is visual.
   - Trust text extraction for ordinary paragraphs, headings, lists, and simple tables only after checking the rendered page.
   - Render pages to PNG when the extracted text omits formulas, diagrams, shapes, underlines, table borders, or other visual elements.
   - Treat E-R diagrams, charts, handwritten annotations, and complex layout regions as image assets unless recreating them is explicitly useful.

3. Preserve inline formatting from spans.
   - Convert bold fonts such as `BoldMT` to `**...**` or `<strong>...</strong>`.
   - Convert italic fonts such as `ItalicMT` to `*...*` or `<em>...</em>`.
   - Convert bold italic fonts to `***...***` or `<strong><em>...</em></strong>`.
   - Preserve colored answer text with HTML such as `<span style="color:red">...</span>` when Markdown alone cannot express it.

4. Preserve underlines explicitly.
   - PDF text extraction often exposes underlines as vector lines, not as font flags.
   - Inspect rendered crops for underlined primary keys or emphasized attributes.
   - Use `<u>...</u>` in Markdown for underlined terms, especially primary keys in relational schemas.
   - For composite primary keys, underline each key attribute: `order(<u>user_ID</u>, <u>plan_ID</u>, ...)`.

5. Convert formulas deliberately.
   - For relational algebra and mathematical notation, prefer block LaTeX with `$$ ... $$`.
   - Use standard symbols: `\Pi`, `\sigma`, `\rho`, `\times`, `\bowtie`, `\land`, `\left`, `\right`.
   - Escape underscores inside text-mode labels, for example `\text{pre\_course\_id}`.
   - Before finalizing, compare the LaTeX transcription against a high-resolution crop of the formula region.

6. Convert tables based on complexity.
   - Use Markdown tables for simple text tables.
   - Use HTML tables when preserving color, alignment, or other styling matters.
   - Do not silently normalize spelling from the source unless the user asks for corrections; preserve source typos when transcribing.

7. Save visual assets next to the Markdown.
   - Create an asset directory named after the output file, for example `Solution 3 of Database Systems.assets/`.
   - Crop only the relevant diagram or figure region, not the whole page, unless the whole page is needed.
   - Use relative Markdown links: `![E-R diagram](<Solution 3 of Database Systems.assets/er-diagram.png>)`.
   - Keep final assets descriptive; delete temporary render/check images after verification.

## Verification

1. Read the generated Markdown with UTF-8 explicitly on Windows.
   - `Get-Content` without `-Encoding UTF8` can display Chinese text as mojibake even when the file is valid.

2. Compare normalized text coverage.
   - Remove Markdown markers and collapse whitespace before comparing PDF text length with Markdown text length.
   - Expect differences where formulas or diagrams were intentionally represented as LaTeX/images.

3. Check style markers directly.
   - Confirm expected markers such as `**`, `*`, `<u>`, `<span style="color:red">`, `$$`, and image links exist.
   - Confirm image files referenced by Markdown exist on disk.

4. Visually inspect key rendered crops.
   - Formula crops catch transcription errors.
   - Diagram crops catch clipped edges.
   - Schema crops catch missing underlines.

## PyMuPDF Snippets

Inspect fonts and style spans:

```python
import fitz
from collections import Counter

doc = fitz.open("input.pdf")
fonts = Counter()

for page in doc:
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["text"].strip():
                    fonts[(span["font"], round(span["size"], 2), span["flags"])] += 1

for item, count in fonts.most_common():
    print(count, item)
```

Render a page or crop for visual inspection:

```python
import fitz

doc = fitz.open("input.pdf")
page = doc[1]
clip = fitz.Rect(82, 160, 530, 355)
pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip, alpha=False)
pix.save("assets/er-diagram.png")
```

## Output Conventions

- Name the Markdown after the PDF: `Solution 3 of Database Systems.pdf` -> `Solution 3 of Database Systems.md`.
- Name image folders after the Markdown stem: `Solution 3 of Database Systems.assets/`.
- Prefer faithful transcription over beautification.
- Mention any content that was represented as an image rather than transcribed.
- Mention if formulas were not detected or if no math objects/fonts appeared in the PDF.
