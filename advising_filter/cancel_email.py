#!/usr/bin/python
# Barbara Hazlett
# CS 419 - Group 4
# Help sources:

import datetime
import smtplib

class email:
	def cancel(self, ad_email, lst, time_choice):
		sender = 'do.not.reply@engr.orst.edu'
				
		#start session and login
		session = smtplib.SMTP('engr.orst.edu')
		session.ehlo()
		session.starttls()
		session.ehlo
				
		#create body of email
		for appt in lst:
			#check for correct starttime
			if appt['starttime'].strftime('%H:%M') == time_choice:
				body, subject = "", ""
				subject = "Advising Signup Cancellation"
				body = "Advising Signup with " + appt['advisor_lname'] + ", " + appt['advisor_fname'] + " CANCELLED\n"
				body += "Name: " + appt['student_lname'] + ", " + appt['student_fname'] + "\n"
				body += "Email: " + appt['student_email'] + "\n"
				body += "Date: " + str(appt['starttime'].strftime("%A, %B %d, %Y")) + "\n"  
				body += "Time: " + appt['starttime'].strftime('%I:%M%p') + " - " + appt['endtime'].strftime('%I:%M%p')			
				body += "\n\n\nPlease contact support@engr.oregonstate.edu if you experience problems"
				body = "" + body + ""
				stu_email = appt['student_email']
			
		#create header
		receivers = [ad_email, stu_email]
		headers = ["From: " + sender,
			   "Subject: " + subject,
			   "To: " + ad_email + "," + stu_email,
			   "MIME-Version: 1.0",
			   "Content-Type: text/plain; charset=UTF-8"]
		headers = "\r\n".join(headers)
		 
		#send and quit
		session.sendmail(sender, receivers, headers + "\r\n\r\n" + body)	
		session.quit()		