https://github.com/V1CeVersaa/Paper-List/blob/main/AGENTS.md

===========


# Paper Note Agent Guide

This project is used to archive notes and records from past paper readings. When the user asks the agent to organize notes, they will typically provide two inputs:

- The paper to read, including its title and the corresponding PDF file
- The target Markdown file to write into or update

The purpose of these notes is twofold: (1) to allow a reader who has not read the original paper to gain a reasonable understanding of the method, and (2) to serve as a quick refresher when the reader has read the paper before but has since forgotten the details. Therefore, the note should be self-contained, clear, and well-organized, with a focus on the core contributions and key technical details of the paper. The note should not be a direct translation or a collection of section summaries; rather, it should be a polished, standalone document that can be easily reviewed and retrieved in the future.

The agent's job is not to produce a paragraph-by-paragraph translation, nor to write only a vague summary. It should produce a high-quality Chinese note based on the paper, one that is reusable, easy to review later, and convenient for long-term retrieval.

## 1. Inputs and Workflow

For each task, follow this default workflow:

1. First confirm the paper PDF provided by the user and the target Markdown file.
2. Read the paper in full at least once to build an overall picture of its argument before beginning to write. Do not start drafting the note while still in the middle of a first reading pass.
3. When reading the paper, prioritize the full main thread: background, core assumptions, formal problem definition, method, experimental support, limitations, and future directions.
4. If the target Markdown file already exists, understand its current content first. Unless the user explicitly asks to preserve a partial draft, the goal should be to reorganize it into a complete and stylistically consistent note rather than mechanically appending text.
5. Write only from the paper itself and materials provided by the user. Do not introduce external papers, web information, or unverified background on your own. When the paper references standard concepts (e.g., KL divergence, MDP, policy gradient), the agent may provide brief inline clarifications, but must not introduce claims or results from external sources.
6. If the paper has an appendix or supplementary material, treat it as a secondary source: check it for important proofs, ablations, or clarifications that strengthen the main text, but do not let appendix content dominate the note.
7. For less important details in the paper, it is acceptable to omit them, mention them only briefly, or downgrade them using `>` quote formatting. Do not let secondary material bury the main line.
8. The final output should be "faithful to the paper, but better than a translation": preserve the original meaning while adding the necessary logical connections, term explanations, and contextual clarification so that the note is clearer and easier to revisit than a direct translation.

## 2. General Writing Principles

- Use Chinese as the primary language of the note. Key technical terms may retain their English form when first introduced.
- When introducing a Chinese-English term pair, use the format `中文术语/English Full Term/Abbreviation`, where the abbreviation is optional. For example: `模仿学习/Imitation Learning/IL`, `强化学习/Reinforcement Learning/RL`, `马尔可夫决策过程/Markov Decision Process/MDP`. The `/` delimiter is reserved for this term-pairing purpose. Chinese full-width parentheses `（）` serve a different role: they are used for inline supplementary explanations or clarifications of the preceding text, not for term pairing.
- The writing must remain faithful to the paper, but it must not stop at sentence-level restatement. The agent should actively reorganize the author's argument structure and add necessary explanation.
- It is acceptable to explain things slightly more clearly or in slightly greater detail than the original, but do not infer conclusions the paper itself does not support.
- Avoid cliched metaphors, empty rhetoric, and exaggerated or overly colloquial evaluation.
- Do not write in the style of a "running translation" or a "pile of section summaries." The note should be a reorganized, standalone finished product.
- Be precise about core contributions, key assumptions, important formulas, and major experimental findings.
- Maintain notational consistency throughout the note. If the paper itself is inconsistent in notation across sections, choose the clearest convention and apply it uniformly.
- Whenever it is unclear whether something is explicitly stated by the authors, distinguish it carefully:
  - If the paper clearly states it, present it directly.
  - If it is the agent's interpretation, synthesis, or inference, use more careful phrasing such as "this can be understood as," "this design suggests that," or "the experimental results indicate that."

