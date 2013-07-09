
import sublime, sublime_plugin

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


