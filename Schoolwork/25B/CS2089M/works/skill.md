---
name: markdown-to-latex-pdf
description: Convert Markdown or MDX documents into standalone LaTeX and compiled PDF, especially Chinese course reports, lab reports, and notes that need UTF-8, code blocks, formulas, images, and reliable XeLaTeX compilation. Use when asked to turn .md/.mdx files into .tex, compile PDFs, diagnose Pandoc/XeLaTeX issues, or preserve Chinese text correctly on Windows.
---

# Markdown To LaTeX PDF

## Workflow

1. Inspect the source file and surrounding directory first.
   - Confirm the input path, output directory, file size, and last modified time.
   - Read Markdown with UTF-8 explicitly on Windows:

     ```powershell
     Get-Content -LiteralPath "input.md" -Encoding UTF8 -TotalCount 80
     ```

   - Use `rg` to identify headings, fenced code blocks, formulas, and image references:

     ```powershell
     rg -n "!\[|!\[\[|\\includegraphics|\.png|\.jpg|\.jpeg|\.pdf|\.svg|\$\$|```|^#" "input.md"
     ```

2. Verify tool availability without assuming first-run setup is clean.
   - Check paths with `Get-Command pandoc`, `Get-Command xelatex`, and optionally `Get-Command pdflatex`.
   - If version commands hang briefly, rerun with a longer timeout before concluding the tool is unavailable.
   - Prefer XeLaTeX for Chinese documents; do not use pdfLaTeX for CJK text unless a project template explicitly requires it.

3. Generate a standalone `.tex` file with Pandoc.
   - Use `ctexart` for Chinese reports and notes.
   - Set the working directory to the source directory so relative images resolve naturally.
   - Keep the `.tex` next to the source unless the user requested another location.

   ```powershell
   pandoc "input.md" `
     --from markdown `
     --to latex `
     --standalone `
     --pdf-engine=xelatex `
     -V documentclass=ctexart `
     -V geometry:margin=2.5cm `
     -V colorlinks=true `
     -V linkcolor=blue `
     -V urlcolor=blue `
     -o "input.tex"
   ```

4. Compile the generated `.tex` with XeLaTeX from the output directory.
   - Run at least once with nonstop mode and halt on hard errors:

     ```powershell
     xelatex -interaction=nonstopmode -halt-on-error "input.tex"
     ```

   - Run XeLaTeX a second time when logs mention labels, references, bookmarks, or page labels.
   - Keep `.aux` and `.log` unless the user asks for cleanup; they are useful for diagnosing compilation.

5. Validate the result.
   - Confirm both `.tex` and `.pdf` exist and report their paths, sizes, and timestamps.
   - Mention page count if XeLaTeX reports it in `Output written on ... (N pages)`.
   - Treat font fallback, underfull boxes, and small overfull boxes as warnings unless they visibly damage the document or the user requested perfect typography.

## Chinese And Windows Notes

- `Get-Content` without `-Encoding UTF8` can display valid Chinese Markdown as mojibake in PowerShell; verify encoding before editing or diagnosing the source.
- Pandoc plus `-V documentclass=ctexart` lets CTEX select Windows CJK fonts such as SimSun/FangSong automatically under XeLaTeX.
- `fc-list` may fail on a fresh MiKTeX setup because it tries to initialize user config under `%APPDATA%`; this is not necessarily a blocker if XeLaTeX with CTEX compiles successfully.
- If CTEX cannot find fonts, check `C:\Windows\Fonts` for common Chinese fonts such as `simsun.ttc`, `msyh.ttc`, `msyhbd.ttc`, or `msyhl.ttc`.

## Troubleshooting

- **Missing images**: inspect Markdown image paths, run Pandoc from the Markdown directory, and prefer relative paths.
- **Chinese glyph errors**: switch to `xelatex` and `ctexart`; avoid `pdflatex`.
- **Long code lines overflow**: accept minor warnings for code-heavy reports, or add line-breaking/listing configuration only when the PDF is visibly unusable.
- **Pandoc direct PDF fails**: generate `.tex` first, then compile with XeLaTeX so the `.log` points to the exact LaTeX problem.
- **First compile succeeds but warns about labels**: run XeLaTeX again.

## Output Convention

- Preserve the source stem:
  - `lab-minisql.md` -> `lab-minisql.tex`
  - `lab-minisql.tex` -> `lab-minisql.pdf`
- Put outputs beside the source file unless requested otherwise.
- In the final response, report the generated `.tex` and `.pdf` paths and any meaningful warnings, but do not paste the full TeX log.
