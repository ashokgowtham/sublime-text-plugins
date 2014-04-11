import sublime, sublime_plugin
import re
import random
from decimal import *
from .edit import *

random.seed(1)

class IncrementNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				text=increment(self.view.substr(region))
				print(text)
				self.view.replace(edit,region,text)

class DecrementNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				text=decrement(self.view.substr(region))
				print(text)
				self.view.replace(edit,region,text)

class GenerateMathematicalProgressionCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = sublime.active_window().active_view();
		self.window.show_input_panel("format","n+1", self.getcallback(view), None, None)
		# self.getcallback(edit)("n")

	def getcallback(self,view):
		def callback(value):
			format_regex="/^[0-9n\-\+]$/"
			format=value;
			if re.search(format_regex,format)!=None:
				pass
			index=0
			for region in view.sel():
				edit=Edit(view);
				text=str(eval(format.replace('n',str(index))))
				print(region)
				print(text)
				edit.replace(view.sel()[index],text)
				index=index+1;
				edit.complete();
		return callback;

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

def increment(text):
	try:
		value=(Decimal(text)) if '.' in text else int(text)
		return str(value+1)
	except Exception:
		print("error")
		return text

def decrement(text):
	try:
		value=(Decimal(text)) if '.' in text else int(text)
		return str(value-1)
	except Exception:
		return text
