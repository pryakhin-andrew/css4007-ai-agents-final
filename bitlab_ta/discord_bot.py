from .config import Settings

# Discord listener skeleton. Completed in Week 11.
#
# Design notes for the real implementation:
#   - A dedicated bot account (not a personal account) reads DMs and channel
#     mentions. Message Content intent must be enabled.
#   - on_message handles two entry points: direct messages, and messages that
#     mention the bot in a server channel.
#   - The reply tool's approval step maps to a DM sent to APPROVER_DISCORD_ID;
#     only after the approver confirms is the message posted to the student.


def run_bot(settings: Settings) -> None:
    import discord

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message: "discord.Message") -> None:
        if message.author == client.user:
            return
        is_dm = message.guild is None
        is_mention = client.user in getattr(message, "mentions", [])
        if not (is_dm or is_mention):
            return
        raise NotImplementedError("Agent + approval wiring is built in Week 11")

    client.run(settings.discord_bot_token)
