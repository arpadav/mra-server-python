import asyncio
import nacre
import time

startTime = time.time()

class UptimeSession:

	def __init__(self, pearl, config):
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+uptime(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	def gettime(self):
		t = (time.time() - startTime)

		day = int(t // (24 * 3600))
		t = t % (24 * 3600)
		hour = int(t // 3600)
		t %= 3600
		minute = int(t // 60)
		t %= 60
		second = t

		if day == 0:
			if hour == 0:
				if minute == 0:
					return str(round(second, 2)) + "s"
				return str(minute) + "m " + str(round(second, 2)) + "s"
			return str(hour) + "h " + str(minute) + "m " + str(round(second, 2)) + "s"
		return str(day) + "d " + str(hour) + "h " + str(minute) + "m " + str(round(second, 2)) + "s"

	async def respond(self, event):
		message = self.gettime()
		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return UptimeSession(pearl, config)
