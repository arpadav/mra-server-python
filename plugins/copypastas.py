import asyncio

import nacre

class CopyPastaSession:

	def __init__(self, pearl, config):
		print("Initializing " + __class__.__name__)
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildUsage()
		self.buildHandle()

	def build(self):
		pass

	def buildUsage(self):
		self.usage = "Copypasta Commands:<br>"
		for command in self.config['commands']:
			self.usage += '<b>{}</b>, {}'.format(command, self.config['commands'][command])

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+copypastas(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event):
		message = self.usage
		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return CopyPastaSession(pearl, config)
