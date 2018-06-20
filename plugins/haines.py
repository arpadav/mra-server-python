import asyncio, random

import nacre

class HainesSession:

	answers = [
		"Ceteris paribus",
		"George Rateb",
		"I don't believe in luck.",
		"<b>Grow up.<b>",
		"James Mazerell",
		"Turn to the page between 665 and 667."
	]

	def __init__(self, pearl, config):
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+haines(\s.*)?$'.format(self.pearl.config['format']))
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
	return HainesSession(pearl, config)
