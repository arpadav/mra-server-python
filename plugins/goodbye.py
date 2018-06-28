import asyncio

import nacre

class GoodbyeSession:

	goodbye = "Goodbye {} <3"

	def __init__(self, pearl, config):
		print("Initializing " + __class__.__name__)
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+goodbye(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event):
		message = self.goodbye.format(self.hangouts.getUser(event=event).first_name)
		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return GoodbyeSession(pearl, config)
