import emoji


def get_all_emojis():
    all_emojis = list(emoji.EMOJI_DATA.keys())
    if "📁" in all_emojis:
        all_emojis.remove("📁")
    all_emojis = sorted(all_emojis)
    return ["📁"] + all_emojis
