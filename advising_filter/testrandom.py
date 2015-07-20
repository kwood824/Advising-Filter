#!/usr/bin/python

import random
import datetime
import smtplib
import time
#------------------------------------------
#sources:	
#		https://docs.python.org/2/library/smtplib.html
#		https://docs.python.org/2/library/random.html
#		http://stackoverflow.com/questions/4479800/python-generate-dates-series
#		https://github.com/benHobbs/cs419
#------------------------------------------

#Generates random emails
def Mail_Test(appt):
	server = 'mail.oregonstate.edu'
	port = 587
	sender = 'do.not.reply@engr.orst.edu'	
	password = ''
	recipient = 'woodky@engr.orst.edu'

	body = ""
	subject = ""

	if appt['status'] == "Signup":
		print "Test pass - Signup"
		subject = "Advising Signup with " + appt["a_last_name"] + ", " + appt["a_first_name"] + " " + appt["a_middle_name"] + " confirmed for " + appt["s_last_name"] + ", " + appt["s_first_name"] + " " + appt["s_middle_name"]
		body = "Advising Signup with " + appt["a_last_name"] + ", " + appt["a_first_name"] + " " + appt["a_middle_name"] + " confirmed\n"
	elif appt['status'] == "Cancelled":
		print "Test pass - Cancelled"
		subject = 'Advising Signup Cancellation'
		body = "Advising Signup with " + appt["a_last_name"] + ", " + appt["a_first_name"] + " " + appt["a_middle_name"] + " CANCELLED\n"
	else:
		print "Test Fail"
		subject = 'Test error'
		body = "Test error"
	body += "Name: " + appt["s_last_name"] + ", " + appt["s_first_name"] + " " + appt["s_middle_name"]+"\n"
	body += "Email: kwood824@gmail.com\n"
	body += "Date: " + str(appt['date'].strftime("%A, %B %d, %Y")) + "\n"
	body += "Time: " + str(appt['date'].strftime("%I:%M%p")) + " - "
	end_time = appt['end_time']
	body += str(end_time.strftime("%I:%M%p"))
	body += "\n\n\nPlease contact support@engr.oregonstate.edu if you experience problems"
	body = "" + body + ""

	headers = ["From: " + sender,
           "Subject: " + subject,
           "To: " + recipient,
           "MIME-Version: 1.0",
           "Content-Type: text/plain"]
	headers = "\r\n".join(headers)
 
	session = smtplib.SMTP(server)
 
	session.ehlo()
	session.starttls()
	session.ehlo
	#session.login(sender, password)
 
	session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
	session.quit()

#generates a date and time
def generate_dates(start_date, end_date):
    td = datetime.timedelta(hours=24)
    current_date = start_date
    lst = []
    while current_date <= end_date:
        lst.append(current_date)
        current_date += td
    return lst

def get_flname(person):
	#finds first and last name of person
	for i in range(len(person)):
		if i == 0:
			first_name = person[i]
		if i == 1:
			last_name = person[i]
	return first_name, last_name

def get_fullname(person):
	#finds first, middle, and last name of person
	for i in range(len(person)):
		if i == 0:
			first_name = person[i]
		if i == 1:
			middle_name = person[i]
		if i == 2:
			last_name = person[i]
	return first_name, middle_name, last_name

lst = []

