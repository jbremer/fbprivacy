import sleekxmpp, sys, time, logging

class PrivacyBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.jids = {}

        self.register_plugin('xep_0054')

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('presence_available', self.handle_presence)
        self.add_event_handler('presence_unavailable', self.handle_presence)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def handle_presence(self, event):
        jid = event['from']

        # determine if presence is available
        presence = 1 if event.get_type() == 'available' else 0

        # get name of this account
        if not jid in self.jids and presence:
            vcard = self['xep_0054'].get_vcard(jid=jid)
            self.jids[jid] = vcard['vcard_temp']['FN']

        # log info
        print jid, repr(self.jids.get(jid, 'None')), presence, int(time.time())

if __name__ == '__main__':
    xmpp = PrivacyBot(sys.argv[1], sys.argv[2])
    xmpp.connect()
    xmpp.process(block=True)
