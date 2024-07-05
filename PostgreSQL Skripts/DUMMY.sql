SET search_path TO cioban;

INSERT INTO job (job_name, job_description, degree)
VALUES 
('Software-Engineer', 'Entwickeln, testen und pflegen von Software', 'Informatik'),
('Data Analyst', 'Analysieren und interpretieren komplexer Datensätze', 'Wirtschaftsinformatik'),
('Web Developer', 'Entwerfen und implementieren von Webanwendungen', 'Informatik'),
('Database Administrator', 'Verwalten und pflegen von Datenbanksystemen', 'Informatik'),
('Project Manager', 'Planen, durchführen und überwachen von Projekten', 'Betriebswirtschaft'),
('UX-Designer', 'Gestalten benutzerfreundlicher Oberflächen', 'Grafikdesign'),
('Security Analyst', 'Umsetzen von Sicherheitsmaßnahmen und Protokollen', 'Informatik'),
('DevOps-Engineer', 'Arbeiten an Code-Veröffentlichungen und Bereitstellungen', 'Informatik'),
('IT-Manager', 'Überwachen von IT-Betriebsabläufen und treffen von strategische Entscheidungen', 'Wirtschaftsinformatik');


INSERT INTO skill (skill_name, skill_description)
VALUES 
('Python', 'Entwickelt in Python'),
('Java', 'Entwickelt in Java'),
('C++', 'Entwickelt in C++'),
('JavaScript', 'Entwickelt in JavaScript'),
('HTML/CSS', 'Entwickelt in HTML/CSS'),
('mySQL', 'Vertaut mit mySQL und Datenbankmanagement'),
('Projektmanagement', 'Vertaut mit Projektmanagement'),
('Datenanalyse', 'Vertaut mit dem Analysieren und Aufbereiten von Daten'),
('Machine Learning', 'Vertraut mit Machine Learning-Algorithmen'),
('Netzwerkmanagement', 'Vetraut mit dem Aufbau, der Wartung und dem Management von Netzwerken'),
('Cybersicherheit', 'Vertaut mit der Umsetzung von IT-Sicherheitsmaßnahmen'),
('Webentwicklung', 'Vertraut mit der Entwicklung von Webanwendungen'),
('UX Design', 'Vertraut mit Design von Benutzeroberflächen');

INSERT INTO address (company, street, house_number, postcode, city, country)
VALUES 
('Berliner Wasserbetriebe AöR', 'Neue Jüdenstraße', 1, 10179, 'Berlin', 'Deutschland'),
('Berliner Wasserbetriebe AöR', 'Fischerstraße', 29, 10317, 'Berlin', 'Deutschland'),
('Berliner Wasserbetriebe AöR', 'Hohenzollerndamm', 44, 10709, 'Berlin', 'Deutschland'),
('Microsoft Inc.', 'Microsoft Way', 1, 98052, 'Redmond', 'USA'),	
('Apple Inc.', 'Apple Park Way', 1, 95014, 'Cupertino', 'USA'),
('Vodafone Deutschland GmbH', 'Germaniastraße', 14, 12099, 'Berlin', 'Deutschland');

INSERT INTO experience_level (exp_lvl_description, years_of_experience)
VALUES 
('Entry Level', 0),
('Junior Level', 2),
('Mid Level', 8),
('Senior Level', 10),
('Leitend', 15);

