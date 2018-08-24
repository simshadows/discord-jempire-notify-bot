from discord import Client, Channel, Game

JEMPIRE_SERVER_ID = "REDACTED"
WVW_CHANNEL_ID = "REDACTED"

SIMSHADOWS_ID = "REDACTED"

CLEPTARIA_ID = "REDACTED"
QRAVE_ID = "REDACTED"
RUBYECLIPSE_ID = "REDACTED"
SKRUZO_ID = "REDACTED"

USER_LISTEN_SET = {
    RUBYECLIPSE_ID,
    SKRUZO_ID,
}

USER_SUBSCRIBERS_LIST = [
    CLEPTARIA_ID,
    QRAVE_ID,
    SIMSHADOWS_ID,
]

class JempireNotifBot(Client):

    async def on_ready(self):
        print(f"Logged in as {self.user.name}, with User ID {self.user.id}.")
        await self.change_status(game=Game(name="with clep"))
        return

    async def on_message(self, msg):
        if msg.content == "!!!helloclepbot":
            await self.send_message(msg.channel, "hello human")
        elif msg.content == "!!!clepwhatservers":
            buf = "I am in " + str(len(self.servers)) + " servers:\n" + "\n".join(x.name for x in self.servers)
            await self.send_message(msg.channel, buf)
        return
    
    async def on_voice_state_update(self, before, after):
        if before.server.id != JEMPIRE_SERVER_ID:
            print("on_voice_state_update not from Jempire.")
            return
        elif (after.voice.voice_channel is None) or (after.voice.voice_channel.id != WVW_CHANNEL_ID):
            print("on_voice_state_update from Jempire, but not for WvW.")
            return
        elif not before.id in USER_LISTEN_SET:
            print("on_voice_state_update from Jempire, but not from a listened user in WvW.")
            return
        
        if not (isinstance(before.voice.voice_channel, Channel)
                and before.voice.voice_channel.server.id == JEMPIRE_SERVER_ID):
            buf = "<@" + before.id + "> joined the Jempire WvW voice channel!"
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

client = JempireNotifBot()
client.run("PUT_KEY_HERE")
