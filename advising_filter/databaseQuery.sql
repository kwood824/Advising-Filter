CREATE TABLE appointment(
	id int AUTO_INCREMENT NOT NULL, 
	student_fname varchar(255) NOT NULL,
	student_lname varchar(255) NOT NULL,
	student_email varchar(255) NOT NULL, #from email
	advisor_fname varchar(255) NOT NULL, #to email
	advisor_lname varchar(255) NOT NULL,
	advisor_email varchar(255) NOT NULL,
	subject varchar(255) NOT NULL,
	starttime DATETIME NOT NULL,
	endtime DATETIME NOT NULL,
	description varchar(255) NOT NULL,
	status varchar(255) NOT NULL, #status flag for cancelled or confirmed
	PRIMARY KEY(id)
)Engine=InnoDB;