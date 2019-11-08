
import sublime, sublime_plugin
from traceback import print_exc

class AddSumNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get non-empty selections
		selections = self.view.sel()
		tokens = [self.view.substr(x) for x in selections if not x.empty()]

		# if there's no non-empty selection, end
		if len(tokens) == 0:
			print "no selected numbers"
			return

		result = 0
		for number_in_text_form in tokens:
			try:
				num_str = str(number_in_text_form).strip()
				if not num_str: continue
				num = float(num_str)
				print "+", num
				result += num
			except:
				print " - ERR: failed to convers to num:", number_in_text_form
				print_exc()

		print "storing", result, "in clipboard"
		sublime.set_clipboard(str(result))

class IncrementNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel(
			"Increment selections by what number?",
			"", 
			self.on_done, 
			None, 
			None,
			)

	def on_done(self, increment_string):
		try:
			increment_value = int(increment_string)
		except ValueError, e:
			# try float then
			increment_value = float(increment_string)
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = int(self.view.substr(selection))
				except ValueError, e:
					# try float then
					x = float(self.view.substr(selection))
				x += increment_value
				self.view.replace(edit, selection, str(x))
			except:
				print_exc()
		self.view.end_edit(edit)


class MultiplyNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.window().show_input_panel(
			"Multiply selections by what number?",
			"", 
			self.on_done, 
			None, 
			None,
			)

	def on_done(self, increment_string):
		try:
			mul_value = int(increment_string)
		except ValueError, e:
			# try float then
			mul_value = float(increment_string)
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = int(self.view.substr(selection))
				except ValueError, e:
					# try float then
					x = float(self.view.substr(selection))
				x *= mul_value
				self.view.replace(edit, selection, str(x))
			except:
				print_exc()
		self.view.end_edit(edit)


class IncrementSequentiallyCommand(sublime_plugin.TextCommand):
	def run(self, edit): 
		self.view.window().show_input_panel(
			"Increment selections incrementially, what is starting offset?",
			"0", 
			self.on_done, 
			None, 
			None,
			)

	def on_done(self, increment_string):
		try:
			increment_value = int(increment_string)
		except ValueError, e:
			# try float then
			increment_value = float(increment_string)
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = int(self.view.substr(selection))
				except ValueError, e:
					# try float then
					x = float(self.view.substr(selection))
				x += increment_value
				self.view.replace(edit, selection, str(x))
				increment_value += 1
			except:
				print_exc()
		self.view.end_edit(edit)

class EvalExpressionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selections = self.view.sel()
		for selection in selections:
			try:
				try:
					x = eval(self.view.substr(selection))
					self.view.replace(edit, selection, str(x))
				except:
					print_exc()
			except:
				print_exc()
		self.view.end_edit(edit)