INSERT INTO employee (first_name, last_name, free_fte, base_fte, e_mail, phone_number, entry_date, experience_level_ID, type_ID, address_ID)
VALUES 
('Malik', 'Khan', 0.1, 1, 'malik.khan@bwb.de', '+491234567890', '2022-01-01', 1, 3, 2),
('Aisha', 'Choudhury',0.2, 1, 'aisha.choudhury@bwb.de', '+499876543210', '2022-02-02', 1, 3, 2),
('Juan', 'Lopez', 0.5, 1, 'juan.lopez@bwb.de', '+491122334455', '2022-03-03', 1, 3, 2),
('Robert', 'Weber', 0.5, 1, 'robert.weber@bwb.de', '+492233445566', '2022-04-04', 1, 3, 2),
('Hasan', 'Dammann',0.6, 1, 'hasan.dammann@bwb.de', '+493344556677', '2022-05-05', 1, 3, 2),
('Jamal', 'Al-Farsi',0.2, 1, 'jamal.alfarsi@bwb.de', '+494455667788', '2022-06-06', 4, 2, 4),
('Zara', 'Ibrahimovic',0.7, 1, 'zara.ibrahimovic@bwb.de', '+495566778899', '2022-07-07', 5, 2, 4),
('Chen', 'Li',0.5, 1, 'chen.li@bwb.de', '+496677889900', '2022-08-08', 4, 2 ,5),
('Ahmed', 'El-Masry',0.3, 1, 'ahmed.elmasry@bwb.de', '+497788990011', '2022-09-09', 5, 2, 5),
('Elena', 'Ivanova',0.4 , 1, 'elena.ivanova@bwb.de', '+498899001122', '2022-10-10', 5, 2, 6),
('Ravi', 'Patel',0.6 , 1, 'ravi.patel@bwb.de', '+499900112233', '2022-11-11', 2, 1, 2),
('Isabella', 'Fernandez',0.45 , 1, 'isabella.fernandez@bwb.de', '+490011223344', '2022-12-12', 5, 1, 2),
('Jasmine', 'Nguyen',0.5 , 1, 'jasmine.nguyen@bwb.de', '+491122334455', '2023-01-01', 3, 1, 1),
('Ahmad', 'Abedi',0.3 , 1, 'ahmad.abedi@bwb.de', '+492233445566', '2023-02-02', 5, 1, 3),
('Sofia', 'Moreno',0.3 , 1, 'sofia.moreno@bwb.de', '+493344556677', '2023-03-03', 4, 1, 3),
('Tariq', 'Khalid',0.5 , 1, 'tariq.khalid@bwb.de', '+491234567899', '2023-04-04', 5, 1, 1),
('Yasmin', 'Akhtar',0.35 , 1, 'yasmin.akhtar@bwb.de', '+499876543298', '2023-05-05', 3, 1, 3),
('Dante', 'Rossi',0.25 , 1, 'dante.rossi@bwb.de', '+491122334466', '2023-06-06', 4, 1, 3),
('Sophie', 'Müller',0.15 , 1, 'sophie.mueller@bwb.de', '+491234567891', '2022-07-07', 1, 3, 2),
('Max', 'Schmidt',0.1 , 1, 'max.schmidt@bwb.de', '+499876543211', '2022-02-02', 1, 3, 2),
('Lina', 'Hofmann',0.4 , 1, 'lina.hofmann@bwb.de', '+491122334466', '2022-03-03', 1, 3, 2),
('Alex', 'Weiss',0.25 , 1, 'alex.weiss@bwb.de', '+492233445567', '2022-04-04', 1, 3, 2),
('Nina', 'Lehmann',0.25 , 1, 'nina.lehmann@bwb.de', '+493344556678', '2022-05-05', 1, 3, 2),
('Elias', 'Schulz',0.1 , 0.5, 'elias.schulz@bwb.de', '+494455667789', '2022-06-06', 4, 2, 4),
('Anna', 'Koch',0.4 , 0.5, 'anna.koch@bwb.de', '+495566778890', '2022-07-07', 5, 2, 4),
('Luca', 'Wagner',0.05 , 0.5, 'luca.wagner@bwb.de', '+496677889901', '2022-08-08', 4, 2 ,5),
('Liam', 'Bauer',0.1 , 0.5, 'liam.bauer@bwb.de', '+497788990012', '2022-09-09', 5, 2, 5),
('Maya', 'Müller',0.2 , 0.5, 'maya.mueller@bwb.de', '+498899001123', '2022-10-10', 5, 2, 6),
('Oliver', 'Schneider',0.4 , 0.75, 'oliver.schneider@bwb.de', '+499900112234', '2022-11-11', 2, 1, 2),
('Elena', 'Fischer',0.75 , 0.75, 'elena.fischer@bwb.de', '+490011223345', '2022-12-12', 5, 1, 2),
('Paul', 'Vogel',0.5 , 0.5, 'paul.vogel@bwb.de', '+491122334467', '2023-01-01', 3, 1, 1),
('Sophia', 'Klein',0.5 , 0.5, 'sophia.klein@bwb.de', '+492233445568', '2023-02-02', 5, 1, 3),
('Finn', 'Berg',0.5 , 0.5, 'finn.berg@bwb.de', '+493344556679', '2023-03-03', 4, 1, 3),
('Emma', 'Schmitt',0.25 , 0.25, 'emma.schmitt@bwb.de', '+491234567890', '2023-04-04', 5, 1, 1),
('Leon', 'Wagner',0.25 , 0.25, 'leon.wagner@bwb.de', '+499876543291', '2023-05-05', 3, 1, 3),
('Mia', 'Huber',0.4 , 0.8, 'mia.huber@bwb.de', '+491122334467', '2023-06-06', 4, 1, 3);

