import sublime, sublime_plugin

import os
import sys
import pysqlite2.dbapi2 as sqlite3
from collections import defaultdict

# This is incremented with change of schema
_version_ = 1


# sublime.set_clipboard(view.syntax_name(view.sel()[0].b))

def execute_statements(conn, statements):
	c = conn.cursor()
	for statement in statements:
		c.execute(statement)


class Item(object):
	"Intended to be immutable to work with set() container"
	__slots__ = ("selection_name", "token")
	def __init__(self, selection_name, token):
		self.selection_name, self.token = selection_name, token
	def __hash__(self):
		ret = hash((self.selection_name, self.token))
		# print "hash returning", ret, self
		return ret
	def __eq__(self, other):
		# print "__eq__", self, other
		return self.selection_name == other.selection_name and self.token == other.token
	def __str__(self):
		return "{0}, {1}".format(self.selection_name, self.token)
	__repr__ = __str__

class HighlightState(object):
	SELECTION_NAME_PREFIX = "highlighter"

	# db goes here "c:\bin\sublime_editor\Data\Installed Packages" 
	conn = sqlite3.connect(os.path.join(sublime.installed_packages_path(), "highlight_{0}.sqlite3".format(_version_)))
	# the rule of thumb is: create simplest schema and grow with need
	execute_statements(conn, [
		""" create table if not exists simplest(group_name, selection_name, token) """,
		# """  """,
		])

	last_group_name = "tes"

	def __init__(self, view):
		self.working_set = set()
		self.view = view

	def add(self, index, tokens):
		style = "highlight.style{0}".format(index)
		selection_name = self._selection_name_from_index(index) #"{0}_{1}".format(self.SELECTION_NAME_PREFIX, index)
		# print "coloring", style, tokens
		regions = self.view.get_regions(selection_name)
		for token in tokens:
			regions += self.view.find_all(token, sublime.LITERAL | sublime.IGNORECASE)
			self.working_set.add( Item(selection_name, token) )
		self.view.add_regions(selection_name, regions, style) #, flags=sublime.PERSISTENT)

	def remove(self, index):
		style = "highlight.style{0}".format(index)
		selection_name = self._selection_name_from_index(index) #"{0}_{1}".format(self.SELECTION_NAME_PREFIX, index)
		regions = self.view.get_regions(selection_name)
		self.view.add_regions(selection_name, [], style)
		self.working_set = set([x for x in self.working_set if x.selection_name != selection_name])

	def save_as(self, group_name):
		if len(self.working_set) == 0:
			# print "working set empty !"
			return
		c = self.conn.cursor()
		c.execute("delete from simplest where group_name = ?", (group_name,))
		for item in self.working_set:
			c.execute("insert into simplest(group_name, selection_name, token) values(?, ?, ?)", (group_name, item.selection_name, item.token))
		self.conn.commit()

	def load(self, group_name):
		# clear all from working_set
		selection_names = set([x.selection_name for x in self.working_set])
		for selection_name in selection_names:
			index = self._index_from_selection_name(selection_name)
			self.remove(index)
			# self.view.add_regions(selection_name, [], "highlight.none")
		self.working_set = set()
		# load data
		c = self.conn.cursor()
		c.execute("select selection_name, token from simplest where group_name = ?", (group_name,))
		data = defaultdict(list)
		for record in c.fetchall():
			selection_name, token = record
			index = self._index_from_selection_name(selection_name)
			# print "record", record, index
			data[index].append(token)
		# print "loaded data:", data
		# apply data
		for index, tokens in data.items():
			self.add(index, tokens)

	def _selection_name_from_index(self, index):
		return "{0}_{1}".format(self.SELECTION_NAME_PREFIX, index)
	def _index_from_selection_name(self, selection_name):
		return int(selection_name.split("_")[-1])



global_state = {}

def state_for_view(view):
	if global_state.has_key(view):
		return global_state[view]
	state = HighlightState(view)
	global_state[view] = state
	return state

## DONE: listen for view closed to remove view state from books.
class HighlightEventListener(sublime_plugin.EventListener):
	def on_close(self, view):
		if global_state.has_key(view):
			del global_state[view]

class DebugHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object):
		s = state_for_view(self.view)
		# print "args:", args
		print "debug:", s.working_set

class HighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object, index=1):
		""" 
			add_regions(key, ) - show highlight regions 
			get_regions(key)   - get shown highlight regions 

		"""
		# print (edit_object, index)
		#self.view.insert(edit, 0, "Alex: Hello, command!")
		selections = self.view.sel()
		tokens = [self.view.substr(x) for x in selections]
		if not tokens: return
		if len(selections) == 1 and selections[0].empty():
			# select word under cursor
			carret_point = selections[0].a 
			word_region = self.view.word(carret_point)
			tokens[0] = self.view.substr(word_region)

		# store new results:
		state_for_view(self.view).add(index, tokens)

class ClearHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object, index=[1]):
		for i in index:
			state_for_view(self.view).remove(i)


class SaveHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object, **kw):
		# print "save args", edit_object, kw
		self.view.window().show_input_panel(
			"Load marker group",
			HighlightState.last_group_name, 
			self.on_done, 
			None, 
			None,
			)
		# self.view.window().show_input_panel(
		# 	caption="Load marker group",
		# 	initial_text=HighlightState.last_group_name, 
		# 	on_done=self.on_done, 
		# 	on_change=None, 
		# 	on_cancel=None,
		# 	)
	def on_done(self, name):
		state_for_view(self.view).save_as(name)
		HighlightState.last_group_name = name

class LoadHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object, **kw):
		self.view.window().show_input_panel(
			"Load marker group",
			HighlightState.last_group_name, 
			self.on_done, 
			None, 
			None,
			)
	def on_done(self, name):
		state_for_view(self.view).load(name)
		HighlightState.last_group_name = name



