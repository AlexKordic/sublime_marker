import sublime, sublime_plugin

class State:
	last_element_name = "div"

class WrapInDivCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel(
			"Wrap in element named",
			State.last_element_name, 
			self.on_done, 
			None, 
			None,
			)

	def on_done(self, name):
		print "name", name
		State.last_element_name = name
		# self.view.run_command("upper_case")
		edit = self.view.begin_edit()
		try:
			selected_ranges = self.view.sel()
			for selection in selected_ranges:
				# text = unicode(self.view.substr(selection), self.view.encoding())
				text = self.view.substr(selection)
				result = "<" + name + ">\n" + text + "\n</" + name + ">"
				self.view.replace(edit, selection, result)
		finally:
			self.view.end_edit(edit)


