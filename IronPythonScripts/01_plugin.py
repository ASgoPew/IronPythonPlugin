Plugins = []

class Plugin:
	instance = None

	def __init__(self):
		self.__class__.instance = self
		self._hooks = {}
		self._commands = {}
		self._timers = {}
	def _initialize(self):
		puts("Initializing " + self.__class__.__name__)
	def initialize(self):
		puts("Disposing " + self.__class__.__name__)
	def _dispose(self):
		self.unhook_all()
		self.remove_all_commands()
		self.remove_all_timers()
	def dispose(self):
		pass

	def hook(self, handler_collection, f, *args):
		if self._hooks.ContainsKey(f):
			self.unhook(f)
			puts('hook is already registered, reregistering...')
		self._hooks[f] = handler_collection
		_hook(handler_collection, f, *args)
	def unhook(self, f):
		if f in self._hooks:
			_unhook(self._hooks[f], f)
			self._hooks.Remove(f)
		else:
			raise Exception("Can't deregister hook")
	def unhook_all(self):
		for hookf in self._hooks.copy():
			self.unhook(hookf)

	def add_command(self, permission, f, *names):
		if self._commands.ContainsKey(f):
			self.remove_command(f)
			puts('command is already registered, reregistering...')
		def cmdF(args):
			try:
				f(args)
			except:
				ptraceback()
		command = _add_command(permission, cmdF, names)
		self._commands[f] = command
		return command
	def remove_command(self, f):
		if f in self._commands:
			_remove_command(self._commands[f])
			self._commands.Remove(f)
		else:
			raise Exception("Can't deregister command")
	def remove_all_commands(self):
		for commandf in self._commands.copy():
			self.remove_command(commandf)

	def add_timer(self, ms, f):
		if self._timers.ContainsKey(f):
			self.remove_timer(f)
			puts('timer is already added, readding...')
		timer = self._timers[f] = create_timer(ms, f, True)
		return timer
	def remove_timer(self, f):
		if f in self._timers:
			self._timers[f].Stop()
			self._timers.Remove(f)
		else:
			raise Exception("Can't remove timer")
	def remove_all_timers(self):
		for f in self._timers.copy():
			self.remove_timer(f)

	@staticmethod
	def Initialize():
		puts('IronPython plugins begin ========================')
		for name, plugin_class in list(globals().items()):
			if (type(plugin_class) == type(Plugin) and plugin_class != Plugin and len(plugin_class.__bases__) > 0
					and plugin_class.__bases__[0] == Plugin and plugin_class.Load()):
				try:
					plugin = plugin_class()
					Plugins.Add(plugin)
					plugin._initialize()
					plugin.initialize()
				except:
					ptraceback()
		puts('IronPython plugins end ==========================')
	@staticmethod
	def Dispose():
		for plugin in Plugins:
			try:
				# Removing all hooks, commands and timers after
				plugin._dispose()
				# Custom dispose first
				plugin.dispose()
			except:
				ptraceback()
	@staticmethod
	def Load():
		return True

def plugins():
	return [p.__class__.__name__ for p in Plugins]
