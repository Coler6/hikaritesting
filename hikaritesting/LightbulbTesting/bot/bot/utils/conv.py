from datetime import datetime as dt
from os import times_result


def badges(badges):
    print("badges")
    if str(badges) == "NONE":
        return "No badges"
    badge_list = ""
    all_badges = {
        "BUG_HUNTER_LEVEL_1": "<:BugHunterLV1:916092123693064232>",
        "BUG_HUNTER_LEVEL_2": "<:BugHunterLV2:916092123885998181>",
        "DISCORD_CERTIFIED_MODERATOR": "<:DiscordCertifiedModerator:916098293023522927>", 
        "DISCORD_EMPLOYEE": "<:Employee:916092124137672804>",
        "EARLY_SUPPORTER": "<:EarlySupporter:916092123206516757>",
        "EARLY_VERIFIED_DEVELOPER": "<:EarlyVerifiedDeveloper:916097664255393802>",
        "HYPESQUAD_BALANCE": "<:HypeSquadBalance:916092123349143572>",
        "HYPESQUAD_BRAVERY": "<:HypeSquadBravery:916092122556420146>",
        "HYPESQUAD_BRILLIANCE": "<:HypeSquadBrillance:916092122652868629>",
        "HYPESQUAD_EVENTS": "<:HypeSquadEvents:916092123210715166>",
        "PARTNERED_SERVER_OWNER": "<:HypeSquadEvents:916092123210715166>",
    }
    print(badges)
    for badge in badges:
        badge_list = str(badge_list)
        badge_list = badge_list + all_badges[str(badge)]
    print(badge_list)
    return badge_list
    
def msg_emoji(emoji):
    emoji = f"<:{emoji.name}:{emoji.id}>"
    return emoji

def long_delta(td, milliseconds=False):
    print(td)
    parts = ""

    if (d := td.days) != 0:
        parts += f"{d:,} day{'s' if d > 1 else ''}, "

    if (h := td.seconds // 3600) != 0:
        parts += f"{h} hour{'s' if h > 1 else ''}, "

    if (m := td.seconds // 60 - (60 * h)) != 0:
        parts += f"{m} minute{'s' if m > 1 else ''}, "

    if (s := td.seconds - (60 * m) - (3600 * h)) != 0 or not parts:
        if milliseconds:
            ms = round(td.microseconds / 1000)
            parts += f"{s}.{ms} seconds"
        else:
            parts += f"{s} second{'s' if s > 1 else ''}"
    return parts

def time_amount(time, max=None):
    times_abrv = {"s": "second",
                "m": "minute",
                "h": "hour",
                "d": "day",
                "w": "week"}
    times_to_sec = {"second": 1,
                    "minute": 60,
                    "hour": 3600,
                    "day": 86400,
                    "week": 604800}
    for times in times_abrv:
        if times == time[-1]:
            time_type = times_abrv[times]
            new_time = time[:-1]
            print(time)
            print(time_type)
            break
    try:
        new_time = int(new_time)
    except ValueError as e:
        print(e)
        return None, 0
    new_time = new_time*times_to_sec[time_type]
    if max != None and new_time > max:
        return None, 1
    print(new_time)
    return new_time, time_type, int(time[:-1])