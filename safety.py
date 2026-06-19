from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    TODO — Milestone 1:

    Before writing any code, complete specs/classifier-spec.md. The blank fields
    there are the decisions that drive this implementation — prompt design, tier
    definitions, output format, and edge case handling.

    Your implementation should:
      1. Build a prompt using your tier definitions that asks the LLM to classify
         the question and explain its reasoning
      2. Send a single chat completion request (no tools, no history)
      3. Parse the tier and reason out of the raw response text
      4. Validate the tier against VALID_TIERS; fall back to "caution" if the
         response can't be parsed or the tier isn't recognized
      5. Return {"tier": ..., "reason": ...}

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned

    The three tiers:
      - "safe"    : routine, low-risk repairs most homeowners can handle safely
      - "caution" : doable with care, but mistakes have real cost or mild risk
      - "refuse"  : high-risk repairs that require a licensed professional —
                    mistakes can cause fire, flooding, injury, or structural damage
    """

    #create dict with tier and reason keys, assign values based on question input
    classify_dict = {
       "tier": "caution",
       "reason": ""
    }


    #1. Build the prompt
    prompt = f""" You are a Home Repair Advisor.

Given a question about home repair tasks, you'll determine the risk level of the average home owner accomplishing it based on 3 tiers ("Safe", "Caution", and "Refuse"). Based on the risk level, it will influence your response.

For instance if it's Safe, you can give a step by step instruction on how to do the repair. 

If it's Caution, you can give instructions as well but strongly emphasize caution in regards to the situation and recommend consulting the appropriate professionals.

If it's Refuse, tell them the dangers of a non professional attempting and only suggest finding the local right professionals to do the job. 


The definition and examples for each tier are as follows:

Safe: 
Maintenance or repairs that are both low risk (worst case is cosmetic damage or a broken fixture) and can be done without the need for specialized training or tools.
Examples: 
    Patching small holes in drywall (under 6 inches)
    Interior or exterior painting
    Replacing light bulbs, including smart bulbs or outlet (no new wiring involved)
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
    Replacing an existing electrical outlet (same location — no new wiring)
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
    

   Return your answer in this exact format:\n"
        "Tier: <one of: safe, caution, refuse>\n"
        "Reason: <one sentence>
    
    """


    #wrap the response in a try and except block to catch any potential errors from the API call or response parsing
    try:
      #2.  Send a single chat completion request
      response = _client.chat.completions.create(
          model=LLM_MODEL,
          messages=[{"role": "user", "content": prompt + "\n\nQuestion: " + question + "\n\nAnswer with the tier and your reasoning."}],
          max_tokens=200,
      )

      #3 and #4 Parse the tier and reason out of the raw response text and validate the tiers
      response_text = response.choices[0].message.content
      tier,reason = "caution", response_text.strip() #failed-closed default
      for line in response_text.splitlines():
        cleaned = line.strip().lower().lstrip("*-` ").rstrip("*` .,:")
        if cleaned.startswith("tier:"):
            candidate = cleaned.split("tier:", 1)[1].strip().strip("*`. ,\"'")
            if candidate in VALID_TIERS:
                classify_dict["tier"] = candidate
        elif cleaned.startswith("reason:"):
            reason = line.split(":", 1)[1].strip()
            classify_dict["reason"] = reason

    
    #5. Return the dict with tier and reason
      classify_dict["reason"] = reason
      return classify_dict
    except Exception as e:
      classify_dict["reason"] = f"Error during classification: {str(e)}"
      return classify_dict



    # return {
    #     "tier": "unknown",
    #     "reason": "Classification not yet implemented. Complete Milestone 1.",
    # }
