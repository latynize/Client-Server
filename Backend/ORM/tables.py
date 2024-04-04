from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DoublePrecision, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Job(Base):
    __tablename__ = 'job'
    __table_args__ = {'schema': 'cioban'}
    
    job_id = Column(Integer, primary_key=True)
    job_name = Column(String(25))
    job_description = Column(String(200))
    degree = Column(String(25))

class Skill(Base):
    __tablename__ = 'skill'
    __table_args__ = {'schema': 'cioban'}
    
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String(25))
    skill_description = Column(String(200))

class EducationDegree(Base):
    __tablename__ = 'education_degree'
    __table_args__ = {'schema': 'cioban'}
    
    education_id = Column(Integer, primary_key=True)
    education_name = Column(String(50))

class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = {'schema': 'cioban'}
    
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    free_fte = Column(DoublePrecision)
    e_mail = Column(String(200))
    phone_number = Column(String(25))
    entry_date = Column(Date)
    experience_level_id = Column(Integer, ForeignKey('cioban.experience_level.experience_level_id'))
    type_id = Column(Integer, ForeignKey('cioban.type.type_id'))
    address_id = Column(Integer, ForeignKey('cioban.address.address_id'))
    
    # Relationships
    experience_level = relationship("ExperienceLevel", backref="employees")
    type = relationship("Type", backref="employees")
    address = relationship("Address", backref="employees")

class Type(Base):
    __tablename__ = 'type'
    __table_args__ = {'schema': 'cioban'}
    
    type_id = Column(Integer, primary_key=True)
    type_name = Column(String(25))
    type_description = Column(String(200))

class Internal(Base):
    __tablename__ = 'internal'
    __table_args__ = {'schema': 'cioban'}
    
    employee_id = Column(Integer, ForeignKey('cioban.employee.employee_id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('cioban.job.job_id'))
    floor = Column(Integer)
    room = Column(Integer)
    
    # Relationships
    employee = relationship("Employee", backref=backref("internal", uselist=False))
    job = relationship("Job", backref="internals")

class External(Base):
    __tablename__ = 'external'
    __table_args__ = {'schema': 'cioban'}
    
    employee_id = Column(Integer, ForeignKey('cioban.employee.employee_id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('cioban.job.job_id'))
    supervisor_id = Column(Integer, ForeignKey('cioban.employee.employee_id'))
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], backref="externals")
    supervisor = relationship("Employee", foreign_keys=[supervisor_id])

class Stat(Base):
    __tablename__ = 'stat'
    __table_args__ = {'schema': 'cioban'}
    
    employee_id = Column(Integer, ForeignKey('cioban.employee.employee_id'), primary_key=True)
    education_id = Column(Integer, ForeignKey('cioban.education_degree.education_id'))
    supervisor_id = Column(Integer, ForeignKey('cioban.employee.employee_id'))
    
    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id], backref="stats")
    education_degree = relationship("EducationDegree", backref="stats")
    supervisor = relationship("Employee", foreign_keys=[supervisor_id])

class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'cioban'}
    
    address_id = Column(Integer, primary_key=True)
    company = Column(String(200))
    street = Column(String(200))
    house_number = Column(Integer)
    postcode = Column(Integer)
    city = Column(String(50))
    country = Column(String(50))

class ExperienceLevel(Base):
    __tablename__ = 'experience_level'
    __table_args__ = {'schema': 'cioban'}
    
    experience_level_id = Column(Integer, primary_key=True)
    exp_lvl_description = Column(String(200))
    years_of_experience = Column(Integer)

class Team(Base):
    __tablename__ = 'team'
    __table_args__ = {'schema': 'cioban'}
    
    team_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('cioban.project.project_id'))
    team_name = Column(String(250))
    team_purpose = Column(String(200))
    
    # Relationships
    project = relationship("Project", backref="teams")

class Project(Base):
    __tablename__ = 'project'
    __table_args__ = {'schema': 'cioban'}
    
    project_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('cioban.department.department_id'))
    proj_name = Column(String(35))
    proj_priority = Column(String(15))
    proj_manager = Column(Integer, ForeignKey('cioban.employee.employee_id'))
    needed_fte = Column(DoublePrecision)
    current_fte = Column(DoublePrecision)
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Relationships
    department = relationship("Department", backref="projects")
    proj_manager_employee = relationship("Employee", backref="managed_projects")

class Department(Base):
    __tablename__ = 'department'
    __table_args__ = {'schema': 'cioban'}
    
    department_id = Column(Integer, primary_key=True)
    dep_name = Column(String(45))
    dep_description = Column(String(300))

class ConnectionJobSkill(Base):
    __tablename__ = 'connection_job_skill'
    __table_args__ = {'schema': 'cioban'}
    
    job_id = Column(Integer, ForeignKey('cioban.job.job_id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('cioban.skill.skill_id'), primary_key=True)

class ConnectionTeamEmployee(Base):
    __tablename__ = 'connection_team_employee'
    __table_args__ = {'schema': 'cioban'}
    
    team_id = Column(Integer, ForeignKey('cioban.team.team_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('cioban.employee.employee_id'), primary_key=True)

class ConnectionEducationSkill(Base):
    __tablename__ = 'connection_education_skill'
    __table_args__ = {'schema': 'cioban'}
    
    education_id = Column(Integer, ForeignKey('cioban.education_degree.education_id'), primary_key=True)
    skill_id = Column(Integer, ForeignKey('cioban.skill.skill_id'), primary_key=True)
