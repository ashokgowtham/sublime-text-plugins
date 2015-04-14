import sublime, sublime_plugin
from subprocess import call

class OpenCurrentLinkInMacCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				command=self.view.substr(region)
				print(command)
				call(['open',command])
