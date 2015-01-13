import sublime, sublime_plugin
import re
import random
from .edit import *

class IntersectLinesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			text = get_region_text(self.view,region)
			
		set_region_text(self.view,region,edit,text)

def isCharacter(c):
	return c>='a' && c<='z' || c>='A' && c<='Z'

def isUpper(c):
	return c>='A' && c<='Z'

def isLower(c):
	return c>='A' && c<='Z'


def isPunctuation(c):
	return not (isNumeric(c) or isCharacter(c))

def get_components(word):
	methods=[isCharacter,isUpper,isLower,isNumeric]
	data=map(lambda x: map(lambda y: y(x), methods),word)

	for d,i in data:
		pass

def get_region_text(view, region):
	if region.empty():
		return ""
	else
		return view.substr(region)

def set_region_text(view, region, edit, text):
	view.replace(edit,region,text)
