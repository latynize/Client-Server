SET search_path TO cioban;

-- projects and department
SELECT p.project_id, 
	p.proj_name, 
	d.dep_name, 
	p.proj_priority, 
	p.needed_fte, 
	p.current_fte, 
	p.start_date, 
	p.end_date
FROM project p
INNER JOIN department d ON p.department_id = d.department_id;

-- department
SELECT department_id, 
	dep_name, dep_description
FROM department;

-- exp level
SELECT experience_level_id, 
	exp_lvl_description, 
	years_of_experience
FROM experience_level;


-- addresses
SELECT address_id, 
	company, 
	house_number, 
	postcode, city, 
	country
FROM address;

-- external, job, supervisor
SELECT e.employee_id, 
	em.first_name, 
	em.last_name, 
	j.job_name, 
	em.free_fte, 
	s.first_name AS supervisor_first_name, 
	s.last_name AS supervisor_last_name
FROM external e
INNER JOIN employee em ON e.employee_id = em.employee_id
INNER JOIN job j ON e.job_id = j.job_id
INNER JOIN employee s ON e.supervisor_id = s.employee_id;

-- stat, education, supoervisor
SELECT s.employee_id, 
	em.first_name, 
	em.last_name, 
	ed.education_name, 
	em.free_fte, 
	sup.first_name AS supervisor_first_name, 
	sup.last_name AS supervisor_last_name
FROM stat s
INNER JOIN employee em ON s.employee_id = em.employee_id
INNER JOIN education_degree ed ON s.education_id = ed.education_id
INNER JOIN employee sup ON s.supervisor_id = sup.employee_id;

-- all employee with exp_lvl
SELECT em.employee_id, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	em.phone_number, 
	em.entry_date, 
	el.exp_lvl_description, 
	t.type_name
FROM employee em
INNER JOIN experience_level el ON em.experience_level_id = el.experience_level_id
INNER JOIN type t ON em.type_id = t.type_id;

-- project
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	experience_level.exp_lvl_description, 
	type.type_name, 
	project.proj_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
INNER JOIN connection_team_employee ON em.employee_ID = connection_team_employee.employee_ID
INNER JOIN team ON connection_team_employee.team_ID = team.team_ID
INNER JOIN project ON team.project_ID = project.project_ID
-- WHERE project.proj_name = 'Microsoft Exchange'; 

-- type
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	experience_level.exp_lvl_description, 
	type.type_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
-- WHERE type.type_name = 'Intern';

-- skill
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	experience_level.exp_lvl_description, 
	type.type_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
INNER JOIN internal ON em.employee_ID = internal.employee_ID
INNER JOIN job ON internal.job_ID = job.job_ID
INNER JOIN connection_job_skill ON job.job_ID = connection_job_skill.job_ID
INNER JOIN skill ON connection_job_skill.skill_ID = skill.skill_ID
WHERE skill.skill_name = 'Projektmanagement'
UNION
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	experience_level.exp_lvl_description, 
	type.type_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
INNER JOIN external ON em.employee_ID = external.employee_ID
INNER JOIN job ON external.job_ID = job.job_ID
INNER JOIN connection_job_skill ON job.job_ID = connection_job_skill.job_ID
INNER JOIN skill ON connection_job_skill.skill_ID = skill.skill_ID
WHERE skill.skill_name = 'Projektmanagement'
UNION
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
	em.free_fte, 
	em.e_mail, 
	experience_level.exp_lvl_description, 
	type.type_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
INNER JOIN stat ON em.employee_ID = stat.employee_ID 
INNER JOIN education_degree ON stat.education_ID = education_degree.education_ID
INNER JOIN connection_education_skill ON education_degree.education_ID = connection_education_skill.education_ID
INNER JOIN skill ON connection_education_skill.skill_ID = skill.skill_ID
WHERE skill.skill_name = 'Projektmanagement';

-- fte
SELECT em.employee_ID, 
	em.first_name, 
	em.last_name, 
    em.free_fte, 
    em.e_mail, 
    experience_level.exp_lvl_description, 
    type.type_name
FROM employee em
INNER JOIN experience_level ON em.experience_level_ID = experience_level.experience_level_ID
INNER JOIN type ON em.type_ID = type.type_ID
WHERE em.free_fte = 0.5;
