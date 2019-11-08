
# http://superuser.com/questions/452189/how-can-i-filter-a-file-for-lines-containing-a-string-in-sublime-text-2

import sublime, sublime_plugin

def filter(view, e, needle):
	# get non-empty selections
	regions = [s for s in view.sel() if not s.empty()]

	# if there's no non-empty selection, filter the whole document
	if len(regions) == 0:
		regions = [ sublime.Region(0, view.size()) ]

	for region in reversed(regions):
		lines = view.split_by_newlines(region)

		for line in reversed(lines):
			if not needle in view.substr(line):
				view.erase(e, view.full_line(line))

class GrepCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		def done(needle):
			e = self.view.begin_edit()
			filter(self.view, e, needle)
			self.view.end_edit(e)

		cb = sublime.get_clipboard()
		sublime.active_window().show_input_panel("Filter file for lines containing: ", cb, done, None, None)
