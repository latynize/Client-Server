import datetime
import os
import jwt
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ORM.mapper import Mapper as m


class Helper:
    SECRET_KEY = os.getenv("SECRET_KEY")

    @staticmethod
    async def universal_delete(model_instance, db, **conditions) -> bool:
        """
        Asynchrone Methode zum Löschen von Einträgen aus einer Datenbank basierend auf gegebenen Bedingungen.

        Args:
            model_instance: Das zu löschende Datenbankmodell.
            db (AsyncSession, optional): Die Datenbanksitzung. Standardmäßig Depends(m.get_db_session).
            **conditions: Bedingungen zur Bestimmung, welche Einträge zu löschen sind.

        Returns:
            bool: True, wenn das Löschen erfolgreich war, sonst False.
        """
        query = select(model_instance)
        for attr, value in conditions.items():
            query = query.filter(getattr(model_instance, attr) == value)

        results = await db.execute(query)
        instances = results.scalars().all()

        if not instances:
            return False

        for instance in instances:
            await db.delete(instance)

        await db.commit()
        return True

    @staticmethod
    async def universal_update(entity_class, db, entity_id, update_data) -> bool:
        """
        Klasse hat Entities
        Modell hat Instances
        """
        try:
            entity = await db.get(entity_class, entity_id)
            if not entity:
                return False

            for key, value in update_data:
                if hasattr(entity, key):
                    setattr(entity, key, value)

            await db.commit()
            return True
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    def create_jwt(username):
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        return jwt.encode(payload, Helper.SECRET_KEY, algorithm="HS256")
