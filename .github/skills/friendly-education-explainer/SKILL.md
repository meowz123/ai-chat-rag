---
name: friendly-education-explainer
description: "Use when: simplifying educational documents, translating technical jargon to plain language, creating beginner-friendly explanations, rewriting lessons for non-experts, and improving readability for students or general audiences."
argument-hint: "Provide the source text or file path, target audience (age/level), and desired output format (summary, glossary, lesson notes, FAQ)."
user-invocable: true
disable-model-invocation: false
---

# Friendly Education Explainer

This skill converts technical educational content into clear, friendly, and easy-to-understand material for broader audiences.

## When To Use
- Your document includes heavy jargon, acronyms, or specialized terms.
- You need beginner-friendly notes from expert material.
- You want to keep meaning accurate while lowering complexity.

## Inputs
- Source content (text snippet or file)
- Audience level (default: internal staff with mixed background)
- Output type (default: Friendly Summary): summary, glossary, lesson notes, or Q&A
- Preferred language (default: English only)

## Default Profile
- Audience: internal staff with mixed background
- Output format: Friendly Summary
- Language: English only

If the user does not provide overrides, use this default profile automatically.

## Workflow

### Step 1: Audience & Goal Setup
1. Identify audience (student, parent, non-technical staff, beginner learner).
2. Set target reading level (default: simple, short-sentence style).
3. Confirm output type (summary, glossary, lesson notes, FAQ).

### Step 2: Extract Core Ideas
1. Pull out key concepts, process steps, and critical definitions.
2. Separate must-know points from nice-to-know details.
3. Keep original intent and factual meaning unchanged.

### Step 3: Jargon Detection & Rewrite
1. Detect domain terms, acronyms, and dense phrases.
2. Replace each term with plain wording.
3. If a technical term must remain, add a one-line friendly definition right away.

### Step 4: Structure for Learning
1. Use short sections with clear headings.
2. Use bullets and short sentences.
3. Add simple examples or analogies where useful.
4. End with a quick recap and 3 key takeaways.

### Step 5: Comprehension Check
1. Check for unexplained jargon.
2. Check sentence length and clarity.
3. Check if a first-time reader can answer: "What is this? Why it matters? What should I do next?"

## Decision Rules
- If source text is too advanced for target audience, split into: basics first, advanced notes later.
- If too many terms appear, create a mini glossary before full explanation.
- If meaning risks changing during simplification, keep the original term and add plain-language annotation.

## Output Formats
Use one of these based on request:

### 1) Friendly Summary
- What this topic is
- Why it matters
- How it works (simple steps)
- Key takeaways

### 2) Glossary-First
- Term -> plain definition -> tiny example

### 3) Lesson Notes
- Topic overview
- Core ideas
- Common mistakes
- Practice questions

### 4) FAQ
- Beginner questions with short, practical answers

## Quality Criteria (Completion Checks)
A response is complete only if:
1. Every key jargon term is simplified or explained.
2. No paragraph is overloaded with long, dense sentences.
3. Meaning is accurate to the source.
4. Audience level is explicitly respected.
5. Output ends with a concise recap.

## Guardrails
- Do not invent facts that are not in source material.
- Do not oversimplify to the point of inaccuracy.
- Do not remove required safety, legal, or compliance information.
