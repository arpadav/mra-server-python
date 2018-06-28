import asyncio, random

import nacre

class EightBallSession:

	answers = [
		"It is certain",				#yes1
		"It is decidedly so",			#yes2
		"Without a doubt",				#yes3
		"Yes definitely",				#yes4
		"You may rely on it",			#yes5
		"As I see it, yes",				#yes6
		"Most likely",					#yes7
		"Outlook good",					#yes8
		"Yes",							#yes9
		"All signs point to yes",		#yes10
		"Reply hazy try again",			#uncertain1
		"Better not tell you now",		#uncertain2
		"Maybe",						#uncertain3
		"Not sure"						#uncertain4
		"Why would you even ask that?",	#uncertain5
		"Don't count on it",			#no1
		"My reply is no",				#no2
		"My sources say no",			#no3
		"Outlook not so good",			#no4
		"Very doubtful", 				#no5
		"No",							#no6
		"Absolutely not",				#no7
		"Nope",							#no8
		"All signs point to no", 		#no9
		"Unlikely"						#no10
	]

	def __init__(self, pearl, config):
		print("Initializing " + __class__.__name__)
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+8ball(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event):
		message = random.choice(self.answers)
		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return EightBallSession(pearl, config)
