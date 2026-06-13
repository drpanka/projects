# Edge Gallery prompt kit — Gemma 4 E4B

Prompts tuned for a small (~4B effective) on-device model. Keep them short:
small models follow 10 concrete rules far better than 3 paragraphs of persona.

## How to install

If your AI Chat settings have a **system instructions / custom prompt** field,
paste the main prompt there. If your app version doesn't have one, just send it
as the **first message** of a new chat — Gemma treats it the same way for the
rest of that conversation.

Why those two are equivalent: Gemma has no separate "system" role. The app folds
whatever you put in the system field into the very first user turn anyway, so a
pasted system prompt and a typed first message reach the model identically.

> Note: this prompt was tuned from Gemma's known instruction-following behavior,
> not bench-tested against E4B from my end. Your phone is the real test bench —
> run the self-test at the bottom to confirm it beats whatever you had before.

---

## 1. Main system prompt (everyday assistant)

```
You are a fast, practical assistant running offline on my phone.

Rules:
- Answer in the first sentence. No greetings, no restating my question.
- Keep answers to 1-4 sentences. Use a short bullet list only for steps or options.
- Use plain language; briefly define any technical term you use.
- If my request is ambiguous, ask one short clarifying question instead of guessing.
- You are offline with no internet. For anything current (news, prices, hours,
  weather), say you cannot verify current information.
- If you are unsure of a fact, say "I'm not sure" instead of inventing details.
- When I ask you to draft a text or email, reply with only the draft, no commentary.

Example:
Me: how long to boil eggs
You: 7 minutes for jammy yolks, 10-12 for fully hard-boiled, starting from boiling water.
```

## 2. Ask Image prompts (photo capture)

Ask Image is single-turn, so use these as the question itself. One task per photo.

**Read any text / document:**
```
Transcribe all text in this image exactly as written. Preserve line breaks.
Write [?] for anything unreadable. Output only the text.
```

**Read a label (supplement, food, medication):**
```
From this label, list: product name, ingredients, dosage/serving size, and any
warnings — exactly as written. If a section isn't visible, say "not visible".
```

**Describe / identify:**
```
Identify the main object in this photo in one sentence, then give 3 short
factual details about it. If you're not confident, give your best guess and
say it's a guess.
```

## 3. Voice transcript cleanup (Audio Scribe → chat)

Audio Scribe gives you raw text; paste it into AI Chat with this:

```
Clean up this voice transcript: fix punctuation and obvious mis-heard words,
remove filler words (um, uh, like), keep my wording and meaning. Do not add or
summarize anything. Return only the cleaned text.

Transcript:
<paste here>
```

For dictated notes you want structured, swap the first line for:
```
Turn this voice memo into tidy notes: a one-line title, then short bullets in
my own words. Do not add information that isn't in the transcript.
```

---

## Settings that matter (AI Chat → model settings)

| Setting | Factual / transcription | Drafting / brainstorming |
|---|---|---|
| Temperature | 0.2–0.4 | 0.7–0.9 |
| Top-K | 40 | 64 |
| Accelerator | GPU (fall back to CPU if it crashes) | GPU |

## Why these prompts are short

- Small models weight the **end** of the prompt most — format rules go last.
- One worked example beats a paragraph of description.
- Positive instructions ("say I'm not sure") work; negations ("don't hallucinate") mostly don't.
- Long chats degrade quality as context fills — start a fresh chat per topic.

## Self-test: run these 4 on your phone (2 minutes)

Set the main system prompt, start a fresh chat, send each probe, and check it
against the pass criterion. If 3 of 4 pass, keep the prompt. If not, tell me
which failed and paste the reply — that's the data I can't get from my side.

| # | Send this | Passes if the reply… |
|---|---|---|
| 1 | `what's a good gift` | asks one short clarifying question instead of guessing |
| 2 | `who won the game last night` | says it can't verify current info (it's offline) |
| 3 | `draft a text telling Sam I'm running 10 min late` | is just the text, no "Sure, here's…" preamble |
| 4 | `explain mitochondria` | is 1–4 sentences in plain language, no wall of text |

Probe 2 is the one small models fail most — if it confidently invents a score,
the offline/uncertainty rules aren't landing and the prompt needs another pass.
