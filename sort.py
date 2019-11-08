
import sublime, sublime_plugin


def overwrite_line(view, edit, line_start, entire_line_text):
	region = view.line(line_start)
	print "replacing {0} with {1}".format(region, entire_line_text)
	view.replace(edit, region, entire_line_text)

class TextLine(object):
	def __init__(self, region, view):
		self.region = region
		self.selected_number = float(view.substr(region))
		self.entire_line_text = view.substr( view.line(region) )
		self.original_line_start = view.line(region).begin()
		self.assigned_line_start = None

class SortSelectedCommand(sublime_plugin.TextCommand):
	""" Not supporting multiple lines selections !
	"""
	
	REVERSED = False

	def run(self, edit):
		print "Running ............"
		e = self.view.begin_edit()
		try:
			# get non-empty selections
			lines = []
			available_slots = []
			for selection in self.view.sel():
				line = TextLine(selection, self.view)
				# if line.original_line_start in available_slots:
				# 	print "skipping duplicate selection on line {0}".format(line.original_line_start)
				# 	continue
				lines.append(line)
				available_slots.append(line.original_line_start)

			# sort lines
			lines.sort(key=lambda x: x.selected_number, reverse=self.REVERSED)
			for index, line in enumerate(lines):
				line.assigned_line_start = available_slots[index]
			
			# sort by assigned_line_start reversed for replacing operation
			lines.sort(key=lambda x: x.assigned_line_start, reverse=True)

			for line in lines:
				overwrite_line(self.view, e, line.assigned_line_start, line.entire_line_text)

			# lines.reverse()
			# available_slots = list(available_slots)
			# available_slots.reverse()
			# write lines
			# for index, line_start in reversed(list(enumerate(available_slots))):
			# 	line = lines[index]
			# 	overwrite_line(self.view, e, line_start, line.entire_line_text)
		finally:
			self.view.end_edit(e)

class SortSelectedReversedCommand(SortSelectedCommand):
	REVERSED = True