INSERT INTO department (dep_name, dep_description)
VALUES
  ('IT-Support', 'Bietet technische Unterstützung für Endbenutzer und löst IT-Probleme'),
  ('Netzbetrieb', 'Verwaltet und pflegt die Computernetzwerke der Organisation'),
  ('Softwareentwicklung', 'Konzentriert sich auf die Erstellung und Wartung von Softwareanwendungen'),
  ('IT-Backend', 'Server und Datenmanagement'),
  ('IT-Frontend', 'Softwarebetreuung, Wartung und Verwaltung'),
  ('IT-Sicherheit', 'Gewährleistet die Sicherheit der Computersysteme und Daten der Organisation'),
  ('IT-Projektmanagement', 'Überwacht die Planung und Durchführung von IT-Projekten'),
  ('Datenanalyse', 'Analysiert und interpretiert Daten zur Unterstützung von Geschäftsentscheidungen');


INSERT INTO project (department_ID, proj_name, proj_priority, proj_manager, needed_fte, current_fte, start_date, end_date)
VALUES 
(4, 'SAP 4/HANA', 'hoch', 7, 8, 8, '2022-01-01', '2025-06-30'),
(5, 'Microsoft 360', 'mittel', 2, 2, 6, '2022-02-01', '2024-08-31'),
(5, 'Microsoft Exchange', 'gering', 10, 3, 2, '2022-03-01', '2029-09-30'),
(4, 'Active Directory', 'hoch', 4, 3, 8, '2022-04-01', '2027-10-31'),
(3, 'IT-Service-Portal', 'niedrig', 8, 5, 10, '2022-05-01', '2035-11-30');


INSERT INTO team (project_ID, team_name, team_purpose)
VALUES 
(1, 'Entwicklung - SAP 4/HANA', 'Entwickelung neuer Funktionen'),
(1, 'Improvement - SAP 4/HANA', 'Verbesserung der Leistung'),
(1, 'Testing - SAP 4/HANA', 'Testen und Behebung von Fehlern'),
(1, 'Data Science - SAP 4/HANA', 'Datenbankmanagement, Datenanalyse und Datenaufbereitung'),
(2, 'Testing - Microsoft 360', 'Testen und Behebung von Fehlern'),
(2, 'Frontend - Microsoft 360', 'Kompatibilität herstellen, Standartsoftware anpassen'),
(3, 'Testing - Microsoft Exchange', 'Testen und Behebung von Fehlern'),
(3, 'Frontend- Microsoft Exchange', 'Kompatibilität herstellen, Standartsoftware anpassen'),
(4, 'Data Science - Active Directory', 'Datenbankmanagement, Datenanalyse und Datenaufbereitung'),
(4, 'Testing - Active Directory', 'Testen und Behebung von Fehlern'),
(4, 'Frontend - Active Directory', 'Kompatibilität herstellen, Standartsoftware anpassen'),
(5,'Design - IT-Service-Portal', 'Verbesserung und Design der Benutzeroberfläche'),
(5, 'Data Science - IT-Service-Portal', 'Datenbankmanagement, Datenanalyse und Datenaufbereitung'),
(5, 'Entwicklung - IT-Service-Portal', 'Entwickelung neuer Funktionen'),
(5, 'Improvement - IT-Service-Portal', 'Verbesserung der Leistung'),
(5, 'Testing - IT-Service-Portal', 'Testen und Behebung von Fehlern');