## 3. Rules for Information Selection

The priority order is as follows:

- Must retain: the problem being solved, why it matters, the core insight, the problem setup, key assumptions, the main method, the training or inference mechanism, the most important experimental conclusions, and the main limitations.
- Should retain: important formulas needed to support the main line, relationships between modules, the conclusions and meaning of key theorems, and the experiments or ablations that most directly validate the method.
- May selectively retain: implementation details, hyperparameters, secondary experiments, and peripheral derivations from supplementary material.
- May omit or downgrade with `>` quote formatting: repetitive statements, descriptions of minor baselines, long proof details that are not necessary for understanding the main idea, and engineering details with little effect on the final conclusions.

When omitting material, follow one rule: the reader must still be able to grasp both the core idea of the paper and the basis for judging its credibility.

**Special rule for theory-heavy papers:** When a paper is primarily theoretical in nature or contains theorems and derivations that are central to its contribution, the note must preserve the derivation process and important intermediate steps in substantial detail, rather than glossing over them with a brief summary. Specifically:

- Key derivations (e.g., how an objective is derived, how a bound is obtained, how one formulation reduces to another) should be presented step by step, with each non-trivial transition explained.
- Important theorems, lemmas, and propositions should include not only the statement but also a sketch or full reproduction of the proof when the proof technique itself is part of the paper's contribution or is necessary for understanding the result.
- Do not compress a multi-step derivation into a single sentence like "through standard variational arguments, we obtain..." — instead, show the intermediate steps so the reader can follow the logic without consulting the original paper.
- Use collapsible callout blocks (`> [!todo]- Derivation` or `> [!todo]- Proof`) to house longer derivations when they are important but would otherwise interrupt the narrative flow. This way the detail is preserved and accessible without cluttering the main reading path.

## 4. Fixed Output Structure

Use the following structure by default, unless the paper type makes it clearly unsuitable:

```md
---
title: <short title or main paper identifier>
headline: <full paper title>
---

> [!abstract] Contributions
>
> Paragraph 1: Summarize in a highly compressed but information-dense way what problem the paper solves, what core method it proposes, what the key technical move is, and what the results show.
>
> Paragraph 2: Briefly state the method's boundary conditions, key assumptions, possible weaknesses, or the main caveat that should be kept in mind when reading the paper.

## 1. Introduction

## 2. Problem Setup

## 3. Algorithm / Methods / Model

## 4. Experiments

## 5. Related Work & Future Work
```

Notes:

- `title` should use a short title, common abbreviation, or main paper identifier.
- `headline` should use the full paper title.
- The `Contributions` block must appear before `Introduction` and should use callout formatting.
- The main body should in principle keep the five-part structure. The title of Section 3 may be adjusted to `Algorithm`, `Methods`, `Model`, and so on, depending on the paper, but its role should remain the same.
- All Markdown headings (lines starting with `#`) must be written in English.

## 5. Section-by-Section Writing Rules

### 5.1 Contributions

This is the most important compressed view of the entire note. It should satisfy the following:

- Do not merely say "the paper proposes X"; also explain why it matters.
- The summary must reflect the paper's central technical move, not just a broad and empty conclusion.
- When appropriate, also mention result-level support such as identifiability, empirical improvements, or expansion of the applicable setting.
- The second paragraph should ideally include the single most important reservation: a strong assumption, scope limitation, modeling restriction, or lack of experimental coverage.

### 5.2 Introduction

This section should present the paper's underlying narrative, not simply rewrite the abstract. It must cover:

- What fundamental problem the paper is trying to solve
- Where the real gap in existing methods lies
- What the authors' most profound motivation and key insight are
- Where the idea comes from and why the modeling choice is reasonable

Writing requirements:

- The focus is on explaining why the paper makes sense and why it is worth doing.
- Do not sink into formulas or implementation details too early.
- If the original paper has a strong background narrative or motivating counterexample, preserve it here.

