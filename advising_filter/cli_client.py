#!/usr/bin/python
# Barbara Hazlett
# CS 419 - Group 4
# Help sources:
# https://docs.python.org/2/howto/curses.html
# https://www.youtube.com/watch?v=eN1eZtjLEnU
# https://github.com/thorups/CS419
# https://github.com/benHobbs/cs419
# http://stackoverflow.com/questions/860140/whoami-in-python
# http://stackoverflow.com/questions/53513/best-way-to-check-if-a-list-is-empty
# http://www.tutorialspoint.com/python/time_strptime.htm
# http://stackoverflow.com/questions/5749195/how-can-i-split-and-parse-a-string-in-python

# add other curses help stuff!

import curses
import calendar
import datetime
import database #program to connect to appointment database
import time
import getpass
import cancel_email 

#get current date (day and year)
now = datetime.datetime.now()

def move_down(cal_window, y_cal, x_cal):
	cal_window.move(y_cal+1,x_cal)			
	y_cal += 1	
	return y_cal, x_cal
	
def time_down(date_window, outer_window, y_date, x_date):
	outer_window.move(y_date +1, x_date)
	y_date += 1
	date_window.noutrefresh()
	return y_date, x_date
	
def move_up(cal_window, y_cal, x_cal):
	cal_window.move(y_cal-1,x_cal)			
	y_cal -= 1
	#cal_window.chgat(y_cal,x_cal,2,curses.A_REVERSE)  playing around with highlighting the current date
	return y_cal, x_cal
	
def time_up(date_window, outer_window, y_date, x_date):
	outer_window.move(y_date -1, x_date)
	y_date -= 1
	date_window.noutrefresh()
	return y_date, x_date
	
def move_right(cal_window, y_cal, x_cal):
	cal_window.move(y_cal,x_cal+3)			
	x_cal += 3
	return y_cal, x_cal
	
def move_left(cal_window, y_cal, x_cal):
	cal_window.move(y_cal,x_cal-3)			
	x_cal -= 3
	return y_cal, x_cal
	
def plus_month(month, year, cal_window):
	cal_window.erase()
	if (month+1) == 13:
		month = 01
		year += 1
		cal_window.addstr(0,0,calendar.month(year,month))
	else:
		cal_window.addstr(0,0,calendar.month(year,(month+1)))
		month += 1	
	cursor_nav(cal_window)
	return month, year
	
def minus_month(month, year, cal_window):
	cal_window.erase()
	if (month-1) == 0:
		month = 12
		year -= 1
		cal_window.addstr(0,0,calendar.month(year,month))
	else:
		cal_window.addstr(0,0,calendar.month(year,month-1))
		month -= 1
	cursor_nav(cal_window)
	return month, year

def toggle(cal_toggle, outer_window, date_window, cal_window):	
	if (cal_toggle):
		outer_window.move(6,6)
		date_window.noutrefresh()
		cal_toggle = False
	else:
		outer_window.move(7,48)
		cal_window.noutrefresh()
		cal_toggle = True
	return cal_toggle

def display_appt(date_window, cal_window, y_cal, x_cal, month, year, ad_email, lst, date_choice):	
	#get month and parse
	m_choice = cal_window.instr(0, 4, 9)
	m_choice = m_choice.strip()
	m_split = m_choice.split(" ")
	
	date_window.addstr(1,10, "                           ") #need a more elegant ways to clear a line - try clrtoel()
	date_window.addstr(1,10,(m_split[0] + " "  + date_choice + ", 20" + str(year))) 
	date_window.noutrefresh()
	
	#change date_choice format if needed
	date_choice = date_choice.strip()
	if int(date_choice) < 10:
		date_choice = "0" + date_choice
		
	#create date string
	date = "20" + str(year) + "-" + str(month) + "-" + date_choice
	#date_window.addstr(6,2, date)  #for debug
	
	#connect to database
	db = database.appt_db()
	db.connect()
	
	#get list of all appointments for date_choice and advisor that is logged in	
	lst = db.get(ad_email, date)
	db.close()
	
	#display appointments for selected date
	date_window.addstr(4,2, "                              ")  #again, need better way!!!!
	date_window.addstr(5,2, "                              ") 
	date_window.addstr(6,2, "                              ") 
	date_window.noutrefresh()
	
	row = 4
	if not lst:
		date_window.addstr(4,4, "No appointments found")
		date_window.noutrefresh()
	else:
		for appt in lst:
			start = appt['starttime'].strftime('%H:%M')
			end = appt['endtime'].strftime('%H:%M')										
			date_window.addstr(row,2,("- "+ str(start) + "->" + str(end) + " " + appt['student_lname'] + ", " + appt['student_fname']))
			date_window.noutrefresh()	
			row += 1
	return y_cal, x_cal, lst
	
