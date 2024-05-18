import requests

SUBMISSIONS_API = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={unix_second}"


class AtCoderAPI:
    def get_submissions(user_id: str, unix_second: str):
        url = SUBMISSIONS_API.format(user_id=user_id, unix_second=unix_second)
        print(url)
        response = requests.get(url)
        print(response)
        return response.json()
