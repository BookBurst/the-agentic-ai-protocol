import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# We simulate the AI's slow generation process using a generator function.
# The 'yield' keyword is the secret. It spits out one piece of data and pauses,
# keeping the function alive instead of returning a single final block.
async def agent_thought_stream(prompt: str):
    # Step 1: The agent acknowledges the command immediately to open the channel.
    yield "data: Action acknowledged. Starting deep research...\n\n"
    
    # Step 2: We simulate a long period of silence while the agent reads a file.
    # The heartbeat keeps the connection alive during this 45-second pause.
    for _ in range(3):
        await asyncio.sleep(15)
        # This invisible ping resets the browser's timeout clock.
        yield "data: [HEARTBEAT_PING_IGNORE]\n\n"
        
    # Step 3: The agent finishes reading and starts streaming the actual answer.
    simulated_words = ["The ", "market ", "shows ", "strong ", "growth ", "potential."]
    
    for word in simulated_words:
        # We add a slight delay to mimic the processor calculating the next token.
        await asyncio.sleep(0.5)
        
        # We stream each individual word down the open radio channel.
        yield f"data: {word}\n\n"
        
    # Step 4: We send a final signal telling the browser the broadcast is officially over.
    yield "data: [END_OF_STREAM]\n\n"

# We open the specific route that the frontend dashboard will connect to.
@app.get("/stream_agent_task")
async def trigger_agent(query: str):
    # We return a StreamingResponse, which tells the server to leave the door open
    # and push the yielded data out to the client continuously.
    return StreamingResponse(agent_thought_stream(query), media_type="text/event-stream")
