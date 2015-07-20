#!/usr/bin/python

import sys
import email
import os
import smtplib
import time
import datetime
import database
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import re

#sources:	http://stackoverflow.com/questions/4823574/sending-meeting-invitations-with-python
#			http://stackoverflow.com/questions/3744568/why-do-you-have-to-call-iteritems-when-iterating-over-a-dictionary-in-python
#			http://stackoverflow.com/questions/127803/how-to-parse-iso-formatted-date-in-python			
#------------------------------------------

#your sending email server
CONST_SERVER = 'mail.oregonstate.edu'
#your sending email port
CONST_PORT = 587
#sending email
CONST_SENDER = 'do.not.reply@engr.orst.edu'
#sending email's password
CONST_PW = ''
#sending email's first and last name
CONST_NAME = ''
#recipient email
CONST_RECIPIENT = ''
#path to email.txt log file
CONST_PATH = '/email.txt'

def main():
	#path for email logfile
	path = os.getcwd()	#gets current working directory
	path = os.path.dirname(path)
	path += '/advising_filter/mail'
	path += CONST_PATH	#adds current directory to const_path where file is located

	#Read from STDIN
	try:
		full_email = sys.stdin.read();
		msg = email.message_from_string(full_email.strip())
	except:
		full_email = "Error parsing email from stdin:  "
		full_email += str(datetime.now())

	#Parse raw email
	m_to = msg['To']
	m_subject = msg['Subject']
	m_body = body(full_email)
	m_student = student(m_body)
	m_advisor = advisor(m_body)
	m_st = get_starttime(m_body)
	m_et = get_endtime(m_body)
	m_from = student_email(m_body)
	m_student_fname, m_student_lname = find_flname(m_student)
	m_advisor_fname, m_advisor_lname = find_flname(m_advisor)

	#check if its a cancellation or request
	if m_subject.find("Advising Signup") > -1:
		if m_subject.find("Advising Signup Cancellation") > -1:
			m_action = "CANCELLED"

			#cancel the appointment and update database
			db = database.appt_db()
			db.connect()
			db.cancel(m_st.strftime("%Y-%m-%d %H-%M-%S")) #YYYY-MM-DD HH-MM-SS
			db.close()				

		else:
			m_action = "CONFIRMED"

			#dictionary for appointment content
			appointment = {
			#	'id' 			: row[0], <--auto incremented
				'student_fname' : m_student_fname,
				'student_lname'	: m_student_lname,
				'student_email' : m_from,
				'advisor_fname' : m_advisor_fname,
				'advisor_lname' : m_advisor_lname,
				'advisor_email' : m_to,
				'subject' 		: m_subject,
				'starttime' 	: m_st.strftime("%Y-%m-%d %H-%M-%S"),
				'endtime'		: m_et.strftime("%Y-%m-%d %H-%M-%S"),
				'description' 	: m_body,
				'status'		: m_action,
				'dateadded'		: datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
				}

			#add appointment to database
			db = database.appt_db()
			db.connect()
			db.put(appointment)	#saves library values to database
			db.close()		

		#Format and send appointment email
		send_appointment(m_subject, m_body, m_st, m_action, m_to, m_et, m_student_fname, m_student_lname, m_from)
	
	#Write email out to file for troubleshooting
	outfile = open(path, 'w')
	sys.stdout = outfile
	print full_email
	outfile.close()

def body(full_email):
	full_email = " ".join(full_email.split("\n"))
	full_email = full_email.split()
	body = ""
	record = False
	skip = 0
	#iterate through all words in email until "Advising", then return body
	for word in full_email:
		if word == "Advising":
			skip += 1
		if skip == 2:
			record = True
		if record == True:
			body += word + " "
		if word == "problems":
			break
	return body

def student(body_email):
	record = False
	name = ""
	body_email = body_email.split()
	#iterate through all words in email until "Name:", then return name of student
	for word in body_email:
		if record:
			name += word + " "
		if word == "Name:":
			record = True
	return name

def advisor(body_email):
	record = False
	name = ""
	body_email = body_email.split()
	#iterate through all words in email until "with", then return name of advisor
	for word in body_email:
		if record:
			name += word + " "
		if word == "with":
			record = True
	return name

