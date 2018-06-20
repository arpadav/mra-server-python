# mra-server-python
Mathakan Red Alert: Server-end Python Script

# Chat-bot instructions:
* #1. Plugins folder
	
	In order to add commands to the chat-bot for Mathakan, navigate your way to `./plugins` where you can see all the other commands.


* #2. Duplication:
	
	The easiest way to make a new chatbot command is to duplicate a preexisting one and changing some stuff. The easiest to duplicate would be one of the copypastas, since the bot reads a command and simply spits back text.
	
	The other ones like `!8ball` and `!haines` can be used as templates for a command to randomly pick out an answer from a string array.
	
	`!hello` and `!goodbye` find the users name to make the chat-bot experience more interactive.
	
	(There are ways to implement API's with the chat-bot, but I have yet to do that and probably will not in the near future.)

	
* #3. Renaming and replacing:
	
	After one is duplicated, rename the `.py` file to whatever command you will use. Ex: if you want `!killallhumans`, rename to `killallhumans.py`. And there is a whole lot more renaming to do lol
	
	Inside your new `.py` file, find the following line of code in `def buildHandle(self)`:
	
	`messageFilter = nacre.handle.newMessageFilter('^{}+COMMAND(\s.*)?$'.format(self.pearl.config['format']))`
	
	Replace `COMMAND` with your command, so in this example replace with "killallhumans". Change the class name from `CommandSession` to `KillAllHumansSession`, and at the bottom replace ` return CommandSession(pearl, config)` with ` return KillAllHumansSession(pearl, config)`

	
* #4. Changing message:
	Now inside of:
	
	`async def respond(self, event):` 
	
	change what the message is equal to, like in this example: 
	
	`message = 'I want to kill all humans!'`
	
	
* #5. Configuring your new command:
	
	Navigate your way back to the master branch and find `config.json`. Add a new segment in `config.json` ALPHABETICALLY (pls) according to your command name like so:
```
"plugins": {
	"8ball": {
		"path": "plugins/eightball.py"
	},
	"begone": {
		"path": "plugins/begone.py"
	},
	"killallhumans": {
		"path": "plugins/killallhumans.py"
	}
}
```
	
* #6. Pushing:
	
	Push the project back here, let me know, and I will pull and restart the server. If you followed all steps completely, the command should work!
	
# Notice

In here I have a couple files, like `client_secret.json` and `credentials.json`/`credentials0.json`. These are vital and PRIVATE for the script to access the Mathakan Hangouts group chat. Should I remove them off of GitHub so no-one else can somehow use them? I don't think it should be a problem since they still need to validate using Oath2Client, but still. I can remove them if ya'll want.