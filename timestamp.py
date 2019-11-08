
import pytz
import datetime
import sublime, sublime_plugin
from traceback import print_exc
from time import ctime
from math import floor

def toHHMMSS(seconds):
	sec_num = float(seconds)
	hours   = floor(sec_num / 3600.0)
	minutes = floor((sec_num - (hours * 3600.0)) / 60.0)
	seconds = sec_num - (hours * 3600.0) - (minutes * 60.0);

	if hours   < 10: 
		hours = "0" + str(int(hours))   
	else: 
		hours = str(int(hours))
	if minutes < 10: 
		minutes = "0" + str(int(minutes)) 
	else: 
		minutes = str(int(minutes))
	if seconds < 10: 
		seconds = "0" + str(seconds)
	else:
		seconds = str(seconds)
	return "{0}:{1}:{2}".format(hours, minutes, seconds)

class TimestampToDateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = int(self.view.substr(selection))
				except ValueError, e:
					# try float then
					x = float(self.view.substr(selection))
				# date = ctime(x / 1000.0)
				# pytz.utc.localize(datetime.datetime.fromtimestamp(time())).strftime('%Y-%m-%d %H:%M:%S.%f %Z')
				date = pytz.utc.localize(datetime.datetime.fromtimestamp(x / 1000.0)).strftime('%Y-%m-%d %H:%M:%S.%f %Z')
				self.view.replace(edit, selection, str(date))
			except:
				print_exc()
		self.view.end_edit(edit)

class SecondsToHoursMinutesSecondsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = int(self.view.substr(selection))
				except ValueError, e:
					# try float then
					x = float(self.view.substr(selection))
				date = toHHMMSS(x)
				self.view.replace(edit, selection, date)
			except:
				print_exc()
		self.view.end_edit(edit)