def cancel_appt(outer_window, y_date, x_date, ad_email, lst):
	#grab starttime
	time_choice = outer_window.instr(y_date, x_date,5) 
	
	#display are you sure window and cancel/go back 
	cancel_win = curses.newwin(curses.LINES-20,curses.COLS-50,6,20)
	cancel_win.addstr(1,2,'Are you sure(y/n)?')
	cancel_win.border()
	cancel_win.refresh()
	
	#enable cursor and echo
	curses.curs_set(1)
	curses.echo()

	#get user response	
	cancel_val = cancel_win.getstr(1,20,1)	

	#disable cursor and echo
	curses.noecho()
	curses.curs_set(0)			
	
	if cancel_val == 'y' or cancel_val == 'Y':
		#get record and send plain text email
		can = cancel_email.email()
		can.cancel(ad_email, lst, time_choice)		
		cancel_win.addstr(2,2, "appt @ " + time_choice + " cancelled")		
		
	elif cancel_val == 'n' or cancel_val =='N':
		#go back to date and cal windows
		cancel_win.addstr(2,2, "ok, wait a sec...")	
		
	else:
		#error message and try again
		cancel_win.addstr(2,2,"please input y or n")
	
	cancel_win.refresh()
	time.sleep(3) 			
	cancel_win.erase()	
	cancel_win.noutrefresh()  
	
def cursor_nav(cal_window):
	cal_window.addstr(9,0,  "         kK       ")
	cal_window.addstr(10,0, "         /\       ")
	cal_window.addstr(11,0, "   hH <------> lL ") 
	cal_window.addstr(12,0, "         \/       ")
	cal_window.addstr(13,0, "         jJ       ")
	cal_window.noutrefresh()	
		
