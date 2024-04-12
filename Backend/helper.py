from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ORM.mapper import Mapper as m


class Helper:

    @staticmethod
    async def universal_delete(model_instance, db: AsyncSession = Depends(m.get_db_session), **conditions) -> bool:
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

    async def universal_insert(model_instance, data: dict, db: AsyncSession = Depends(m.get_db_session)):
        new_entry = model_instance(**data)
        db.add(new_entry)
        try:
            await db.commit()
            await db.refresh(new_entry)
            return new_entry
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Error creating entry: {e}")
        
    async def universal_update(entity_class, db: AsyncSession, entity_id: int, update_data: List):
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