#used random name generator from http://random-name-generator.info/ for 50 names
for i in range(1,2):
	#chooses random name from array of elements
	sname = random.choice(["Rochelle D Morgan", "M Ada Perry", "Salvatore T Lindsey", "Tim Reynolds", "Jimmie Nguyen", "Julian Henry", "T Sophie Maldonado", "D Terrence Vaughn", "M Candice Davis", "Connie T Harris", "Shannon Joelle Hart", "Pedro T Shaw", "Emanuel Manning", "Chelsea Barton", "Justin Boyd", "Natalie Dean", "Peggy Bradley", "Jerome Pearson", "Brendan E Ellis", "Taylor Willis", "Joe Gray", "Carol Wright", "Amanda A Alvarado","Nina Young", "Paula Campbell", "Michelle Fitzgerald", "Gordon Washington", "Greg Rivera", "Walter W Newman", "Olive Erickson", "Nathan Ramos", "Kyle D Pearson", "Reginald Gutierrez", "Juan Taco Santiago", "Phillip Bryan", "Jermaine Owen", "T Tomas Barnett", "Angelo M Malone", "D Kirk Moody", "Rogelio G Vaughn", "Lola Wagner", "Margie Lane", "Floyd Saunders", "Camille Poole", "Ernestine Stokes", "Luz Harvey", "Rosie Anne Olson", "Brent Garza", "Bradley Jon Yates", "Alberta Pittman"])
	student = sname.split()

	if len(student) == 2:
		s_first_name, s_last_name = get_flname(student)
		s_middle_name = ""
	else:
		s_first_name, s_middle_name, s_last_name = get_fullname(student)

	aname = random.choice(["Catherine T Owen", "Priscilla Simpson", "D Warren Phelps", "Darrell Mckenzie", "April C Blair", "T Ricardo Harrison", "Ernestine Hammond", "Nicholas C Bryant", "T Lynette Larson", "Genevieve Logan", "Jerome Allen", "Mae Anne Robinson", "Cynthia M Miller", "T Anthony Mccarthy", "Linda Dennis", "Mildres M Moss", "Harry Gibson", "Bryan Collins", "K Jared Waters", "Kelvin Ross", "Jodi Joelle Cortez", "Angelica Robertson", "T Lorraine Conner", "Daryl Underwood", "P Joe Patton", "Betty Crawford", "Jacob Jan Elliot", "Gretchen Mccormick", "Myra T Banks", "M Rita Hale", "Casey Yates", "Kathy Sio Campbell", "Rodolfo V Horton", "Flora Fields", "James P Saunders", "Adrienne Sanders", "Isaac Vi Nguyen", "T Kay Francis", "Floyd Curtis", "Howard Hodges", "Jennifer J Hughes", "L Luther Griffin", "Willie Silva", "Eduardo Duncan", "Blanche Townsend", "Joann Hicks", "Judy Parks"])
	advisor = aname.split()

	if len(advisor) == 2:
		a_first_name, a_last_name = get_flname(advisor)
		a_middle_name = ""
	else:
		a_first_name, a_middle_name, a_last_name = get_fullname(advisor)

	start_date = datetime.date(2015, 3, 20)
	end_date = datetime.date(2015, 8, 31)

	#choose random datetime anywhere from start_date to end_date
	appt_date = datetime.datetime.combine(random.choice(generate_dates(start_date, end_date)), datetime.time(random.choice(range(8,17)), random.choice([00,15,30,45])))
	
	#add random duration of appointment
	end1 = appt_date + datetime.timedelta(minutes = 10)
	end2 = appt_date + datetime.timedelta(minutes = 15)
	end3 = appt_date + datetime.timedelta(minutes = 20)
	end4 = appt_date + datetime.timedelta(minutes = 25)
	end5 = appt_date + datetime.timedelta(minutes = 30)
	end6 = appt_date + datetime.timedelta(minutes = 35)
	end7 = appt_date + datetime.timedelta(minutes = 40)
	end8 = appt_date + datetime.timedelta(minutes = 45)
	end9 = appt_date + datetime.timedelta(minutes = 50)
	end10 = appt_date + datetime.timedelta(minutes = 55)
	end11 = appt_date + datetime.timedelta(minutes = 60)
	end12 = appt_date + datetime.timedelta(minutes = 75)
	end13 = appt_date + datetime.timedelta(minutes = 90)
	end14 = appt_date + datetime.timedelta(minutes = 120)

	appt_end = random.choice([end1, end2, end3, end4, end5, end6, end7, end8, end9, end10, end11, end12, end13, end14])

	status = "Signup"

	#adds appointment to library of the random appointments
	appointment = {
		"s_first_name"	:	s_first_name,
		"s_last_name"	:	s_last_name,
		"s_middle_name"	:	s_middle_name,
		"a_first_name"	:	a_first_name,
		"a_last_name"	:	a_last_name,
		"a_middle_name"	:	a_middle_name,
		"status" 		: 	status,
		"date"			:	appt_date,
		"end_time"		:	appt_end,
	}

	#list the library to check if all appointments were emailed
	lst.append(appointment)

	#email all the tests to the recipient
	Mail_Test(appointment)

	#to prevent 20 emails coming all at once
	time.sleep(1)

print lst