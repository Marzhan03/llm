import DAL
import models
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


async def add_news(title, date, content, category_id, location_id, site_id, summarized_content, old_id):
    async with DAL.async_session() as session:
        async with session.begin():
            existing_category = await session.execute(select(models.Category).where(models.Category.id == category_id))
            existing_category = existing_category.scalar()

            if not existing_category:
                new_category = models.Category(id=category_id, name="Новая категория")  # Пример значений
                session.add(new_category)

            existing_location = await session.execute(select(models.Location).where(models.Location.id == location_id))
            existing_location = existing_location.scalar()

            if not existing_location:
                new_location = models.Location(id=location_id, name="Новая категория")  # Пример значений
                session.add(new_location)

            existing_site = await session.execute(select(models.Site).where(models.Site.id == site_id))
            existing_site = existing_site.scalar()

            if not existing_site:
                new_site = models.Site(id=site_id, name="Новая категория")  # Пример значений
                session.add(new_site)    
            

            date_formatted = datetime.strptime(date, "%Y-%m-%d").date()

            new_news = models.News(
                title=title,
                date=date_formatted,
                content=content,
                category_id=category_id,  # Пример значения для внешнего ключа
                location_id=location_id,  # Пример значения для внешнего ключа
                site_id=site_id,  # Пример значения для внешнего ключа
                summarized_content=summarized_content,
                old_id=old_id,
            
            )
            # await session.execute(insert(models.News).values(new_news))
            session.add(new_news)  # Добавление объекта в сессию
            session.commit()


# async def get_all_news():
#     async with DAL.session() as session:
#         async with session.begin():
#             news_list = await session.execute(select(models.News))
#             print("dfsdfsdafd",news_list.scalars().all())
            
#             return news_list.scalars().all()


async def get_news_by_id(news_id: int):
    query = DAL.news.select().where(DAL.news.c.id == news_id)
    return await DAL.database.fetch_one(query)


async def get_all_news(session: AsyncSession):
    result = await session.execute(select(models.News).where(models.News.is_read == False).limit(10))
    news_list = result.scalars().all()

    if news_list:
        news_ids = [record.id for record in news_list]
        update_query = (
            update(models.News)
            .where(models.News.id.in_(news_ids))
            .values(is_read=True)
        )
        await DAL.database.execute(update_query)
    return news_list
