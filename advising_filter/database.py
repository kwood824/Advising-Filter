#!/usr/bin/python	

import MySQLdb

#sources: 	http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python
#			https://docs.python.org/2/tutorial/datastructures.html#dictionaries
#			http://stackoverflow.com/questions/3294889/iterating-over-dictionaries-for-loops-in-python
#			http://stackoverflow.com/questions/3744568/why-do-you-have-to-call-iteritems-when-iterating-over-a-dictionary-in-python
#			http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html
#			http://downloads.mysql.com/docs/connector-python-en.a4.pdf
#			http://stackoverflow.com/questions/509211/explain-pythons-slice-notation

class appt_db:
	#database parameters
	def __init__(self):
		self.host = 'mysql.eecs.oregonstate.edu'
		self.user = 'cs419-g4'
		self.password = 'JH59tyapzvJx5EL3'
		self.database = 'cs419-g4'

	#connect to the database
	def connect(self):
		self.db = MySQLdb.connect(self.host, self.user, self.password, self.database)
		self.cur = self.db.cursor()	#create cursor object to execute queries

	#puts appointment in database
	def put(self, appointment):
		columns, values = "", "" #initialize column and values variables

		#iterate through the appointment dictionary of keys & values with appropriate MySQL syntax
		for key, value in appointment.iteritems():
			columns += key + ","
			values += value +"','"
		
		#print columns
		#print values
		#columns[:-1] iterates through array minus the last char ,
		#values[:-3] iterates through array minus the last chars ','
		insert_appt = "INSERT INTO appointment (" + columns[:-1] + ") VALUES ('" + values[:-3] + "')"
		self.cur.execute(insert_appt)
		self.db.commit()

	#get sorted list of appointments for specific advisor and date
	def get(self, ad_email, date):
		self.cur = self.db.cursor()
		self.cur.execute("SELECT * FROM appointment WHERE status = 'CONFIRMED' AND advisor_email = '"+ad_email+"' AND DATE(starttime) = '"+date+"' ORDER BY starttime ASC ") #modifying this to order by starttime
		lst = []
		for row in self.cur.fetchall():
			appointment = {
				'id' 			: row[0],
				'student_fname' : row[1],
				'student_lname'	: row[2],  #fixed error, was fname
				'student_email' : row[3],
				'advisor_fname' : row[4],
				'advisor_lname' : row[5],
				'advisor_email' : row[6],
				'subject' 		: row[7],
				'starttime' 	: row[8],
				'endtime'		: row[9],
				'description' 	: row[10],
				'status'		: row[11],
				'dateadded'		: row[12]
				}
			lst.append(appointment)
		return lst

	#cancels appointment at starttime
	def cancel(self, time):
		self.cur = self.db.cursor()
		self.cur.execute("UPDATE appointment SET status = 'CANCELLED' WHERE starttime = '"+time+"' ")
		self.db.commit()

	#close database connection
	def close(self):
		self.cur.close()
		self.db.close()