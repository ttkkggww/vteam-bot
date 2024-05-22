from datetime import datetime
import asyncio
from .atcoder_api import AtCoderAPI


class ContestManager:
    def __init__(self, settings: dict, interval: int):
        self.title = settings.get("title", "no title")
        self.start_time = datetime.fromisoformat(
            settings.get("start_time", "1970-01-01T00:00:00")
        )
        self.contest_length = settings.get("contest_length", 0)
        self.problem_set = settings.get("problem_set", [])
        # teams = [{"name": "team1", "member_ids": ["user1", "user2"]}, ...]
        self.teams = settings.get("teams", [])
        self.team_names = [team.get("name") for team in self.teams]

        self.lock = asyncio.Lock()
        self.contest_status = {
            "contest_active": True,
            "submissions": {
                problem_id: {team_name: {} for team_name in self.team_names}
                for problem_id in self.problem_set
            },
        }

        self.interval = interval

        self.user_ids = [team.get("member_ids") for team in self.teams]
        self.team_index = 0
        self.user_index = 0
        return

    async def submission_update(self, team_name: str, user_id: str):
        unix_time = str(self.start_time.timestamp())
        unix_time = str(int(self.start_time.timestamp()))
        submissions = AtCoderAPI.get_submissions(user_id=user_id, unix_second=unix_time)
        print(self.contest_status)
        for submission in submissions:
            id = submission.get("id")
            unix_time = submission.get("epoch_second")
            problem_id = submission.get("problem_id")
            result = submission.get("result")
            async with self.lock:
                if problem_id in  self.contest_status["submissions"]:
                    self.contest_status["submissions"][problem_id][team_name][unix_time]= result


    async def contest_update(self):
        await self.submission_update(
            self.team_names[self.team_index],
            self.user_ids[self.team_index][self.user_index],
        )
        self.user_index += 1
        if self.user_index >= len(self.user_ids[self.team_index]):
            self.user_index = 0
            self.team_index += 1
            if self.team_index >= len(self.user_ids):
                self.team_index = 0

    def get_contest_status(self):
        return self.contest_status
