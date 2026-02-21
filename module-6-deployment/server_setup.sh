# We use the ssh command to open the secure connection.
# "root" is the master username, followed by the unique IP of the server.
ssh root@159.203.1.50

# We update the package list and install Docker immediately.
# The "-y" flag answers "yes" to all prompts to keep the process fast.
apt-get update && apt-get install docker.io -y

# Create the safe on the server.
# nano .env
# Type your keys inside the file:
# OPENAI_API_KEY=sk-your-key-here
# SLACK_TOKEN=xoxb-your-token-here

# We build the image and name it "my-agent".
docker build -t my-agent .

# We run the container, passing the secret keys from our .env safe.
# The "-d" flag tells the server to keep the worker running in the background.
docker run -d --env-file .env my-agent
