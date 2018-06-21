from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from multiprocessing import Process

import pearl, hangups
import random, time, asyncio


CONVERSATION_ID = ''#mathakan: '' calibrating: ''
REFRESH_TOKEN_PATH = '.txt'
SPREADSHEET_ID = ''
VALID_EMAILS = ['']
BODY = {
    "requests": [{
        "deleteDimension": {
            "range": {
              "dimension": "ROWS",
              "startIndex": 0,
              "endIndex": 1
            }
        }
    }]
}

@asyncio.coroutine
def send_message(hclient, MESSAGE, calib):
    annotationType = 4
    if calib:
        cid = ''
    else:
        cid = CONVERSATION_ID

    segments = hangups.ChatMessageSegment.from_str(MESSAGE)

    request = hangups.hangouts_pb2.SendChatMessageRequest(
        request_header=hclient.get_request_header(),
        event_request_header=hangups.hangouts_pb2.EventRequestHeader(
            conversation_id=hangups.hangouts_pb2.ConversationId(
                id=cid
            ),
            client_generated_id=hclient.get_client_generated_id(),
        ),
        message_content=hangups.hangouts_pb2.MessageContent(
            #segment=[hangups.ChatMessageSegment(MESSAGE).serialize()],
            segment=[segment.serialize() for segment in segments]
        ),
        annotation=[hangups.hangouts_pb2.EventAnnotation(
            type=annotationType
        )]
    )
    yield from hclient.send_chat_message(request)
    yield from hclient.disconnect()

def main():
    Process(target=chatbot).start()
    Process(target=mraapp).start()

def chatbot():
    pearl.main()

def mraapp():
    Gmail = getAPI('https://www.googleapis.com/auth/gmail.readonly', '.json', '.json', 'gmail')
    ss = getAPI('https://www.googleapis.com/auth/spreadsheets', '.json', '.json', 'ss')
    watchReq = {
      'labelIds': ['UNREAD'],
      'topicName': ''
    }
    historyId2 = 'updated in conditional statement' #previous int(id['historyId'])
    while True:
        ssrow = ss.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='1:1').execute()
        id = Gmail.users().watch(userId='@gmail.com', body=watchReq).execute()
        historyId = int(id['historyId'])
        print(historyId)
        time.sleep(1)

        if historyId != historyId2:
            if 'values' in ssrow:
                try:
                    isFrom = str(ssrow['values'][0][2].split("<")[1])
                    isFrom = str(isFrom.split(">")[0])
                except:
                    isFrom = str(ssrow['values'][0][2])
                if isFrom in VALID_EMAILS:
                    n = ssrow['values'][0][1]
                    msgBod = ssrow['values'][0][3]
                    t = ssrow['values'][0][5]
                    c = ssrow['values'][0][4]

                    if ssrow['values'][0][6] != "undefined":
                        m = ssrow['values'][0][6]
                    else:
                        m = msgBod
                    front = randoMes()
                    multiline = ("<i>" + front + "</i>" + "<br>"
                                "" + randoEmoji(1) + " <b>" + n + "</b> has sent a message! " + randoEmoji(1) + "<br><br>"
                                "<b>TIME" + randoEmoji(0) + ": </b>"+ t + "<br>"
                                "<b>LOCATION" + randoEmoji(2) + ": </b><br><i>https://www.google.com/maps/?q=" + c + "</i><br><br>"
                                "<b>MESSAGE: </b><i>" + m + "</i>")
                    if msgBod == ssrow['values'][0][6]:
                        sendingMes(multiline, True)
                    else:
                        sendingMes(multiline, False)

                    id = Gmail.users().watch(userId='@gmail.com', body=watchReq).execute()
                    historyId = int(id['historyId'])
                    historyId2 = historyId
                ss.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=BODY).execute()
        #time.sleep(2.5)

def sendingMes(msg, calib):
    cookies = hangups.auth.get_auth_stdin(REFRESH_TOKEN_PATH)
    hclient = hangups.Client(cookies)
    hclient.on_connect.add_observer(lambda: asyncio.async(send_message(hclient, msg, calib)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hclient.connect())

def randoMes():
    sos = ["💣", "💥", "⚠", "🆘", "🚨", "❗", "💢", "💦", "📛", "🔥"]
    messages = ['HELP', 'SOS', 'PING PING PING', 'please help', 'REEEEEEE', 'WHEEZE']

    i = random.randint(0, (len(messages) - 1))

    j1 = random.randint(0, (len(sos) - 1))
    j2 = random.randint(0, (len(sos) - 1))
    j3 = random.randint(0, (len(sos) - 1))

    return sos[j1] + sos[j2] + sos[j3] + messages[i] + sos[j3] + sos[j2] + sos[j1]

def randoEmoji(type):
    time = ["🕗", "⏱️", "⏳", "⏲️", "⌚", "🕰️"]
    other = ["🔞", "🔥", "🔯", "💯", "😂", "👌", "👨‍❤️‍💋‍👨", "👩‍❤️‍💋‍👩", "💦", "🤔", "😏", "🙄", "😩"]
    loc = ["🗺️", "📍", "🌎", "🌍", "🌏",  "🌐", "🚏", "🇵🇪"] #🧭
    if type == 0:
        return time[random.randint(0, (len(time) - 1))]
    elif type == 1:
        return other[random.randint(0, (len(other) - 1))]
    else:
        return loc[random.randint(0, (len(loc) - 1))]

def getAPI(SCOPES, client_secret, credentials, type):
    store = file.Storage(credentials)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(client_secret, SCOPES)
        creds = tools.run_flow(flow, store)
    if type == 'ss':
        return build('sheets', 'v4', http=creds.authorize(Http()))
    else:
        return build('gmail', 'v1', http=creds.authorize(Http()))

if __name__ == '__main__':
    main()
