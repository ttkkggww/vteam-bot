import discord.embeds


def convert_embed(contest_status: dict):
    embed = discord.Embed(title=contest_status.get("title"))
    for problem_id in contest_status.get("submissions"):
        field_name = f"Problem {problem_id}"
        field_value = ""
        for team_name in contest_status.get("submissions")[problem_id]:
            field_value += f"{team_name}:"
            submissions = [
                v for v in contest_status.get("submissions")[problem_id][team_name]
            ]
            submissions.sort(key=lambda x: x.get("unix_time"))
            wa = 0
            ac = 0
            for submission in submissions:
                if submission.get("result") == "AC":
                    ac += 1
                    break
                else:
                    wa += 1
            field_value += f"AC:{ac} WA:{wa}\n"

        embed.add_field(name=field_name, value=field_value, inline=False)
    return embed
