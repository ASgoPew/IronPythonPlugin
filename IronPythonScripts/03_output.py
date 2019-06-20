output_colors = {
	"white":(255, 255, 255)
}
chat_prefix = "[c/00cc00:<python>] "
console_chat_prefix = "<python> "
default_color = (150, 150, 255)

def puts(*args):
	SendMessage(", ".join([str(arg) for arg in args]), default_color[0], default_color[1], default_color[2])

def putsc(color, *args):
	SendMessage(", ".join([str(arg) for arg in args]), color[0], color[1], color[2])

def perror(*args):
	if len(args) == 1 and args[0].GetType().Name.EndsWith("Exception"):
		pexception(args[0])
		return
	SendErrorMessage(", ".join([str(arg) for arg in args]))

def ptraceback():
	perror(traceback.format_exc())

def pexception(e):
	perror(env.GetExceptionTraceback(e))

def SendMessage(text, r, g, b):
	console.SendInfoMessage(console_chat_prefix + text)
	text = chat_prefix + text
	for i in range(255):
		player = TShock.Players[i]
		if player is not None and player.Active and player.HasPermission(IronPythonConfig.ControlPermission):
			player.SendMessage(text, r, g, b)

def SendErrorMessage(text):
	console.SendErrorMessage(console_chat_prefix + text)
	text = chat_prefix + text
	for i in range(255):
		player = TShock.Players[i]
		if player is not None and player.Active and player.HasPermission(IronPythonConfig.ControlPermission):
			player.SendErrorMessage(text)