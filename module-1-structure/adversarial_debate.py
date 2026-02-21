from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. SETUP: Separate models prevent memory bleed. 
# The Generator is creative; the Critic is cold and deterministic.
gen_llm = ChatOpenAI(model="<LATEST_CREATIVE_MODEL>", temperature=0.7)
crit_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.0)

def execute_debate(task: str, max_rounds: int = 3) -> str:
    # 2. GENERATION: Prime the first agent to build the raw solution.
    draft = gen_llm.invoke([
        SystemMessage(content="Senior Dev. Write efficient, functional code."),
        HumanMessage(content=f"Draft a solution for: {task}")
    ]).content

    # 3. HOSTILE LOOP: Cap attempts to prevent infinite API billing.
    for _ in range(max_rounds):
        
        # The Critic hunts for flaws. The string 'LGTM' triggers the exit.
        feedback = crit_llm.invoke([
            SystemMessage(content="Ruthless Security Auditor. Find flaws. Do not be polite."),
            HumanMessage(content=f"List fatal flaws. If none, reply exactly 'LGTM'.\n{draft}")
        ]).content

        # 4. EXIT CONDITION: Break the loop if the code passes inspection.
        if "LGTM" in feedback:
            break

        # 5. REVISION: Force the Generator to fix the exact issues found.
        draft = gen_llm.invoke([
            SystemMessage(content="Rewrite the code fixing the listed issues. Output only code."),
            HumanMessage(content=f"Draft:\n{draft}\n\nCritic Feedback:\n{feedback}")
        ]).content

    # Returns the battle-tested output.
    return draft
