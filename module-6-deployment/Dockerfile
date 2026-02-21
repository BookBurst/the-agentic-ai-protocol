# We start by grabbing a pre-built, official version of Python.
# This guarantees we always use version 3.11, no matter what the server has installed locally.
FROM python:3.11-slim

# We tell the container to do all its work inside a dedicated folder called /app.
WORKDIR /app

# We copy our list of required libraries from our laptop into the container's workspace.
COPY requirements.txt .

# We force the container to install every single library exactly as listed.
# The --no-cache-dir flag keeps the final box lightweight by deleting temporary files after installation.
RUN pip install --no-cache-dir -r requirements.txt

# We copy the rest of our actual agent code into the container so it has the instructions.
COPY . .

# We tell the container what command to run the moment it wakes up on the server.
CMD ["python", "agent.py"]
