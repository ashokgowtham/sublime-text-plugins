import sublime, sublime_plugin


class GenerateSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get number of selections N
		# generate N <space-char>s
		# place N cursors
		pass

class SelectTillNextSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		index=-1
		sels=[]
		last_region=None
		for region in self.view.sel():
			index=index+1
			if index==0:
				last_region=region
				continue
			last_region.b=region.a-1
			sels.append(last_region)
			last_region=region
		sels.append(last_region)
		sels[-1].b=self.view.size()
		self.view.sel().clear()
		self.view.sel().add_all(sels)


class GenerateCursorsCommand(sublime_plugin.WindowCommand):
	def run(self):
		view = sublime.active_window().active_view();
		self.window.show_input_panel("Number of cursors / lines","100", self.getcallback(view), None, None)

	def getcallback(self, view):
		def callback(value):
			view.run_command("generate_cursors_text", {"count": value})
		return callback;

class GenerateCursorsTextCommand(sublime_plugin.TextCommand):
	def run(self, edit, count):
		for region in self.view.sel():
			self.view.replace(edit, region, "\n" * (int(count) - 1))
		self.view.run_command("split_selection_into_lines")
		self.view.run_command("select_lines", {"forward": True})