### 5.3 Problem Setup

This section must be serious, formal, and clear, but not excessively verbose. It should answer, as far as possible:

- What the input is and what the output is
- What information is accessible and what is not
- What the data, state, action, objective, constraints, and assumptions are
- What the symbols in the paper mean and how they relate to one another

Writing requirements:

- Try to write the problem definition as a coherent mathematical object rather than as a loose natural-language description.
- Formulas may be introduced when needed, but every formula must come with an explanation of its variables.
- Do not mix method details into the problem setup prematurely, unless the method itself is part of the setup.

### 5.4 Algorithm / Methods / Model

This section should remain as faithful to the paper as possible, but still be reorganized. The recommended order is:

1. Start with one or two paragraphs of method overview, explaining what the method is trying to do and what its core mechanism is.
2. Then introduce each key component in a modular way.
3. After that, explain the training objective, optimization procedure, inference process, or algorithmic pipeline.
4. Finally, summarize the theoretical properties, key assumptions, and why the method is considered reasonable by the authors.

Specific requirements for this section:

- Explain the backbone before the details; do not begin with a wall of formulas.
- If the method has multiple modules, introduce them according to logical dependency rather than mechanically following the paper's subsection order.
- For every key formula, explain what role it plays in the method, not just the literal expression.
- If the paper uses a probabilistic model, latent variables, an energy function, an optimization target, regularization terms, and so on, make each role explicit.
- If the paper has separate training and testing stages, distinguish them clearly.
- If the paper contains a theorem, proposition, or guarantee, summarize its conclusion, conditions, and practical meaning. Unless the proof itself is central, it usually does not need to be reproduced in full.
- If some part is merely an implementation aid, engineering trick, or otherwise not a bottleneck for understanding the core method, it may be weakened in presentation.

Additional conventions for this section:

- When presenting a theorem, proposition, or key definition, use an Obsidian callout block (e.g., `> [!note] Theorem 1`) to visually distinguish it from the surrounding narrative. For accompanying proofs that are worth preserving but not essential to the narrative flow, use a collapsible callout (e.g., `> [!todo]- Proof`) so readers can expand them on demand without disrupting the reading flow.
- If the paper provides algorithm pseudocode, reproduce it only when it genuinely aids understanding of the method's non-obvious control flow. For straightforward training loops, a natural-language description is preferred. For non-trivial algorithmic pipelines with multiple stages or branching logic, a concise pseudocode block or step-by-step enumeration is appropriate.
- Beyond presenting the formal content, provide intuitive interpretation of key design choices. For example, explain what each term in a loss function encourages or penalizes, what each dimension of a learned representation captures, or why a particular architectural choice is reasonable for the problem at hand. These interpretations should be clearly marked as such when they go beyond what the paper states directly.

### 5.5 Experiments

The experiments section should be concise, but it must not degrade into a list of datasets and numbers. It must answer:

- What claims the paper is trying to validate through the experiments
- What core tasks, datasets, baselines, and metrics are used
- What the most important results actually show
- Which results genuinely support the method design, such as ablations, robustness analysis, generalization, efficiency, or validation of theoretical predictions

In addition, the agent must include grounded critical organization and point out possible weaknesses in the experiments, for example:

- Whether the baselines are sufficient and fairly compared
- Whether the datasets or tasks are too narrow
- Whether the metrics truly correspond to the claimed capability
- Whether there is a missing ablation, error analysis, efficiency analysis, or failure case
- Whether there is a gap between the theoretical claim and the empirical validation

Critical content must be restrained, specific, and grounded in the paper itself. Do not make vague objections just for the sake of sounding critical.

### 5.6 Related Work & Future Work

The first priority of this section is clarity of organization.

- `Related Work` should explain which methods are closest to the paper and what the actual differences are.
- `Future Work` should distinguish future directions explicitly mentioned by the authors from possible extensions naturally inferred by the agent from the paper's limitations.
- If the authors' future work suggestions are preserved in a near-original form, concise organization or `>` quote formatting is appropriate.

