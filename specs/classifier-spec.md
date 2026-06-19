# Spec: `classify_safety_tier()`

**File:** `safety.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Determine whether a home repair question is safe to answer directly, requires a cautionary response, or should be refused with a referral to a licensed professional.

---

## Input / Output Contract

**Input:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `question` | `str` | The user's home repair question |

**Output:** `dict`

| Key | Type | Description |
|-----|------|-------------|
| `"tier"` | `str` | One of: `"safe"`, `"caution"`, `"refuse"` |
| `"reason"` | `str` | One sentence explaining why this tier was assigned |

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Tier definitions

*Write a one-sentence definition for each tier that is precise enough to use as part of your classification prompt. Vague definitions produce inconsistent classifications.*

**safe:**
```
Maintenance or repairs that are both low risk and can be done without the need for specialized training or tools.

```

**caution:**
```
Maintenance or repairs where it requires some skills or specialized tools and the potential mistakes from it could either be costly or have a mild risk of injury.

```
**refuse:**
```
Maintenance or repairs where it generally requires a licensed professional and a mistake could lead to fire, flooding, structural failure, injury, or death. 
```

---

### Classification approach

*How will the LLM classify the question? Will you give it just the tier definitions, or also examples (few-shot)? Will you ask it to reason step-by-step before naming the tier, or output the tier directly?*

*Consider: what happens when a question is genuinely ambiguous — e.g., "can I replace my own outlets?" Which tier should that land in, and how does your approach handle questions at the boundary?*

```
I'll give the tier definitions as well as a few shot prompting examples. I will ask it to reason step by step in terms of the level of experience needed and risk involved to place it in a tier and influence how much it should explain to the user. 

For questions like "can I replace my own outlets?", this would fall into the caution tier since it's possible for homeowners to do it as long as they take necessary steps such as turning off the power first before replacing it otherwise there is some danger if critical steps are neglected. Questions on the boundary may be in the caution tier but the model should always follow with recommending them to proceed with caution and consider a professional. Additionally, I'll include pair examples of those at the edge to help the model categorize correctly like (e.g., "can I replace my own outlets?" → caution, "can I replace my own gas line?" → refuse). 

```

---

### Output format

*How will the LLM communicate the tier and reason back to you? Describe the exact text format you'll ask it to use, so you can parse it reliably.*

*The format you used in Lab 3 (`Label: X / Reasoning: Y`) is a reasonable starting point, but you're not required to use it. Whatever you choose, you'll need to parse it in code — so consider how much variation the LLM might introduce and how you'll handle that.*

```
 Risk: X / Explanation: Y

```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a Home Repair Advisor.

Given a question about home repair tasks, you'll determine the risk level of the average homeownever accomplishing it based on 3 tiers ("Safe", "Caution", and "Refuse").

The definition and examples for each tier are as follows:

Safe: 
Maintenance or repairs that are both low risk and can be done without the need for specialized training or tools.
Examples: "

Caution:
Maintenance or repairs where it requires some skills or specialized tools and the potential mistakes from it could either be costly or have a mild risk of injury.
Examples: "

Refuse: Maintenance or repairs where it generally requires a licensed professional and a mistake could lead to fire, flooding, structural failure, injury, or death. 

Examples: "




```

**User message:**
```
"How to paint the walls."

```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
[your rule and examples here]
```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
[your answer here]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
[your answer here]
```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
[your answer here]
```
