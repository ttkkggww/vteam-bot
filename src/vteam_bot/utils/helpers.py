import discord.embeds


def convert_embed(contest_status: dict):
    embed = discord.Embed(title=contest_status.get("title"))
    for problem_id in contest_status.get("submissions"):
        field_name = f"Problem {problem_id}"
        field_value = ""
        for team_name in contest_status.get("submissions")[problem_id]:
            field_value += f"{team_name}:"
            problem_submission = contest_status.get("submissions")[problem_id][team_name]
            submissions = [
                (v,problem_submission[v]) for v in problem_submission
            ]
            print(contest_status.get("submissions"))
            print(submissions)
            submissions.sort(key=lambda x: x[0])
            wa = 0
            ac = 0
            for submission in submissions:
                if submission[1] == "AC":
                    ac += 1
                    break
                else:
                    wa += 1
            if ac > 0:
                field_value += "🟩AC({})".format(wa)
            elif wa > 0:
                field_value += "🟧WA({})".format(wa)
            else:
                field_value += "⬜"
            field_value += "\n"

        embed.add_field(name=field_name, value=field_value, inline=False)
    return embed
