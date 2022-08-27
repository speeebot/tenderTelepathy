# tenderTelepathy
Discord bot for caching (a quicker alternative to searching each time) and randomly displaying user uploaded messages. 

1. Create a [MongoDB](https://www.mongodb.com/basics/create-database) database and make a Discord bot [account](https://discordpy.readthedocs.io/en/stable/discord.html).
2. Define the environment variables in the .env file.
3. Add a channel in your discord server for the bot called "telepathy".
4. Make sure [Docker](https://docs.docker.com/engine/install/) is installed and generate a Docker image: ```docker build -t telepathy .```
5. Then bring the bot online: ```docker run telepathy```
6. Lastly, invite the bot to your server with the URL printed in the terminal.

TODO:
- Clean up code
- Have bot automatically check for images from last known message forward
