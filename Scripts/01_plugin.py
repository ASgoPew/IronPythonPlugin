Plugins = []

class Plugin:
	instance = None
	_hooks = {}
	_commands = {}

	def __init__(self):
		self.__class__.instance = self
	def _initialize(self):
		puts("Initializing " + self.__class__.__name__)
	def initialize(self):
		pass
	def _dispose(self):
		puts("Disposing " + self.__class__.__name__)
		self.unhook_all()
		self.remove_all_commands()
	def dispose(self):
		pass

	def hook(self, handler_collection, f, *args):
		if self._hooks.ContainsKey(f):
			self.unhook(f)
			puts('hook is already registered, reregistering...')
		self._hooks[f] = handler_collection
		_hook(handler_collection, f, *args)
	def unhook(self, f):
		hookf = next((x for x in self._hooks if x == f), None)
		if hookf is not None:
			_unhook(self._hooks[hookf], hookf)
		else:
			raise Exception("Can't deregister hook")
	def unhook_all(self):
		for hookf in self._hooks:
			self.unhook(hookf)

	def add_command(self, permission, f, *names):
		if self._commands.ContainsKey(f):
			self.remove_command(f)
			puts('command is already registered, reregistering...')
		def cmdF(args):
			try:
				f(args)
			except:
				perror(traceback.format_exc())
		command = _add_command(permission, cmdF, names)
		self._commands[f] = command
		return command
	def remove_command(self, f):
		commandf = next((x for x in self._commands if x == f), None)
		if commandf is not None:
			_remove_command(self._commands[commandf])
		else:
			raise Exception("Can't deregister command")
	def remove_all_commands(self):
		for commandf in self._commands:
			self.remove_command(commandf)

	@staticmethod
	def Initialize():
		for name, plugin_class in globals().items():
			if (type(plugin_class) == type(Plugin) and plugin_class != Plugin and len(plugin_class.__bases__) > 0
					and plugin_class.__bases__[0] == Plugin and plugin_class.Load()):
				try:
					plugin = plugin_class()
					Plugins.Add(plugin)
					plugin._initialize()
					plugin.initialize()
				except:
					perror(traceback.format_exc())
	@staticmethod
	def Dispose():
		for plugin in Plugins:
			try:
				plugin._dispose()
				plugin.dispose()
			except:
				perror(traceback.format_exc())
	@staticmethod
	def Load():
		return True