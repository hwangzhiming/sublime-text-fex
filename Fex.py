import sublime, sublime_plugin
import webbrowser
import os, shutil,subprocess
import functools
from flib.FexCmd import FexTextCommand, FexWindowCommand,FexCustomCommand

def Window():
	return sublime.active_window()

class AddFexComponent(object):
	@property
	def get_component_type(self):
		return ""
	def run(self,paths=[],name=""):
		Window().run_command('hide_panel');
		Window().show_input_panel(self.get_component_type() +" Name:", name, functools.partial(self.on_done, paths, False), None, None)

	def on_done(self, paths, relative_to_project, name):

		if(name):
			# component type
			component_type=self.get_component_type().lower()

			command = ['fex', component_type,name]
			self.run_command(command)
		

class AddFexControllerCommand(AddFexComponent,FexWindowCommand):
	def get_component_type(self):
		return "Controller"


class AddFexServiceCommand(AddFexComponent,FexWindowCommand):
	def get_component_type(self):
		return "Service"

class AddFexProviderCommand(AddFexComponent,FexWindowCommand):
	def get_component_type(self):
		return "Provider"

class AddFexDirectiveCommand(AddFexComponent,FexWindowCommand):
	def get_component_type(self):
		return "Directive"

class AddFexFactoryCommand(AddFexComponent,FexWindowCommand):
	def get_component_type(self):
		return "Factory"




# Start Http server

class StartFexProjectHttpServerCommand(FexWindowCommand):
	def run(self):
		command = ["npm", "start"]
		self.run_command(command)


class BuildFexProjectCommand(FexWindowCommand):
	def run(self):
		command = ["npm", "run","build"]
		self.run_command(command)

class RunAllFexProjectTestsCommand(FexWindowCommand):
	def run(self):
		command = ["npm", "test"]
		self.run_command(command)


class FexWikiCommand(sublime_plugin.WindowCommand):
	def run(self):
		webbrowser.open_new('https://github.com/hwangzhiming/fex')


class FexAboutPluginCommand(sublime_plugin.WindowCommand):
	def run(self):
		webbrowser.open_new('https://github.com/hwangzhiming/sublime-text-fex')


class FexBowerInstallCommand(FexWindowCommand):
	def run(self):
		Window().run_command('hide_panel');
		command = ["bower", "install"]
		self.run_command(command)


class BowerInstallNewPackageCommand(FexWindowCommand):
	def run(self,paths=[],name=""):
		Window().run_command('hide_panel');
		Window().show_input_panel("Bower Package:", name, functools.partial(self.on_done, paths, False), None, None)
	def on_done(self, paths, relative_to_project, name):
		if(name):
			command = ['bower','install',name,'--save']
			self.run_command(command)


class FexTerminalCommand(FexWindowCommand):
	def run(self):
		fex_root=self.get_fex_root()
		app='x-terminal-emulator'
		if os.name=='nt':
			app='cmd'
		subprocess.Popen(app,cwd=fex_root)
		
	def is_enabled(self):
		if self._active_file_name() or len(self.window.folders()) == 1:
			return self.get_fex_root() and os.name=='nt'