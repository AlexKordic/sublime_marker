
import sublime, sublime_plugin

class SelectToNextCommand(sublime_plugin.TextCommand):
	saved_pattern = ""
	def run(self, edit):
		# cb = sublime.get_clipboard()
		def done(pattern):
			self.saved_pattern = pattern
			# we take end of selection for start point in search
			existing_selections = [x for x in self.view.sel()]
			# resulting_selection = []
			e = self.view.begin_edit()
			self.view.sel().clear()
			for selection in existing_selections:
				found_selection = self.view.find(pattern, selection.b, sublime.LITERAL | sublime.IGNORECASE)
				if found_selection != None:
					# resulting_selection.append(found_selection)
					new_selection = sublime.Region(selection.a, found_selection.b)
					self.view.sel().add( new_selection )
					# print "added selection:", new_selection
			self.view.end_edit(e)
			# print "total selections:", self.view.sel()
		sublime.active_window().show_input_panel("select to next pattern: ", self.saved_pattern, done, None, None)


class MoveToNextCommand(sublime_plugin.TextCommand):
	"""
		a = [(467, 467), (478, 478)]
		[view.sel().add( sublime.Region(view.text_point(x[1], x[0])) ) for x in a]
		[sublime.Region(view.text_point(x[1], x[0])) for x in a]
		[view.text_point(x[1], x[0]) for x in a]
		[sublime.Region(x[0], x[1]) for x in a]

		
		[view.sel().add( sublime.Region(x[0], x[1]) ) for x in a]
		[x.b for x in view.sel()]
	"""
	saved_pattern = ""
	def run(self, edit):
		# cb = sublime.get_clipboard()
		def done(pattern):
			self.saved_pattern = pattern
			# we take end of selection for start point in search
			cursor_points = [x.b for x in self.view.sel()]
			# resulting_selection = []
			e = self.view.begin_edit()
			self.view.sel().clear()
			for point in cursor_points:
				region = self.view.find(pattern, point, sublime.LITERAL | sublime.IGNORECASE)
				if region != None:
					# resulting_selection.append(region)
					self.view.sel().add(region)
			self.view.end_edit(e)
		sublime.active_window().show_input_panel("move cursors to next pattern: ", self.saved_pattern, done, None, None)

class KeepEveryNthCursorCommand(sublime_plugin.TextCommand):
	"""
		From all existing cursor keep every nth starting from first.
	"""
	saved_number = 1
	def run(self, edit):
		# cb = sublime.get_clipboard()
		def done(number):
			self.saved_number = int(number)
			# we take end of selection for start point in search
			cursors_to_keep = []
			for index, selection in enumerate(self.view.sel()):
				if index % self.saved_number == 0:
					cursors_to_keep.append(selection)
			e = self.view.begin_edit()
			self.view.sel().clear()
			for selection in cursors_to_keep:
				self.view.sel().add(selection)
			self.view.end_edit(e)

		sublime.active_window().show_input_panel("Nth integer: ", str(self.saved_number), done, None, None)

