console = TSPlayer.Server
everyone = TSPlayer.All

# Invokes on IronPythonPlugin.Initialize()
def OnInit(args):
	global loaded
	loaded = True
	puts("IronPython OnInit ===============================")

	for f in Type.GetFields(GetDataHandlers):
		if f.GetValue(None) is None:
			f.SetValue(None, f.FieldType())

	Plugin.Initialize()

def OnClose(args):
	puts("IronPython OnClose ==============================")

	Plugin.Dispose()

	gc.collect()

def execute(script, args):
	global me
	me = args[0]
	if script.startswith('\\'):
		script = 'puts(' + script[1:] + ')'
	elif script.startswith('='):
		script = 'puts(dir(' + script[1:] + '))'
	putsc(output_colors["white"], script)
	# Extensions (clr.ImportExtensions) work with env.Engine.Execute but not with exec
	return env.Engine.Execute(script, env.Scope)

def _hook(hc, h, priority=0):
	if hc.ToString().startswith('TShockAPI.HandlerList'):
		hc.Register(h)
	elif hc.ToString().startswith('TerrariaApi.Server.HandlerCollection'):
		hc.Register(IronPythonPlugin.Instance, h, priority)
	elif str(type(hc)) == "<type 'BoundEvent'>":
		hc += h
def _unhook(hc, h):
	if hc.ToString().startswith('TShockAPI.HandlerList'):
		hc.UnRegister(h)
	elif hc.ToString().startswith('TerrariaApi.Server.HandlerCollection'):
		hc.Deregister(IronPythonPlugin.Instance, h)
	elif str(type(hc)) == "<type 'BoundEvent'>":
		hc -= h

def _add_command(permission, f, names):
	cmd = TShockAPI.Command(List[str]([permission]), TShockAPI.CommandDelegate(f), Array[str](names))
	TShockAPI.Commands.ChatCommands.Add(cmd)
	return cmd
def _remove_command(cmd):
	TShockAPI.Commands.ChatCommands.Remove(cmd)
