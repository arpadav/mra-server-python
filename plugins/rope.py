import asyncio

import nacre
import json, random

class RopeSession:

	phrase = [
		"killed themselves",
		"commited suicide",
		"roped themselves",
		"ended it"
	]

	def __init__(self, pearl, config):
		print("Initializing " + __class__.__name__)
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()
		self.datapath = 'plugins/data/rope.json'

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+rope(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event):
		with open(self.datapath) as f1:
			fdata = json.load(f1)
			try:
				fdata[str(event.sender_id.gaia_id)] += 1
				message = self.hangouts.getUser(event=event).first_name + " has " + random.choice(self.phrase) + " " + str(fdata[str(event.sender_id.gaia_id)]) + " times."
			except:
				message = "This is the first time " + self.hangouts.getUser(event=event).first_name + " has " + random.choice(self.phrase) + "!"
				fdata[str(event.sender_id.gaia_id)] = 1
			with open(self.datapath, 'w') as f:
				json.dump(fdata, f, indent = 4)
		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return RopeSession(pearl, config)