INSERT INTO connection_team_employee (team_ID, employee_ID, assigned_fte)
VALUES 
(1, 1, 0.9),
(1, 2, 0.8),
(2, 3, 0.5),
(2, 4, 0.5),
(3, 5, 0.4),
(3, 6, 0.8),
(4, 7, 0.3),
(4, 8, 0.5),
(5, 9, 0.7),
(6, 10, 0.6),
(7, 11, 0.4),
(8, 12,0.55),
(9, 13, 0.5),
(10, 14, 0.7),
(11, 15, 0.7),
(12, 16, 0.5),
(13, 17, 0.65),
(14, 18, 0.75),
(15, 19, 0.85),
(16, 20, 0.9),
(6, 21, 0.6),
(7, 22, 0.75),
(8, 23, 0.75),
(9, 24, 0.4),
(10, 25, 0.1),
(11, 26, 0.45),
(12, 27, 0.4),
(13, 28, 0.3),
(14, 29, 0.35),
(15, 30, 0),
(16, 36, 0.4);

INSERT INTO connection_education_skill (education_ID, skill_ID)
VALUES 
(1,1),
(1,2),
(1,6),
(1,7),
(1,8),
(1,9),
(1,10),
(1,11),
(2,7),
(2,8),
(2,9),
(2,10),
(2,11),
(3,1),
(3,2),
(3,3),
(3,4),
(3,5),
(3,6),
(3,10),
(3,11),
(3,12),
(4,9),
(4,10),
(4,11),
(4,12),
(4,13),
(5,2),
(5,4),
(5,5),
(5,10),
(5,12),
(5,13);

INSERT INTO connection_job_skill (job_ID, skill_ID)
VALUES 
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(2, 6),
(2, 8),
(2, 9),
(3, 4),
(3, 5),
(3, 12),
(3, 13),
(4, 6),
(5, 7),
(6, 12),
(6, 13),
(7, 1),
(7, 10),
(7, 11),
(8, 1),
(8, 2),
(8, 3),
(8, 4),
(8, 5),
(8, 7),
(9, 7);

INSERT INTO stat (employee_ID, education_ID, supervisor_ID)
VALUES
	(1,1,12),
	(2,2,14),
	(3,3,16),
	(4,4,30),
	(5,5,32),
	(19,1,34),
	(20,2,14),
	(21,3,16),
	(22,4,30),
	(23,5,12);
    
INSERT INTO external (employee_ID, job_ID, supervisor_ID)
VALUES
	(6,1,12),
	(7,2,14),
	(8,3,16),
	(9,4,30),
	(10,5,32),
	(24,6,34),
	(25,2,14),
	(27,3,16),
	(28,4,30);
    
INSERT INTO internal (employee_ID, job_ID, floor, room)
VALUES
	(11,2, 1, 465),
	(12,1, 3, 234),
    (13,3, 5, 678),
    (14,2, 7, 567),
    (15,4, 4, 456),
    (16,3, 3, 3456),
    (17,5, 2, 567),
    (18,6, 3, 586),
    (29,6, 6, 476),
    (30,4, 7, 35),
	(31,7, 8, 567),
	(32,5, 3, 356),
	(33,8, 2, 234),
	(34,6, 5,274),
	(35,9, 4, 848),
    (36,9, 4, 848);
    
SET search_path TO login;

INSERT INTO user_login (username, hashed_password) 
VALUES 
	('WI22', 'ecb79c5358a9d8596b62ba238e38822e8ec03d2a8177e0b99921eec4ff219304'),
	('Schmietendorf', 'bdd2da1e54dfda96dc0d3231eab93f7abc18c0c1e11805882830f3ec444f9654');
