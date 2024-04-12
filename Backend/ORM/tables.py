from pydantic import BaseModel
from datetime import date
from typing import Optional


class JobBase(BaseModel):
    job_id: int
    job_name: str
    job_description: str
    degree: str


class SkillBase(BaseModel):
    skill_id: int
    skill_name: str
    skill_description: str


class EducationDegreeBase(BaseModel):
    education_id: int
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
    type_id: int
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
    address_id: int
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


class SearchCriteriaBase(BaseModel):
    department: Optional[str] = None
    job: Optional[str] = None
    experienceLevel: Optional[str] = None
    project: Optional[str] = None
    type: Optional[str] = None
    skill: Optional[str] = None
    fte: Optional[float] = None

class ConnectionTeamEmployeeBase(BaseModel):
    team_id: int
    employee_id: int

class User_LoginBase(BaseModel):
    username: str
    password: str

class TokenBase(BaseModel):
    access_token: str


class Job(JobBase):
    pass


class Skill(SkillBase):
    pass


class EducationDegree(EducationDegreeBase):
    pass


class Employee(EmployeeBase):
    pass


class Type(TypeBase):
    pass


class Internal(InternalBase):
    pass


class External(ExternalBase):
    pass


class Stat(StatBase):
    pass


class Address(AddressBase):
    pass


class ExperienceLevel(ExperienceLevelBase):
    pass


class Team(TeamBase):
    pass


class Project(ProjectBase):
    pass


class Department(DepartmentBase):
    pass

class ConnectionTeamEmployee(ConnectionTeamEmployeeBase):
    pass

class SearchCriteria(SearchCriteriaBase):
    pass    