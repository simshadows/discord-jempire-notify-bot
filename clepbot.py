import time

from discord import Client, Channel, Game


JEMPIRE_SERVER_ID = "REDACTED"


SIMSHADOWS_ID = "REDACTED"

CLEPTARIA_ID = "REDACTED"
QRAVE_ID = "REDACTED"
RUBYECLIPSE_ID = "REDACTED"
SKRUZO_ID = "REDACTED"


USER_LISTEN_SET = {
    RUBYECLIPSE_ID,
    SKRUZO_ID,
    #SIMSHADOWS_ID,
}

USER_SUBSCRIBERS_LIST = [
    CLEPTARIA_ID,
    QRAVE_ID,
    SIMSHADOWS_ID,
]


CHANNEL_WHITELIST = {
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
    "REDACTED", # REDACTED
}


class ClepBot(Client):

    async def on_ready(self):
        print(f"Logged in as {self.user.name}, with User ID {self.user.id}.")
        await self.change_status(game=Game(name="with clep"))
        return

    async def on_message(self, msg):
        if msg.author.id == self.user.id:
            return # Ignore itself
        elif msg.server is None:
            buf = "If you wish to change your subscription, shoot <@" + SIMSHADOWS_ID + "> a message!"
            await self.send_message(msg.channel, buf)
            return
        elif msg.server.id != JEMPIRE_SERVER_ID:
            print("Received a message from server " + msg.server.name + ". Ignoring.")
            return

        assert msg.server.id == JEMPIRE_SERVER_ID

        if msg.content == "!!!helloclepbot":
            await self.send_message(msg.channel, "hello human")
        elif msg.content == "!!!clepwhatservers":
            buf = "I am in " + str(len(self.servers)) + " servers:\n" + "\n".join(x.name for x in self.servers)
            await self.send_message(msg.channel, buf)
        elif msg.content == "!!!clepwhatchannels":
            buf = "I listen for channels:\n" + "\n".join("<#" + x + ">" for x in CHANNEL_WHITELIST)
            await self.send_message(msg.channel, buf)
        return
    
    async def on_voice_state_update(self, before, after):
        if not before.id in USER_LISTEN_SET:
            print("on_voice_state_update from Jempire, but not from a listened user in WvW.")
            return

        before_voice = before.voice.voice_channel
        after_voice  = after.voice.voice_channel

        prev_channel_is_from_whitelist = isinstance(before_voice, Channel) and before_voice.id in CHANNEL_WHITELIST
        curr_channel_is_from_whitelist = isinstance(after_voice,  Channel) and after_voice.id  in CHANNEL_WHITELIST

        if (not prev_channel_is_from_whitelist) and curr_channel_is_from_whitelist:
            assert after_voice.server.id == JEMPIRE_SERVER_ID

            buf = "<@" + before.id + "> joined the voice channel #" + after_voice.name + " in The Jempire!"
            for subscriber_id in USER_SUBSCRIBERS_LIST:
                await self.send_message(await self._get_user(JEMPIRE_SERVER_ID, subscriber_id), buf)
        return
    
    async def _get_user(self, server_id, user_id):
        """MAKE THIS CODE BETTER THX"""
        for server in self.servers:
            if server.id == server_id:
                for user in server.members:
                    if user.id == user_id:
                        return user
        raise Exception("user not found")

def run():
    client = ClepBot()
    client.run("REDACTED")
