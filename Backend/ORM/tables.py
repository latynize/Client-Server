from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class JobBase(BaseModel):
    job_name: str
    job_description: str
    degree: str

class SkillBase(BaseModel):
    skill_name: str
    skill_description: str

class EducationDegreeBase(BaseModel):
    education_name: str

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    free_fte: float
    e_mail: str
    phone_number: str
    entry_date: date
    experience_level_id: int
    type_id: int
    address_id: int

class TypeBase(BaseModel):
    type_name: str
    type_description: str

class InternalBase(BaseModel):
    employee_id: int
    job_id: int
    floor: int
    room: int

class ExternalBase(BaseModel):
    employee_id: int
    job_id: int
    supervisor_id: int

class StatBase(BaseModel):
    employee_id: int
    education_id: int
    supervisor_id: int

class AddressBase(BaseModel):
    company: str
    street: str
    house_number: int
    postcode: int
    city: str
    country: str

class ExperienceLevelBase(BaseModel):
    exp_lvl_description: str
    years_of_experience: int

class TeamBase(BaseModel):
    project_id: int
    team_name: str
    team_purpose: str

class ProjectBase(BaseModel):
    department_id: int
    proj_name: str
    proj_priority: str
    proj_manager: int
    needed_fte: float
    current_fte: float
    start_date: date
    end_date: Optional[date]

class DepartmentBase(BaseModel):
    dep_name: str
    dep_description: str

class JobCreate(JobBase):
    pass

class SkillCreate(SkillBase):    
    pass

class EducationDegreeCreate(EducationDegreeBase):
    pass

class EmployeeCreate(EmployeeBase):
    pass

class TypeCreate(TypeBase):
    pass

class InternalCreate(InternalBase):
    pass

class ExternalCreate(ExternalBase):
    pass

class StatCreate(StatBase):
    pass

class AddressCreate(AddressBase):
    pass

class ExperienceLevelCreate(ExperienceLevelBase):
    pass

class TeamCreate(TeamBase):
    pass

class ProjectCreate(ProjectBase):
    pass

class DepartmentCreate(DepartmentBase):
    pass

