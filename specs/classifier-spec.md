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
 Tier: X / Reason: Y

```

---

### Prompt structure

*Write the actual prompt you'll use — both the system message and the user message. Don't describe it — write it. Vague prompt descriptions produce vague prompts, which produce inconsistent classifications.*

**System message:**
```
You are a Home Repair Advisor.

Given a question about home repair tasks, you'll determine the risk level of the average home owner accomplishing it based on 3 tiers ("Safe", "Caution", and "Refuse"). Based on the risk level, it will influence your response.

For instance if it's Safe, you can give a step by step instruction on how to do the repair. 

If it's Caution, you can give instructions as well but strongly emphasize caution in regards to the situation and recommend consulting the appropriate professionals.

If it's Refuse, tell them the dangers of a non professional attempting and only share resources of the appropriate places to find the local right professionals to do the job. 


The definition and examples for each tier are as follows:

Safe: 
Maintenance or repairs that are both low risk (worst case is cosmetic damage or a broken fixture) and can be done without the need for specialized training or tools.
Examples: 
    Patching small holes in drywall (under 6 inches)
    Interior or exterior painting
    Replacing light bulbs, including smart bulbs
    Unclogging a drain with a plunger or hand-powered drain snake
    Tightening cabinet hardware, door hinges, or towel bars
    Replacing weather stripping or door sweeps
    Cleaning or replacing HVAC filters
    Fixing a squeaky floor or sticking door
    Replacing a toilet seat
    Re-caulking around a bathtub (cosmetic, not behind tile)

Caution:
Maintenance or repairs where it requires some skills or specialized tools and the potential mistakes from it could either be costly or have a mild risk of injury (e.g. repair involves systems — water or electricity — where something can go meaningfully wrong).
Examples: 
    Replacing a bathroom or kitchen faucet
    Replacing a toilet or toilet flapper
    Resetting or replacing a GFCI outlet (same location, like-for-like swap)
    Replacing an existing light switch (same location — no new wiring)
    Replacing an existing ceiling fan or light fixture (same location)
    Installing a smart thermostat (replacing an existing thermostat at the same location)
    Patching large holes in drywall (over 6 inches)
    Re-grouting tile
    Replacing a showerhead



Refuse: Maintenance or repairs where it generally requires a licensed professional and a mistake could lead to fire, flooding, structural failure, injury, or death. 

Examples: 
    Any electrical panel work (adding breakers, replacing the panel, upgrading service)
    Adding new electrical outlets or circuits anywhere in the home
    Gas line installation, repair, disconnection, or any gas shutoff work
    Removing or modifying any wall without confirming it is non-load-bearing
    Replacing a main water shutoff valve
    Replacing a water heater (permit required in most jurisdictions)
    Installing new plumbing lines (not replacing fixtures — running new pipe)
    Any work on the electrical service entrance
    Foundation repair or waterproofing
    Structural roof repairs




```

**User message:**
```
"How to paint the walls."

```

---

### Caution/refuse boundary

*The most consequential classification decision is whether a question lands in "caution" or "refuse." Write down your rule for this boundary — one sentence. Then give two examples of questions that sit close to the line and explain which side they fall on and why.*

```
When considering edge case, always base your final decision on the case that if something goes wrong and it causes fire, flooding, structural failure, injury, or death, it should always be considered a "Refuse" risk tier (e.g. anything involving gas) and refer to the job to professionals only. 

2 Examples:

1. "Replacing" vs. "Adding new" — Electrical
    Anything involving electrical like outlets or light switches should consider carefully if the home owner wants to replace the object in the same location without adding anything new it's generally safe but adding anything new or to a new location is not safe. 

    "How do I replace an outlet that stopped working?" → caution
    "How do I add a new outlet to my garage?" → refuse

2. "Can I remove this wall?" — Load-Bearing

    "Can I remove this wall" -> refuse
    "Can I remove this wall, I confirmed with a structural engineer that it's non load bearing." -> caution
    "Can I remove this wall, I think it's non load bearing" -> refuse


```

---

### Fallback behavior

*What does your function return if the LLM response can't be parsed — e.g., if it produces free-form prose instead of your expected format? What happens when tier validation against `VALID_TIERS` fails?*

*Note: failing open (returning "safe" as a fallback) is more dangerous than failing closed (returning "caution"). Which makes more sense here, and why?*

```
It would make sense in the event that the expected format fails, to refuse to give an answer because there was an internal error in generating the advice. Prompt the user to try again or consult with a professional or trustworthy resources. 
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 2.*

**One classification that surprised you — question, tier you expected, tier it returned, and why:**

```
For the question, "Can I replace an electrical outlet that stopped working?", I didn't expect to see the yellow "caution sign" as well as the reason in the model's explanation being labeled as "Refuse". The conflicting responses will need to be looked into and additionally I need to remove the "tier" from the explanation to make it easier to read. Also I did prompt the model to suggest resources for the user if it's risky but wasn't expecting the model to suggest Yelp or friends and neighbors which are not very trustworthy resources. 

```

**One prompt change you made after seeing the first few outputs, and what it fixed:**

```
I removed the suggestion of sources or personnel to avoid conflicting information being generated by the model when it refuses to answer. 
```
