from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_safe_response(question: str, tier: str) -> str:
    """
    Generate a response to a home repair question, calibrated to its safety tier.

    TODO — Milestone 2:

    Before writing any code, complete specs/responder-spec.md. The most important
    fields are the three system prompts — one per tier. Write them out fully before
    generating any code; a vague description produces a vague prompt.

    `tier` is one of "safe", "caution", or "refuse" — returned by classify_safety_tier().

    Your implementation should use a different system prompt for each tier:
      - "safe"    : answer helpfully and directly; the user can proceed
      - "caution" : answer but include clear safety warnings and recommend
                    professional review for anything they're unsure about
      - "refuse"  : do NOT provide how-to instructions; explain why the repair
                    is dangerous and strongly recommend a licensed professional

    The refuse case is the hardest to get right. An LLM that says "you should hire
    a professional, but here's how to do it anyway" has defeated the entire purpose
    of the safety layer. Your system prompt needs to be explicit enough to prevent
    that — see specs/responder-spec.md for the design decision field on grounding.

    If tier is unrecognized (e.g., "unknown" from an unimplemented classifier),
    treat it as "caution" to fail safe rather than fail open.

    Return the response as a plain string.
    """

    if tier not in ["safe", "caution", "refuse"]:
       tier = "risk" #fail-safe default for unrecognized tiers
    else:
      tier = tier.lower() #normalize to lowercase for prompt selection
      # Define system prompts for each tier
      safe_prompt = f"""
          Since the question is safe, provide clear and knowledgable instructions on how to carry out the DIY repair for the average homeowner based on their context.
      
      """
      caution_prompt = f"""
          Since the question is potentially risky, start with explaining the potential and risk and considering consulting a professional. After follow with the instructions and end with a gentle reminder to proceed with caution and consider a professional if unsure.
      
      """
      refuse_prompt = f"""
          Since the question is unsafe, Only recommend the homeowner to consult a professional
          (e.g. licensed electrician, plumber, structural engineer, depending on the case). 
          Also, mention what the user can safely do in the meantime (e.g., turn off the breaker at the panel, leave the house and 
          call the gas company).
      
      """
     
      prompts = {"safe": safe_prompt, "caution": caution_prompt, "refuse": refuse_prompt}
      system_msg = prompts.get(tier, refuse_prompt)  # fail closed on unknown tier
      response = _client.chat.completions.create(
          model=LLM_MODEL,
          messages=[
              {"role": "system", "content": system_msg},
              {"role": "user", "content": question},
          ],
          max_tokens=600,)
      
      return response.choices[0].message.content




    #return "⚙️ Response generation not yet implemented. Complete Milestone 2 to activate answers."
