import requests
import dotenv, os

dotenv.load_dotenv()

class RequestWorker:
    def __init__(self):
        self.BACKEND_URL = os.getenv("BACKEND_URL")

    def parse_news(self, category_id, limit, offset):
        response = requests.get(self.BACKEND_URL + "news/%s/%s/%s"%(category_id, limit, offset))

        return response.json()
