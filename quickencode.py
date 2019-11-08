import sublime, sublime_plugin
import base64
import xml.dom.minidom


class DecimalToHexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			number = int(self.view.substr(selection))
			hexstring = hex(number)
			self.view.replace(edit, selection, hexstring)
		self.view.end_edit(edit)

class HexToDecimalCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			hexstring = str(self.view.substr(selection))
			decimal = str(int(hexstring, 16))
			self.view.replace(edit, selection, decimal)
		self.view.end_edit(edit)

class EncodeHexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.run_command("upper_case")
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			result = str(self.view.substr(selection))
			if (result.startswith("'") and result.endswith("'")) or (result.startswith('"') and result.endswith('"')):
				result = eval(result)
			self.view.replace(edit, selection, result.encode("hex"))
		self.view.end_edit(edit)

class DecodeHexCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			result = str(self.view.substr(selection))
			if (result.startswith("'") and result.endswith("'")) or (result.startswith('"') and result.endswith('"')):
				result = eval(result)
			self.view.replace(edit, selection, repr(result.decode("hex")))
		self.view.end_edit(edit)

class DecodeBase64Command(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			result = str(self.view.substr(selection))
			result = base64.b64decode(result)
			self.view.replace(edit, selection, result)
		self.view.end_edit(edit)

class EncodeBase64Command(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			# result = str(self.view.substr(selection).upper().replace("-", "_").replace(" ", "_").replace("<", "_").replace(">", "_")).translate(None, """()"'[]#$,.:/\\""")
			result = str(self.view.substr(selection))
			result = base64.b64encode(result)
			self.view.replace(edit, selection, result)
		self.view.end_edit(edit)

class PathToClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.set_clipboard(self.view.file_name())

class FilenameToClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
	   sublime.set_clipboard(os.path.basename(self.view.file_name()))

class FiledirToClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		branch, leaf = os.path.split(self.view.file_name())
		sublime.set_clipboard(branch)


class XmlPrettyPrintCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			xml_ = xml.dom.minidom.parseString(self.view.substr(selection))
			pretty_xml_as_string = xml_.toprettyxml()
			self.view.replace(edit, selection, pretty_xml_as_string)
		self.view.end_edit(edit)


class LineEndingWinToLinuxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			changed = self.view.substr(selection).replace("\r\n", "\n")
			self.view.replace(edit, selection, changed)
		self.view.end_edit(edit)

class LineEndingLinuxToWinCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		edit = self.view.begin_edit()
		selected_ranges = self.view.sel()
		for selection in selected_ranges:
			changed = self.view.substr(selection).replace("\n", "\r\n")
			self.view.replace(edit, selection, changed)
		self.view.end_edit(edit)


