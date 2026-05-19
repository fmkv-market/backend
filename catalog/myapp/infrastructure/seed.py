import asyncio
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from myapp.infrastructure.models.categories import Categories
from myapp.infrastructure.models.goods import Goods


def _get_db_url() -> str:
    return (
        f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )

SEED_CATEGORIES = [
    {"id": 1, "title": "Фрукты и ягоды", "parent_id": None},
    {"id": 2, "title": "Овощи", "parent_id": None},
    {"id": 3, "title": "Молочное", "parent_id": None},
    {"id": 4, "title": "Хлеб и выпечка", "parent_id": None},
    {"id": 5, "title": "Напитки", "parent_id": None},
    {"id": 6, "title": "Мясо и птица", "parent_id": None},
    {"id": 7, "title": "Снеки и сладкое", "parent_id": None},
]

SEED_GOODS = [
    # Фрукты и ягоды
    {
        "title": "Яблоко Гала",
        "description": "Сладкое яблоко сорта Гала. Отличается насыщенным вкусом и приятным ароматом.",
        "weight": 0.18,
        "cost": 29.0,
        "composition": "Яблоко",
        "expiration_days": 60,
        "category_id": 1,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Банан",
        "description": "Спелый банан из Эквадора. Богат калием и природными сахарами.",
        "weight": 0.15,
        "cost": 19.0,
        "composition": "Банан",
        "expiration_days": 7,
        "category_id": 1,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Клубника 250г",
        "description": "Свежая клубника, собранная в сезон. Насыщенный сладко-кислый вкус.",
        "weight": 0.25,
        "cost": 249.0,
        "composition": "Клубника",
        "expiration_days": 3,
        "category_id": 1,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Виноград Кишмиш",
        "description": "Сладкий зелёный виноград без косточек.",
        "weight": 0.5,
        "cost": 189.0,
        "composition": "Виноград",
        "expiration_days": 14,
        "category_id": 1,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Лимон",
        "description": "Сочный лимон. Источник витамина C.",
        "weight": 0.12,
        "cost": 39.0,
        "composition": "Лимон",
        "expiration_days": 30,
        "category_id": 1,
        "small_img": None,
        "big_img": None,
    },
    # Овощи
    {
        "title": "Огурец",
        "description": "Свежий хрустящий огурец. Идеален для салатов и перекусов.",
        "weight": 0.2,
        "cost": 35.0,
        "composition": "Огурец",
        "expiration_days": 10,
        "category_id": 2,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Томат черри 250г",
        "description": "Маленькие сладкие томаты черри. Отлично подходят для салатов.",
        "weight": 0.25,
        "cost": 129.0,
        "composition": "Томаты черри",
        "expiration_days": 7,
        "category_id": 2,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Морковь",
        "description": "Сочная сладкая морковь. Богата бета-каротином.",
        "weight": 0.15,
        "cost": 22.0,
        "composition": "Морковь",
        "expiration_days": 30,
        "category_id": 2,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Картофель 1кг",
        "description": "Рассыпчатый картофель. Подходит для варки, запекания и жарки.",
        "weight": 1.0,
        "cost": 89.0,
        "composition": "Картофель",
        "expiration_days": 60,
        "category_id": 2,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Перец болгарский красный",
        "description": "Сочный сладкий перец. Источник витамина C.",
        "weight": 0.18,
        "cost": 59.0,
        "composition": "Перец болгарский",
        "expiration_days": 14,
        "category_id": 2,
        "small_img": None,
        "big_img": None,
    },
    # Молочное
    {
        "title": "Молоко 3,2% 1л",
        "description": "Пастеризованное цельное молоко. Мягкий натуральный вкус.",
        "weight": 1.03,
        "cost": 89.0,
        "composition": "Молоко пастеризованное",
        "expiration_days": 10,
        "category_id": 3,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Кефир 2,5% 500мл",
        "description": "Кефир с живыми бактериями. Полезен для пищеварения.",
        "weight": 0.5,
        "cost": 69.0,
        "composition": "Нормализованное молоко, закваска кефирных грибков",
        "expiration_days": 10,
        "category_id": 3,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Творог 5% 200г",
        "description": "Нежный творог средней жирности. Богат белком и кальцием.",
        "weight": 0.2,
        "cost": 99.0,
        "composition": "Молоко нормализованное, закваска",
        "expiration_days": 5,
        "category_id": 3,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Сыр Российский 200г",
        "description": "Полутвёрдый сыр с лёгким сливочным вкусом.",
        "weight": 0.2,
        "cost": 189.0,
        "composition": "Молоко нормализованное, соль, закваска, хлористый кальций",
        "expiration_days": 60,
        "category_id": 3,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Масло сливочное 82,5% 180г",
        "description": "Натуральное сливочное масло высшего качества.",
        "weight": 0.18,
        "cost": 159.0,
        "composition": "Сливки пастеризованные",
        "expiration_days": 30,
        "category_id": 3,
        "small_img": None,
        "big_img": None,
    },
    # Хлеб и выпечка
    {
        "title": "Хлеб Бородинский 350г",
        "description": "Тёмный ржаной хлеб с кориандром. Классика русской выпечки.",
        "weight": 0.35,
        "cost": 65.0,
        "composition": "Мука ржаная, вода, солод, соль, кориандр",
        "expiration_days": 5,
        "category_id": 4,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Батон нарезной 400г",
        "description": "Мягкий пшеничный батон. Удобно нарезан для бутербродов.",
        "weight": 0.4,
        "cost": 49.0,
        "composition": "Мука пшеничная, вода, дрожжи, соль, сахар",
        "expiration_days": 3,
        "category_id": 4,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Круассан с маслом",
        "description": "Слоёный круассан с нежным сливочным вкусом. Свежая выпечка.",
        "weight": 0.08,
        "cost": 89.0,
        "composition": "Мука, масло сливочное, яйцо, соль, дрожжи",
        "expiration_days": 2,
        "category_id": 4,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Лаваш тонкий",
        "description": "Тонкий армянский лаваш. Идеален для заворачивания.",
        "weight": 0.25,
        "cost": 55.0,
        "composition": "Мука пшеничная, вода, соль",
        "expiration_days": 7,
        "category_id": 4,
        "small_img": None,
        "big_img": None,
    },
    # Напитки
    {
        "title": "Вода питьевая 1,5л",
        "description": "Негазированная питьевая вода. Натуральная родниковая.",
        "weight": 1.5,
        "cost": 59.0,
        "composition": "Вода питьевая",
        "expiration_days": 365,
        "category_id": 5,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Сок апельсиновый 1л",
        "description": "Сок прямого отжима из спелых апельсинов. Без сахара.",
        "weight": 1.0,
        "cost": 149.0,
        "composition": "Сок апельсиновый восстановленный",
        "expiration_days": 12,
        "category_id": 5,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Кофе растворимый 150г",
        "description": "Сублимированный кофе. Насыщенный вкус и аромат.",
        "weight": 0.15,
        "cost": 389.0,
        "composition": "Кофе натуральный растворимый сублимированный",
        "expiration_days": 730,
        "category_id": 5,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Чай чёрный 25 пакетиков",
        "description": "Крупнолистовой чёрный чай. Богатый вкус и крепкий настой.",
        "weight": 0.05,
        "cost": 129.0,
        "composition": "Чай чёрный байховый",
        "expiration_days": 730,
        "category_id": 5,
        "small_img": None,
        "big_img": None,
    },
    # Мясо и птица
    {
        "title": "Куриная грудка 500г",
        "description": "Охлаждённое куриное филе. Диетический продукт с высоким содержанием белка.",
        "weight": 0.5,
        "cost": 249.0,
        "composition": "Грудка куриная охлаждённая",
        "expiration_days": 5,
        "category_id": 6,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Фарш говяжий 400г",
        "description": "Свежий говяжий фарш из мяса первого сорта.",
        "weight": 0.4,
        "cost": 319.0,
        "composition": "Говядина",
        "expiration_days": 3,
        "category_id": 6,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Сосиски молочные 450г",
        "description": "Нежные молочные сосиски из свинины и говядины.",
        "weight": 0.45,
        "cost": 219.0,
        "composition": "Свинина, говядина, вода, соль, специи",
        "expiration_days": 14,
        "category_id": 6,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Бекон копчёный 200г",
        "description": "Нарезанный копчёный бекон из свиной грудинки.",
        "weight": 0.2,
        "cost": 259.0,
        "composition": "Грудинка свиная, соль, специи, дым",
        "expiration_days": 20,
        "category_id": 6,
        "small_img": None,
        "big_img": None,
    },
    # Снеки и сладкое
    {
        "title": "Чипсы картофельные 150г",
        "description": "Хрустящие чипсы со вкусом сметаны и лука.",
        "weight": 0.15,
        "cost": 129.0,
        "composition": "Картофель, масло подсолнечное, соль, ароматизатор",
        "expiration_days": 90,
        "category_id": 7,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Шоколад тёмный 72% 100г",
        "description": "Горький шоколад с высоким содержанием какао.",
        "weight": 0.1,
        "cost": 149.0,
        "composition": "Какао тёртое, масло какао, сахар",
        "expiration_days": 365,
        "category_id": 7,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Орехи кешью 100г",
        "description": "Жареные орехи кешью без соли. Источник полезных жиров.",
        "weight": 0.1,
        "cost": 199.0,
        "composition": "Орехи кешью жареные",
        "expiration_days": 180,
        "category_id": 7,
        "small_img": None,
        "big_img": None,
    },
    {
        "title": "Йогурт клубничный 150г",
        "description": "Густой йогурт с натуральным клубничным джемом.",
        "weight": 0.15,
        "cost": 79.0,
        "composition": "Молоко, сливки, клубника, сахар, закваска",
        "expiration_days": 14,
        "category_id": 7,
        "small_img": None,
        "big_img": None,
    },
]


async def seed() -> None:
    engine = create_async_engine(_get_db_url())
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        result = await session.execute(select(Goods).limit(1))
        if result.scalar_one_or_none() is not None:
            print("[seed] Data already exists, skipping.")
            await engine.dispose()
            return

        for cat_data in SEED_CATEGORIES:
            session.add(Categories(**cat_data))
        await session.flush()

        for good_data in SEED_GOODS:
            session.add(Goods(**good_data))
        await session.commit()

        print(f"[seed] Inserted {len(SEED_CATEGORIES)} categories and {len(SEED_GOODS)} goods.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
