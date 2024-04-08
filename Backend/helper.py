from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Any, Dict
from ORM.mapper import Mapper
from ORM.tables import Employee, Department, ExperienceLevel, Job, Project, Skill


class Helper:

    async def universal_delete(model_instance, db: AsyncSession = Depends(Mapper.get_db_session), **conditions) -> None:

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
        
    async def universal_update(entity_class, db: AsyncSession, entity_id: int, update_data: dict):
        try:
            entity = await db.get(entity_class, entity_id)
            if not entity:
                return False 

            for key, value in update_data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            await db.commit()
            return True  
        except Exception as e:
            await db.rollback()
            raise e

    async def build_search_query(criteria: Dict[str, Any], session: AsyncSession) -> Any:
        query = select(Employee)

        for key, value in criteria.items():
            if key == "department" and value:
                query = query.join(Department).where(Department.dep_name == value)
            elif key == "job" and value:
                query = query.join(Employee.job).where(Job.job_name == value)  
            elif key == "experienceLevel" and value:
                query = query.join(ExperienceLevel).where(ExperienceLevel.exp_lvl_description == value)
            elif key == "project" and value:
                query = query.join(Employee.projects).where(Project.proj_name == value) 
            elif key == "skill" and value:
                query = query.join(Employee.skills).where(Skill.skill_name == value)  

        return query
