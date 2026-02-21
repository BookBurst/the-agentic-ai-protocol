from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. SETUP: Separate models prevent memory bleed. 
gen_llm = ChatOpenAI(model="<LATEST_CREATIVE_MODEL>", temperature=0.7)
crit_llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0.0)

def execute_debate(task: str, max_rounds: int = 3) -> str:
    # 2. GENERATION
    draft = gen_llm.invoke([
        SystemMessage(content="Senior Dev. Write efficient, functional code."),
        HumanMessage(content=f"Draft a solution for: {task}")
    ]).content

    # 3. HOSTILE LOOP
    for _ in range(max_rounds):
        
        feedback = crit_llm.invoke([
            SystemMessage(content="Ruthless Security Auditor. Find flaws. Do not be polite."),
            HumanMessage(content=f"List fatal flaws. If none, reply exactly 'LGTM'.\n{draft}")
        ]).content

        if "LGTM" in feedback:
            break

        # 5. REVISION
        draft = gen_llm.invoke([
            SystemMessage(content="Rewrite the code fixing the listed issues. Output only code."),
            HumanMessage(content=f"Draft:\n{draft}\n\nCritic Feedback:\n{feedback}")
        ]).content

    return draft
