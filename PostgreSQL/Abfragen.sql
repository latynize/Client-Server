SELECT *
FROM cioban.department;

SELECT first_name, last_name, free_fte
FROM cioban.employee
WHERE last_name = 'Miller';

SELECT e.first_name, e.last_name, e.e_mail, el.exp_lvl_description
FROM cioban.employee e
INNER JOIN cioban.external ex ON ex.employee_id = e.employee_id
INNER JOIN cioban.experience_level el ON el.experience_level_id = e.experience_level_id
WHERE el.exp_lvl_description = 'Mid Level';