def get_starttime(body_email):
	record_date = False
	record_date_cnt = 0
	record_time = False
	record_time_cnt = 0
	date_strp = ""
	time_strp = ""
	skip = 0
	body_email = body_email.split()
	for word in body_email:
		if record_date and record_date_cnt < 3:
			date_strp += word + " "
			record_date_cnt+=1
		if record_time and record_time_cnt < 1:
			time_strp += word + " "
			record_time_cnt+=1
		if skip == 1:
			record_date = True
		if word == "Date:":
			skip += 1
		if word == "Time:":
			record_time = True
	date_in = date_strp+time_strp
	date_in = re.sub(r"(st|nd|rd|th),", ",", date_in)
	try:
		dt = datetime.datetime.strptime(date_in, '%B %d, %Y %I:%M%p ')
	except:
		dt = datetime.datetime.strptime(date_in, '%B %d, %Y %H:%M%p ')
	return dt

def get_endtime(body_email):
	record_date = False
	record_date_cnt = 0
	record_time = False
	record_time_cnt = 0
	date_strp = ""
	time_strp = ""
	skip = 0
	body_email = body_email.split()
	for word in body_email:
		if record_date and record_date_cnt < 3:
			date_strp += word + " "
			record_date_cnt+=1
		if record_time and record_time_cnt < 1:
			time_strp += word + " "
			record_time_cnt+=1
		if skip == 1:
			record_date = True
		if word == "Date:":
			skip += 1
		if word == "-":
			record_time = True
	date_in = date_strp+time_strp
	date_in = re.sub(r"(st|nd|rd|th),", ",", date_in)
	try:
		dt = datetime.datetime.strptime(date_in, '%B %d, %Y %I:%M%p ')
	except:
		dt = datetime.datetime.strptime(date_in, '%B %d, %Y %H:%M%p ')
	return dt


def find_flname(person):
	person = " ".join(person.split(","))
	person = person.split()
	for i in range(len(person)):
		if i == 0:
			lastname = person[i]
		if i == 1:
			firstname = person[i]
			if len(person[i]) == 1:
				firstname = person[i + 1]
	return firstname, lastname
	
def student_email(body_email):
	record = False
	body_email = body_email.split()
	email = ""
	#iterate through all words in email until "Email:", then return student's email
	for word in body_email:
		if record:
			email += word
			break
		if word == "Email:":
			record = True
	return email
	
def send_appointment(subj, description, when, action, m_to, m_et, fname, lname, m_from):
	CRLF = "\r\n"
	login = CONST_SENDER
	password = CONST_PW
	attendees = [CONST_RECIPIENT]
	organizer = "ORGANIZER;CN="+CONST_SENDER+":mailto:"+CONST_SENDER
	fro = CONST_SENDER
	#dur = datetime.timedelta(minutes = 15)
	ddtstart = when
	dtend = m_et
	dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
	dtstart = ddtstart.strftime("%Y%m%dT%H%M%S")
	dtend = dtend.strftime("%Y%m%dT%H%M%S")
	dtsubj = ddtstart.strftime(" (%B %d, %Y %H:%M:%S)")
	emails = [m_to, m_from]
	
	if action == "CANCELLED":
		method = "CANCEL"
		sequence = str(1)
	else:
		method = "REQUEST"
		sequence = str(0)
	
	for e in emails:
		attendee = ""
		for att in attendees:
			att = CONST_RECIPIENT
		attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN=organizer;X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
		ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
		ical+="METHOD:"+method+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstart+CRLF+organizer+CRLF
		ical+= "UID:STDNTAPPT"+dtstart+fname+lname+CRLF
		ical+= attendee+"CREATED:"+dtstamp+CRLF+subj+CRLF+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:"+sequence+CRLF+"STATUS:"+action+CRLF
		ical+= "SUMMARY:"+subj+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF
		#ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
		#ical+= "SUMMARY:"+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

		eml_body = description
		eml_body_bin = description
		msg = MIMEMultipart('mixed')
		msg['Reply-To']=fro
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] =subj+dtsubj
		msg['From'] = fro
		msg['To'] = e

		part_email = MIMEText(eml_body,"html")
		if method == "CANCEL":
			part_cal = MIMEText(ical,'calendar;method=CANCEL')
		if method == "REQUEST":
			part_cal = MIMEText(ical,'calendar;method=REQUEST')

		msgAlternative = MIMEMultipart('alternative')
		msg.attach(msgAlternative)

		ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
		ical_atch.set_payload(ical)
		Encoders.encode_base64(ical_atch)
		ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

		eml_atch = MIMEBase('text/plain','')
		Encoders.encode_base64(eml_atch)
		eml_atch.add_header('Content-Transfer-Encoding', "")

		msgAlternative.attach(part_email)
		msgAlternative.attach(part_cal)

		mailServer = smtplib.SMTP('engr.orst.edu')
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		#mailServer.login(login, password)
		mailServer.sendmail(fro, e, msg.as_string())
		mailServer.close()

main()