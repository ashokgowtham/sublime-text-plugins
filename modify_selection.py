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
			print(region)
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
