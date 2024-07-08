import datetime
import os
import jwt
from sqlalchemy.future import select


# This module provides the Helper class, which contains static methods that are needed in multiple modules of the
# main module.

class Helper:
    # The secret key for the JWT encoding.
    SECRET_KEY = os.getenv("SECRET_KEY")

    @staticmethod
    async def universal_delete(model_instance, db, **conditions) -> bool:
        """
        Deletes the instances of the given model that match the given conditions.
        :param model_instance: The model instance to delete.
        :param db: The database session.
        :param conditions: The conditions to match.
        :return: bool: True if the instances were deleted, False otherwise.
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
    async def universal_update(model_instance, db, entity_id, update_data) -> bool:
        """
        Updates the instance of the given model by the given ID based on the given data.
        :param model_instance: The model instance to update.
        :param db: The database session.
        :param entity_id: The ID of the entity to update.
        :param update_data: The data to update.
        :return: bool: True if the instance was successfully updated, False otherwise.
        """
        try:
            entity = await db.get(model_instance, entity_id)
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
    async def calculate_employee_fte(Employee, employee_id, assigned_fte, operation ,db) -> float:

        employee_fte = await db.execute(select(
            Employee.free_fte,
            Employee.base_fte)
        .filter(Employee.employee_id == employee_id)
        )

        for employee_fte_row in employee_fte.mappings().all():
            if operation == "add":
                new_free_fte = employee_fte_row.free_fte - assigned_fte
                if not new_free_fte >= 0:
                    raise Exception ("Free FTE is below zero")
            elif operation == "delete":
                new_free_fte = employee_fte_row.free_fte + assigned_fte
                if not new_free_fte <= employee_fte_row.base_fte:
                    raise Exception ("Free FTE is over one")
                
            return new_free_fte
        
    @staticmethod
    async def calculate_project_fte(Project, project_id, assigned_fte, operation, db) -> float:

        project_fte = await db.execute(select(
            Project.needed_fte,
            Project.current_fte)
        .filter(Project.project_id == project_id)
        )

        for project_fte_row in project_fte.mappings().all():
            if operation == "add":
                new_current_fte = project_fte_row.current_fte + assigned_fte
                if new_current_fte > project_fte_row.needed_fte:
                    raise Exception ("Current Project FTE is larger then FTE's needed")
            elif operation == "delete":
                new_current_fte = project_fte_row.current_fte - assigned_fte
                if not new_current_fte >= 0:
                    raise Exception ("Current Project FTE is below zero")
                
        return new_current_fte
        
    @staticmethod 
    async def check_fte_employee(employee_data, new_base_fte) -> bool:

        assigned_fte = employee_data.base_fte - employee_data.free_fte

        if not new_base_fte >= assigned_fte:
            return False
        
        else:
            return True
    
    @staticmethod
    async def check_fte_project(project_data, new_fte) -> bool:
        return bool

    @staticmethod
    def create_jwt(username) -> str:
        """
        Creates a JWT token for the given username.
        :param username: The username to create the token for.
        :return: str: The JWT token.
        """
        payload = {
            "username": username,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=30)
        }

        return jwt.encode(payload, Helper.SECRET_KEY, algorithm="HS256")
