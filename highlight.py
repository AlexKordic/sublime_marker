"""
TODO:
	- Learn from https://github.com/SublimeText/WordHighlight
"""

import sublime, sublime_plugin

import os
import sys
import pickle
from collections import defaultdict
from traceback import print_exc


STORAGE_DIR = os.path.join(sublime.installed_packages_path(), "_marker_data")
try:
	os.mkdir(STORAGE_DIR)
except:
	pass # :D


def execute_statements(conn, statements):
	c = conn.cursor()
	for statement in statements:
		c.execute(statement)


class Item(object):
	"Intended to be immutable to work with set() container"
	# __slots__ = ("selection_name", "token")
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
		filename = os.path.join(STORAGE_DIR, "{0}.pickled".format(group_name))
		try:
			with open(filename, 'wb') as f:
				pickle.dump(self.working_set, f, 0)
		except:
			print_exc()

	def load(self, group_name):
		# load data
		filename = os.path.join(STORAGE_DIR, "{0}.pickled".format(group_name))
		try:
			with open(filename, "rb") as f:
				working_set = pickle.load(f)
			# run ckeck of working set:
			if not isinstance(working_set, set):
				raise Exception("Not a set", working_set)
			for el in working_set:
				if not isinstance(el, Item):
					raise Exception("Not a Item", Item)
			
			# clear all from working_set
			selection_names = set([x.selection_name for x in self.working_set])
			for selection_name in selection_names:
				index = self._index_from_selection_name(selection_name)
				self.remove(index)
				# self.view.add_regions(selection_name, [], "highlight.none")

			self.working_set = working_set
			# apply loaded items
			for item in self.working_set:
				index = self._index_from_selection_name(item.selection_name)
				style = "highlight.style{0}".format(index)
				regions = self.view.get_regions(item.selection_name)
				regions += self.view.find_all(item.token, sublime.LITERAL | sublime.IGNORECASE)
				self.view.add_regions(item.selection_name, regions, style) #, flags=sublime.PERSISTENT)
		except:
			print_exc()

	def _selection_name_from_index(self, index):
		return "{0}_{1}".format(self.SELECTION_NAME_PREFIX, index)
	def _index_from_selection_name(self, selection_name):
		return int(selection_name.split("_")[-1])



global_state = {}

def state_for_view(view):
	key_in_global_state = id(view)
	if key_in_global_state in global_state:
		return global_state[key_in_global_state]
	state = HighlightState(view)
	global_state[key_in_global_state] = state
	return state

## DONE: listen for view closed to remove view state from books.
class HighlightEventListener(sublime_plugin.EventListener):
	def on_close(self, view):
		key_in_global_state = id(view)
		if key_in_global_state in global_state:
			del global_state[key_in_global_state]

class DebugHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit_object):
		s = state_for_view(self.view)
		# print "args:", args
		print ("debug:", s.working_set)

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


