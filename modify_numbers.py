import sublime, sublime_plugin
import re
import math
import random
from decimal import *
from .edit import *

random.seed(1)

class IncrementNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				text=increment(self.view.substr(region))
				self.view.replace(edit,region,text)

class DecrementNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				text=decrement(self.view.substr(region))
				self.view.replace(edit,region,text)

class GenerateMathematicalProgressionCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = sublime.active_window().active_view();
		self.window.show_input_panel("format","n+1", self.getcallback(view), None, None)

	def getcallback(self, view):
		def callback(value):
			# use a text command to do the actual string editting.
			# so that only one entry is added to undo buffer and no other hacks are needed
			view.run_command("generate_mathematical_progression_text", {"format": value})
		return callback;


class GenerateMathematicalProgressionTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, format):
		format_regex = "/^[0-9n\-\+]$/"
		if re.search(format_regex, format) != None:
			pass
		index = 0
		for region in self.view.sel():
			expr = get_expression(format,index)
			text = str(eval(expr))
			self.view.replace(edit,region, text)
			index = index + 1;

class EvaluateLineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			text=self.view.substr(region)
			if text.strip()!="":
				text=str(eval(text))
				self.view.replace(edit,region,text)

class GenerateRandomNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		index=0
		for region in self.view.sel():
			text=str(random.randint(0,100));
			self.view.replace(edit,region,text)
			index=index+1;

class GenerateBarGraphCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				text=toBarGraph(self.view.substr(region))
				self.view.replace(edit,region,text)

class AshExpandSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sels=self.view.sel()
		l=len(sels)
		for i in range(0,l-1):
			sels[i].b=sels[i+1].a-1
		sels[l-1].b=1000

def get_expression(raw_expr, replacement):
	if '{' in raw_expr:
		return raw_expr.replace('{n}', str(replacement))
	return raw_expr.replace('n', str(replacement))

def toBarGraph(text):
	fractional_part = ['', '▏','▎','▍','▌','▋','▊','▉']
	value = toNumber(text)
	if value<0:
		return "<Negative number not handled yet>"
	value = (value/8.0) # since we use increments of eighths in unicode character
	bar = math.floor(value) * '█'
	bar = bar + fractional_part[math.floor((value - math.floor(value))*8)]
	return bar

def increment(text):
	return str(toNumber(text)+1)

def decrement(text):
	return str(toNumber(text)-1)

def toNumber(text):
	try:
		return (float(text)) if '.' in text else int(text)
	except Exception as exception:
		print("Error in toNumber:")
		print(exception)
		return text
