from fastapi import FastAPI
from fastapi import Depends
import DAL, data_accessor
from request_worker import RequestWorker
import schedule
import time
import signal, uvicorn
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from generate import generation_config
from prompts.request_prompt import PROMPT
import DAL
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()
# generated_text = generation_config.openchat_generate(PROMPT)
# print("DDD:", generated_text)
# open_chat_model = generation_config.OpenChatModel()

# @app.get("/news/{news_id}")
# async def get_news(news_id: int):
#     await DAL.database.connect()
#     result = await data_accessor.get_all_news()
#     await DAL.database.disconnect()
#     return result

request_worker = RequestWorker()
async def parse_news():
    response = request_worker.parse_news(category_id=1, limit=10, offset=5)
    
    for news_object in response:
        title = news_object.get("title")
        id = news_object.get("id")
        date = news_object.get("date")
        content = news_object.get("content")
        category_id = news_object.get("category_id")
        location_id = news_object.get("location_id")
        site_id = news_object.get("site_id")
        summarized_content = open_chat_model.summarize_text(content)
        summarized_content = summarized_content.split("GPT4 Correct Assistant:", 1)[-1].strip()
        print("fdgFDGFD",summarized_content)

        await data_accessor.add_news(
            title,
            date,
            content,
            category_id,
            location_id,
            site_id,
            summarized_content,
            old_id=id,
        )



test_list = ["1"] * 10

@app.get("/news/")
async def get_news(session: AsyncSession = Depends(DAL.get_session)):
    await DAL.database.connect()
    result = await data_accessor.get_all_news(session)
    await DAL.database.disconnect()
    print(result)
    return result

# async def test():
#     await DAL.database.connect()
#     result = await data_accessor.get_all_news()
#     await DAL.database.disconnect()
#     print(result)
#     return result

@app.on_event('startup')
def init_data():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(parse_news, 'cron', second='*/5')
    # scheduler.start()

def graceful_shutdown(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000)
