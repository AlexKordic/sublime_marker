import sublime, sublime_plugin

class ConstantizeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.run_command("upper_case")
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_")).translate(None, """()"'[]#$,.:/\\""")
			result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			self.view.replace(edit, selection, result)
		self.view.end_edit(edit)

class PythonListCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.run_command("upper_case")
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			_input = self.view.substr(selection)
			_parts = [repr(str(x)) for x in _input.split(" ") if x]
			result = ", ".join(_parts)
			self.view.replace(edit, selection, result)
		self.view.end_edit(edit)

# PROGRAM_END_TERMINATES_A_PROGRAM_STREAM

