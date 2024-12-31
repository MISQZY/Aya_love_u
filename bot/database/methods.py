from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, UserConfig, Timezone, Weektype

async def user_exist(session: AsyncSession, telegram_id: int) -> bool:
    query = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return query.scalars().first() is not None

async def get_user(session: AsyncSession, telegram_id: int) -> User:
    if await user_exist(session, telegram_id):
        query = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return query.scalars().first()
    else:
        return None


async def add_user(session: AsyncSession, telegram_id: int, username: str, name:str,  timezone_id: int, weektype_id: int, diminutive_affectionate_list = None):
    user = User(
        telegram_id=telegram_id,
        username=username,
        name=name,
        diminutive_affectionate_list=diminutive_affectionate_list
    )

    config_user = UserConfig(
        time_zone_id=timezone_id, #TODO
        week_type_id=weektype_id #TODO
    )
    session.add(config_user)
    await session.commit()

    user.user_config_id = config_user.id

    session.add(user)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e

async def update_user(session: AsyncSession, telegram_id: int, username: str, name: str, timezone_id: int, weektype_id: int, diminutive_affectionate_list=None):
    user = await get_user(session, telegram_id)
    
    if user is not None:
        user.username = username
        user.name = name
        user.diminutive_affectionate_list = diminutive_affectionate_list

        try:
            await session.commit()

            if user.user_config_id:
                query = await session.execute(select(UserConfig).where(UserConfig.id == user.user_config_id))
                user_config = query.scalars().first()

                if user_config:
                    if user.user_config_id:
                        user_config.time_zone_id = timezone_id if timezone_id else user_config.time_zone_id
                        user_config.week_type_id = weektype_id if weektype_id else user_config.week_type_id
                        await session.commit()
                    else:
                        new_user_config = UserConfig(
                            time_zone_id=timezone_id,
                            week_type_id=weektype_id
                        )
                        session.add(new_user_config)
                        await session.commit()

                        user.user_config_id = new_user_config.id
                        await session.commit()
            else:
                new_user_config = UserConfig(
                    time_zone_id=timezone_id,
                    week_type_id=weektype_id
                )
                session.add(new_user_config)
                await session.commit()

                user.user_config_id = new_user_config.id
                await session.commit()

        except Exception as e:
            await session.rollback()
            raise e
    else:
        await add_user(session, telegram_id, username, name, timezone_id, weektype_id, diminutive_affectionate_list)


async def delete_user(session: AsyncSession, telegram_id: int) -> bool:
    user = await get_user(session, telegram_id)
    
    if user:
        try:
            if user.user_config_id:
                query = await session.execute(select(UserConfig).where(UserConfig.id == user.user_config_id))
                user_config = query.scalars().first()

                if user_config:
                    await session.delete(user_config)

            await session.delete(user)
            await session.commit()

            return True
        except Exception as e:
            await session.rollback()
            raise e
    else:
        return False


async def get_timezones(session: AsyncSession) -> dict:
    query = await session.execute(select(Timezone.id, Timezone.name))
    timezones = query.fetchall()

    timezone_dict = [{'id': timezone.id, 'name': timezone.name} for timezone in timezones]

    return timezone_dict

async def get_weektypes(session: AsyncSession) -> dict:
    query = await session.execute(select(Weektype.id, Weektype.name))
    weektypes = query.fetchall()

    weektype_dict =  [{'id': weektype.id, 'name': weektype.name} for weektype in weektypes]

    return weektype_dict
