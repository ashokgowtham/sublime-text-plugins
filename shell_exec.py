import sublime, sublime_plugin
from subprocess import call

def get_command(string):
    return string.split('\n')

class OpenCurrentLinkInMacCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        commands = []
        for region in self.view.sel():
            if not region.empty():
                commands = commands + get_command(self.view.substr(region))
        if len(commands)==0:
            for region in self.view.sel():
                commands = commands + get_command(self.view.substr(self.view.line(region)))
        if len(commands)>0:
            print(commands)
            call(['open'] + commands)
