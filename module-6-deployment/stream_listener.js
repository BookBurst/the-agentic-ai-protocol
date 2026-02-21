// We open the radio connection to our specific server URL.
const source = new EventSource("https://your-server.com/stream_agent_task?query=analyze");
const outputBox = document.getElementById("agent-output");

// The 'onmessage' event triggers automatically every time a new chunk arrives.
source.onmessage = function(event) {
    const incomingText = event.data;
    
    // We filter out the invisible heartbeat pings so they never show on screen.
    if (incomingText === "[HEARTBEAT_PING_IGNORE]") {
        return; 
    }
    
    // We close the radio connection once the final signal arrives.
    if (incomingText === "[END_OF_STREAM]") {
        source.close();
        return;
    }
    
    // We append the new word to the existing text in the dashboard.
    outputBox.innerHTML += incomingText;
};

// If the network completely fails, we log the error and close the connection.
source.onerror = function(error) {
    console.error("The radio broadcast dropped.", error);
    source.close();
};
