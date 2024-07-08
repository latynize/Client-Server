-- Drop Schema
DROP SCHEMA IF EXISTS cioban CASCADE;
DROP SCHEMA IF EXISTS login CASCADE;

-- Create the schema
CREATE SCHEMA cioban;

-- Set the search path to the new schema
SET search_path TO cioban;

-- Create the tables
CREATE TABLE job (
    job_id SERIAL PRIMARY KEY,
    job_name VARCHAR(25),
    job_description VARCHAR(200),
    degree VARCHAR(25)
);

CREATE TABLE skill (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(25),
    skill_description VARCHAR(200)
);

CREATE TABLE education_degree (
    education_id SERIAL PRIMARY KEY,
    education_name VARCHAR(50)
);

CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(200), 
    last_name VARCHAR(200),
    base_fte DOUBLE PRECISION,
    free_fte DOUBLE PRECISION,
    e_mail VARCHAR(200),
    phone_number VARCHAR(25), 
    entry_date DATE,
    experience_level_id INT,
    type_id INT,
    address_id INT
);

CREATE TABLE type (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(25),
    type_description VARCHAR(200)
);

CREATE TABLE internal (
    employee_id INT REFERENCES employee(employee_id) ON DELETE CASCADE,
    job_id INT REFERENCES job(job_id) ON DELETE CASCADE,
    floor INT,
    room INT,
    PRIMARY KEY (employee_id)
);

CREATE TABLE external (
    employee_id INT REFERENCES employee(employee_id) ON DELETE CASCADE,
    job_id INT REFERENCES job(job_id) ON DELETE CASCADE,
    supervisor_id INT REFERENCES employee(employee_id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id)
);

CREATE TABLE stat (
    employee_id INT REFERENCES employee(employee_id) ON DELETE CASCADE,
    education_id INT REFERENCES education_degree(education_id) ON DELETE CASCADE,
    supervisor_id INT REFERENCES employee(employee_id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id)
);

CREATE TABLE address (
    address_id SERIAL PRIMARY KEY,
    company VARCHAR(200),
    street VARCHAR(200),
    house_number INT,
    postcode INT,
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE experience_level (
    experience_level_id SERIAL PRIMARY KEY,
    exp_lvl_description VARCHAR(200), 
    years_of_experience INT
);

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    dep_name VARCHAR(45),
    dep_description VARCHAR(300)
);

CREATE TABLE project (
    project_id SERIAL PRIMARY KEY,
    department_id INT,
    proj_name VARCHAR(35),
    proj_priority VARCHAR(15),
    proj_manager INT,
    needed_fte DOUBLE PRECISION,
    current_fte DOUBLE PRECISION,
    start_date DATE,
    end_date DATE
);

CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    project_id INT,
    team_name VARCHAR(250),
    team_purpose VARCHAR(200)
	FOREIGN KEY (project_id) REFERENCES project(project_id) ON DELETE CASCADE;
);

CREATE TABLE connection_job_skill (
	cjs SERIAL PRIMARY KEY,
    job_id INT,
    skill_id INT,
    FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id) ON DELETE CASCADE
);

CREATE TABLE connection_team_employee (
	cte_id SERIAL PRIMARY KEY,
    team_id INT,
    employee_id INT,
    assigned_fte DOUBLE PRECISION,
	FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

CREATE TABLE connection_education_skill (
	ces_id SERIAL PRIMARY KEY,
    education_id INT,
    skill_id INT,
    FOREIGN KEY (education_id) REFERENCES education_degree(education_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(skill_id) ON DELETE CASCADE
);

-- Add foreign key constraints to previously created tables
ALTER TABLE employee
ADD CONSTRAINT experience_level FOREIGN KEY (experience_level_id) REFERENCES experience_level(experience_level_id) ON DELETE CASCADE,
ADD CONSTRAINT type FOREIGN KEY (type_id) REFERENCES type(type_id) ON DELETE CASCADE, 
ADD CONSTRAINT address FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE CASCADE;

-- Insert initial data
INSERT INTO type (type_name, type_description) VALUES
('Intern', 'interne*r Mitarbeiter*in'),
('Extern', 'externe*r Mitarbeiter*in'),
('StudZubi', 'Auszubildende und Studierende');

INSERT INTO education_degree (education_name) VALUES
('Wirtschaftsinformatik B.A.'),
('Wirtschaftsinformatik M.A.'),
('Informatik B.A.'),
('Informatik M.A.'),
('IT-Ausbildung');

-- Create the schema
CREATE SCHEMA login;

-- Set the search path to the new schema
SET search_path TO login;

CREATE TABLE user_login (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

