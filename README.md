# arpadav/mra-server-python
Mathakan Red Alert: Server-end Python Script

# Notice
You will not be able to run this yourself. Private information (like credentials, auth tokens, conversation id's, usernames, and passwords) are missing and stored locally on my computer. This is just to prevent others from gaining access to MRA's Google Account.

# Adding commands to chat-bot instructions:
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
	
	(NOTE: the message string is processed into HTML, so you can add commands like <br>, <b>, <i>, <u>, etc. to format the message accordingly)
	
	
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

# Changing MRA APP notifications
* send.py

	`send.py` is the Python script which runs both the chat-bot and the MRA app notifications asynchronously. Ignore everything other than the following:
	
	** variable called `multiline`
	
		This is the actual message that is sent to the Mathakan Hangouts. It can be formatted with HTML, so feel free to bold, underline, etc. For some reason hyperlinks can not be embedded with `<a href="url.com">Link to url.com</a>`. Just send the raw URL and it will auto-convert to a hyperlink.
	
	** function called `randoMes()`
	
		This is the random pop-up message that generated for `multiline` to send to the Mathakan Hangouts. Feel free to add more emojis and messages of your liking.
		
	** function called `randoEmoji(type)`
		
		This is a function which returns a random emoji from different lists. If we add a lot of arrays of emojis, we can add a switch statement instead of a bunch of elseifs.