def main(screen):

	#get user name and convert to email
	email_name = getpass.getuser()
	ad_email = email_name + "@engr.orst.edu"
			
	#create curses screen
	stdscr = curses.initscr()

	#Properly initialize the screen
	curses.noecho()
	curses.cbreak()
	curses.curs_set(1)	

	#Check for and begin color support
	if curses.has_colors():
		curses.start_color()
		
	#Optionally enable the 
	#stdscr.keypad(1)

	#Initialize the color combinations we're going to use
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

	#Begin program
	heading = "   ADVISING APPOINTMENTS for " + email_name + "  "
	stdscr.addstr(heading, curses.A_REVERSE)
	stdscr.chgat(-1, curses.A_REVERSE)

	stdscr.addstr(curses.LINES-1, 0, "q Quit | t Toggle | d Display Appt | c Cancel Appt | p/m Plus/Minus Month")	
	
	#Change the Q to red
	stdscr.chgat(curses.LINES-1,0,1,curses.A_BOLD | curses.color_pair(1))

	#Set up main window
	outer_window = curses.newwin(curses.LINES-2,curses.COLS,1,0)

	#Create a date window 
	date_window = outer_window.subwin(curses.LINES-6,curses.COLS-42,3,2)
	date_window.addstr(1,10,now.strftime("%B %d, %Y"))	
	date_window.hline(2,2,"-",34)
	#date_window.addstr(8,2,str(pword))
	date_window.box()
	
	#Create a calendar window 
	cal_window = outer_window.subwin(curses.LINES-10,curses.COLS-50,6,47)
	#cal_window.box()
	year = int(now.strftime("%y"))
	month = now.month
	cal_window.addstr(calendar.month(year,month))
	outer_window.move(7,47)
	
	#create instructions for moving cursor
	cursor_nav(cal_window)
		
	#Initialize variables
	cal_toggle = True
	y_cal = 2
	x_cal = 0
	y_date = 6
	x_date = 6
	lst=[]
	
	#display today's appointments in date_window
	date_choice = now.strftime("%d")
	y_cal, x_cal, lst = display_appt(date_window, cal_window, y_cal, x_cal, month, year, ad_email, lst, date_choice)
	
	#Draw a border around the main window
	outer_window.box()

	#Update the internal window data structures
	stdscr.noutrefresh()	
	outer_window.noutrefresh()

	#Redraw the screen
	curses.doupdate()

	#Create the event loop
	while True:
		c = outer_window.getch()
		
		if c == ord('q') or c == ord('Q'): #end program			
			break
			
		elif c == ord('t') or c == ord('T'):  #toggle between windows
			cal_toggle = toggle(cal_toggle, outer_window, date_window, cal_window)
			y_cal = 2
			x_cal = 0	
			
		elif c == ord('d') or c == ord('D'):  #display appt
			date_choice = cal_window.instr(y_cal,x_cal,2)
			y_cal, x_cal, lst = display_appt(date_window, cal_window, y_cal, x_cal, month, year, ad_email, lst, date_choice)
			cal_window.move(y_cal, x_cal)
			
		elif c == ord('c') or c == ord('C'):  #cancel appt
			cancel_appt(outer_window, y_date, x_date, ad_email, lst)
			#restore screen
			curses.curs_set(1)
			cal_toggle == True
			y_cal, x_cal, lst = display_appt(date_window, cal_window, y_cal, x_cal, month, year, ad_email, lst, date_choice)				
			date_window.box()
			cal_window.addstr(0,0,calendar.month(year,month))
			outer_window.move(6,6)		
			date_window.noutrefresh()
			
		elif c == ord('j') or c == ord('J'):	#down 		
			if cal_toggle == True:
				if y_cal <= 6:
					y_cal, x_cal = move_down(cal_window, y_cal, x_cal)
			else:
				if y_date <= 8:
					y_date, x_date = time_down(date_window, outer_window, y_date, x_date)
				
		elif c == ord('k') or c == ord('K'):		#up
			if y_cal >= 1:
				if cal_toggle == True:
					y_cal, x_cal = move_up(cal_window, y_cal, x_cal)
				else:
					y_date, x_date = time_up(date_window, outer_window, y_date, x_date)
				
		elif c == ord('l') or c == ord('L'):    #right
			if (x_cal <= 16) and (cal_toggle == True):
				y_cal, x_cal = move_right(cal_window, y_cal, x_cal)
			
		elif c == ord('h') or c == ord('H'):    #left
			if x_cal >= 1:
				y_cal, x_cal = move_left(cal_window, y_cal, x_cal)
			
		elif c == ord('p') or c == ord('P'):  #advance one month
			month, year = plus_month(month, year, cal_window)	
			cal_window.move(y_cal, x_cal)
			
		elif c == ord('m') or c == ord('M'):  #go back one month
			month, year = minus_month(month, year, cal_window)
			cal_window.move(y_cal, x_cal)
			
		#Refresh the window from the bottom up
		#stdscr.noutrefresh()
		#outer_window.noutrefresh()
		cal_window.noutrefresh()
		#date_window.noutrefresh()  important not to enable this!
		curses.doupdate()

	#Restore the terminal settings
	curses.nocbreak()
	#stdscr.keypad(0)
	curses.echo()
	curses.curs_set(1)

	#Restore the terminal itself to its former state
	curses.endwin()

try:
	#Curses wrapper initalizes screen, etc
	curses.wrapper(main)
except KeyboardInterrupt:
    print "Got KeyboardInterrupt exception. Exiting..."
    exit() 