If the paper does not have a dedicated related work or future work section, the agent should still synthesize one here, but must not fabricate content.

## 6. Style and Formatting Details

- Default to coherent paragraph-based writing. Use lists only when enumerating comparisons, module composition, or experimental setup genuinely makes the content clearer.
- Define mathematical symbols the first time they appear.
- For important equations that are referenced later in the note, use `\tag{N}` to assign equation numbers for cross-referencing. Equations that appear only once and are not referenced elsewhere do not need tags.
- When writing display (block) math equations, always place `$$` on its own separate line, both before and after the equation content. Do not put `$$` on the same line as the formula.
- Use the following Obsidian callout types consistently:
  - `> [!abstract] Contributions` — only for the contribution summary at the top of the note.
  - `> [!note]` — for theorems, propositions, definitions, and key remarks.
  - `> [!tip]` — for helpful intuitions or interpretive asides.
  - `> [!todo]-` — for collapsible detailed content such as proofs, long derivations, or extended calculations (the `-` suffix makes the block collapsed by default).
  - `> [!info]` — for supplementary context or technical side-notes.
- When key figures or diagrams from the paper are essential for understanding, insert a Markdown image reference at the appropriate location (e.g., `![](./assets/<Name>-<N>.webp)`) if the image file is available.  If the figure file is not yet available, leave a clear placeholder comment (e.g., `<!-- TODO: insert Figure X from paper -->`) with a brief description of what the figure shows, so the user can add it later. Image width can be controlled with the `![|600]` syntax when appropriate.
- For secondary material, marginal notes, implementation details, or direct excerpts from the paper, prefer `>` quote formatting to lower their visual weight.
- Do not copy large chunks of the original text just for the sake of completeness.
- Avoid mechanical narration such as "the authors first..., then..., next..." unless you are explicitly describing an algorithmic procedure.
- Ensure smooth narrative transitions between sections. Each section should begin with a brief orientation that connects it to the preceding content, rather than starting abruptly with definitions or formulas.
- When referencing other works, cite the paper title rather than using author-year formats like `Nguyen et al., 2023`. For example, write "as proposed in *Proximal Policy Optimization*" instead of "as proposed in Schulman et al. (2017)".
- Do not include personal reflections unrelated to the paper itself.

## 7. File Update Rules

- If the target file is empty, generate the complete note directly according to this specification.
- If the target file already contains content but is structurally messy, replace or rewrite it into an organized full version rather than appending unordered fragments.
- If the target file already contains relatively mature content, keep the existing style consistent when adding new material, and avoid duplicated paragraphs or repeated definitions.
- Unless the user explicitly requests it, do not modify other files just because you are adding or polishing notes.

## 8. Pre-Completion Checklist

Before finishing, check at least the following:

- Has the note gone beyond direct translation and become capable of independently explaining the paper's main line?
- Does `Contributions` truly summarize the paper's core contribution and boundary conditions?
- Does `Introduction` clearly explain the motivation, gap, insight, and origin of the idea?
- Is `Problem Setup` sufficiently formal, clear, and not overly verbose?
- Does `Algorithm / Methods / Model` present the backbone before the details, and are the formulas explained?
- Does `Experiments` both summarize the results and point out concrete, restrained weaknesses?
- Is `Related Work & Future Work` clearly organized, with the paper's own claims distinguished from the agent's synthesis?
- Have unimportant details been removed so that secondary content does not overwhelm the main line?
- Has the note avoided cliched metaphors, empty evaluation, unsupported inference, and overinterpretation?
- Is notation used consistently throughout the note, with every symbol defined on first use?
- Are key figures accounted for — either included as images or described with placeholders?
- Do sections flow into one another with adequate transitions, rather than reading as disconnected blocks?

If the answer to any of the above is no, continue revising rather than stopping.
