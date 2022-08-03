class PluginExample(Plugin):
	# Static method for checking if this plugin should be loaded.
	@staticmethod
	def Load():
		return True

	# Method will be called automatically on plugin load (on IronPythonPlugin load or `/py reset` command).
	def initialize(self):
		# Registering a command for registering and unregistering tests in runtime.
		self.add_command("*", self.RegisterCommand, "reg")
		# A field showing whether test hooks, command and timer were registered.
		self.registered = False

		delay(3000, lambda: puts("Hello world from IronPython!"))

	# Method will be called automatically on plugin unload (on IronPythonPlugin dispose or `/py reset` command).
	def dispose(self):
		# Actually we don't need to do anything here because all hooks, commands and timers unregister automatically.
		pass

	# A test method for registering a few hooks, a command and a timer for tests.
	def register(self):
		# Note that in every time you call e.g. self.OnServerChat it creates a new method reference instance.
		# So you cannot register and unregister the function like this:
		#   self.hook(ServerApi.Hooks.ServerChat, self.OnServerChat)
		#   self.unhook(ServerApi.Hooks.ServerChat, self.OnServerChat)
		# You have to save the method reference if you need to unregister it during the work.
		# Otherwise using method reference directly would be fine since plugin
		# automatically deregister all hooks, commands and timers on `/py reset`

		# Function hook(handler_collection, function) registers a callback function to the handler collection
		# that can be an event or any other server hook.
		# Don't forget to use try except in plugins because you won't see errors without it.
		# Also check that callback function has enough amount of argumens (otherwise it will be
		# silently ignored without subsciption).
		self.OnServerChatInstance = self.OnServerChat
		self.hook(ServerApi.Hooks.ServerChat, self.OnServerChatInstance)

		# Let's register a function that will raise a python error on TogglePvp packet from client:
		self.OnTogglePvpInstance = self.OnTogglePvp
		self.hook(GetDataHandlers.TogglePvp, self.OnTogglePvpInstance)

		# Just an example of hooking Event hook.
		# self.OnTickInstance = self.OnTick
		# self.hook(Main.OnTickForThirdPartySoftwareOnly, self.OnTickInstance)

		# Add a python command with add_command(permission, function, name1, name2, name3, ...)
		self.TestCommandInstance = self.TestCommand
		self.add_command("permission.name", self.TestCommandInstance, "test", "test2")

		# Add a timer with add_timer(milliseconds, function)
		self.OnTimerInstance = self.OnTimer
		self.add_timer(5000, self.OnTimerInstance).Start()

		puts("Test hooks, command and a timer registered!")

		self.registered = True

	# Call this to unregister everything registered in register()
	def unregister(self):
		# Unregistering saved instances.
		self.unhook(self.OnServerChatInstance)
		self.unhook(self.OnTogglePvpInstance)
		# self.unhook(self.OnTickInstance)
		self.remove_command(self.TestCommandInstance)
		self.remove_timer(self.OnTimerInstance)

		puts("Everything unregistered!")

		self.registered = False

	# A command for registering and unregistering tests in runtime.
	def RegisterCommand(self, args):
		if self.registered:
			self.unregister();
		else:
			self.register()

	def OnTogglePvp(self, sender, args):
		# Here we will raise an error to see the output.
		try:
			# Calling an undefined function
			this_will_raise_an_error()
			puts("This won't be printed.")
		except:
			# You can get a traceback by calling:
			#    traceback.format_exc()
			# The simpliest way to handle exception:
			ptraceback()

			puts("Error from IronPython")

	def OnServerChat(self, args):
		puts("ServerChat hook from IronPython")

	def OnTick(self):
		puts("OnTick hook from IronPython")

	def TestCommand(self, args):
		puts("Test command from IronPython")

	def OnTimer(self):
		puts("5 seconds timer from IronPython")
