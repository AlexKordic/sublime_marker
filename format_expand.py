import sublime, sublime_plugin

def expand(txt, open, close, indent=0):
	output, chars_parsed = [], 0
	while 1:
		open_index = txt.find(open, chars_parsed)
		close_index = txt.find(close, chars_parsed)
		if open_index >= 0 and open_index < close_index:
			# increase indent
			output.append(txt[chars_parsed:open_index])
			# output.append("\n") # break before {
			# output.append("\t" * indent)
			output.append(open)
			output.append("\n")
			indent += 1
			output.append("\t" * indent)

			chars_parsed = len(open) + open_index
			continue
		elif close_index >= 0:
			# decrease indent
			output.append(txt[chars_parsed:close_index])
			output.append("\n") # break before }
			indent -= 1
			output.append("\t" * indent)
			output.append(close)
			# output.append("\n")
			# output.append("\t" * indent)

			chars_parsed = len(close) + close_index
			continue
		else:
			# end
			output.append(txt[chars_parsed:])
			break
	return "".join(output)

class ExpandBracesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.run_command("upper_case")
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			result = str(self.view.substr(selection))
			self.view.replace(edit, selection, expand(result, "{", "}"))
		self.view.end_edit(edit)

class FormatSameParamsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			input_ = str(self.view.substr(selection))
			result = ", ".join(["{x}={x}".format(x=x.strip()) for x in input_.split(",")])
			self.view.replace(edit, selection, result)
		self.view.end_edit(edit)

