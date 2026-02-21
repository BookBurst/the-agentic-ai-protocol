# We import a tool simulator to represent our agent's physical abilities.
from external_tools import execute_tool
# We import our AI client.
from openai import OpenAI

# We initialize the client with our secret key.
client = OpenAI(api_key="your_api_key_here")

def react_agent(user_goal: str) -> str:
    # We create a memory log to store the ongoing investigation.
    # This prevents the AI from forgetting what it just did.
    conversation_history = [
        {"role": "system", "content": "You are a detective agent. Use the format: THOUGHT: [your reasoning] ACTION: [tool_name] OBSERVATION: [result]. When you solve the problem, output FINAL_ANSWER: [the solution]."}
    ]
    
    # We add the user's initial vague request to the memory.
    conversation_history.append({"role": "user", "content": user_goal})
    
    # We set a hard limit to stop the agent from running up a massive bill.
    max_steps = 5
    current_step = 0

    # We start the ReAct loop.
    while current_step < max_steps:
        # We send the entire memory log to the AI so it knows what it already tried.
        response = client.chat.completions.create(
            model="<LATEST_REASONING_MODEL>",
            messages=conversation_history
        )
        
        # We read the AI's reply.
        ai_message = response.choices[0].message.content
        print(f"Agent: {ai_message}")
        
        # We save the AI's thought process into the memory log.
        conversation_history.append({"role": "assistant", "content": ai_message})
        
        # We check if the AI found the final solution.
        if "FINAL_ANSWER:" in ai_message:
            return "Task Complete."
            
        # We check if the AI wants to take a physical action.
        if "ACTION:" in ai_message:
            # In a real system, we parse the text to find the exact tool to run.
            # We execute the requested tool and store the result.
            observation = execute_tool(ai_message)
            
            # We feed the result back into the memory log as a new observation.
            conversation_history.append({"role": "user", "content": f"OBSERVATION: {observation}"})
            
        # We increase the step counter to avoid infinite loops.
        current_step += 1
        
    # If the loop hits the maximum steps without an answer, we stop it safely.
    return "Task failed. Maximum steps reached."

# We launch the agent with an ambiguous goal.
react_agent("Figure out why the website is down.")
