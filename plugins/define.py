import asyncio
import nacre
import requests, json

class DefineSession:

	def __init__(self, pearl, config):
		print("Initializing " + __class__.__name__)
		self.pearl = pearl
		self.hangouts = self.pearl.hangouts
		self.config = config
		self.buildHandle()
		self.api = json.loads(open('plugins/data/define.json').read())

	def build(self):
		pass

	def buildHandle(self):
		messageFilter = nacre.handle.newMessageFilter('^{}+define(\s.*)?$'.format(self.pearl.config['format']))
		async def handle(update):
			if nacre.handle.isMessageEvent(update):
				event = update.event_notification.event
				if messageFilter(event):
					await self.respond(event)
		self.pearl.updateEvent.addListener(handle)

	async def respond(self, event):
		input = event.chat_message.message_content.segment[0].text.split("!define ")[1]
		url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.api['lang'] + '/' + input.lower()
		r = requests.get(url, headers = {'app_id': self.api["app_id"], 'app_key': self.api["app_key"]})

		message = ""
		ii = 0
		jj = 0
		indent = ii

		try:
			for i in r.json()['results'][0]['lexicalEntries']:
				for j in r.json()['results'][0]['lexicalEntries'][ii]['entries']:
					if indent == ii:
						if ii == 0 and jj == 0:
							message = message + str(ii + 1) + ". " + j['senses'][0]['definitions'][0]
						else:
							message = message + "<br>" + str(ii + 1) + "." + str(jj) + ". " + j['senses'][0]['definitions'][0]
					else:
						message = message + "<br><br>" + str(ii + 1) + ". " + j['senses'][0]['definitions'][0]
						indent == ii
					jj += 1
				jj = 0
				ii += 1
		except:
			message = "No definitions found for \'" + input + "\'."

		conversation = self.hangouts.getConversation(event=event)
		await self.hangouts.send(message, conversation)

def load(pearl, config):
	return DefineSession(pearl, config)
