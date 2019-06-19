class PluginExample(Plugin):
	# Static method for checking if this plugin should be loaded.
	@staticmethod
	def Load():
		return True

	# Method will be called automatically on plugin load (on IronPythonPlugin load or /py reset command).
	def initialize(self):
		# Function hook(handler collection, function) registers the function to the handler collection
		# that can be an event or any other server hook.
		# Don't forget to use try except in plugins because you won't see errors without it.
		# Also check that hook function has enough amount of argumens (otherwise it will be
		# silently ignored without subsciption).
		self.hook(ServerApi.Hooks.ServerChat, self.OnServerChat)

		# Let's register a function that will raise a python error on player chat:
		self.hook(GetDataHandlers.TogglePvp, self.OnTogglePvp)

		# Just an example of hooking Event hook.
		#self.hook(Main.OnTick, self.OnTick)

		# Add a python command with add_command(permission, function, name1, name2, name3, ...)
		self.add_command("permission.name", self.TestCommand, "test", "test2")

		delay(3000, lambda: puts("Hello world with 3s delay!!!"))

	# Method will be called automatically on plugin unload (on IronPythonPlugin dispose or /py reset command).
	def dispose(self):
		# Actually we don't need to do anything here because all hooks and commands unregister automatically.
		pass

	def OnTogglePvp(self, sender, args):
		# Here we will raise an error to see the output.
		try:
			this_will_raise_an_error()
			puts("This won't be printed.")
		except:
			perror(traceback.format_exc(), "\n(THIS IS IronPythonPlugin SCRIPT ERROR EXAMPLE, REMOVE INVALID FUNCTION CALL FROM plugin_example.py OR DISABLE PluginExample)")

	def OnServerChat(self, args):
		puts("You said something in chat, yay!\n(THIS IS IronPythonPlugin SCRIPT EXAMPLE, REMOVE HOOK FROM plugin_example.py OR DISABLE PluginExample)")

	def OnTick(self):
		puts("OnTick test")

	def TestCommand(self, args):
		puts("You executed test python command!")