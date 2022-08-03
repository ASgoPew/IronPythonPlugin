output_colors = {
	"white":(255, 255, 255)
}
chat_prefix = "[c/00cc00:<python>] "
console_chat_prefix = "<python> "
default_color = (150, 150, 255)
info_color = (255, 255, 0)
warning_color = (255, 69, 0)

def puts(*args):
	SendMessage(", ".join([str(arg) for arg in args]), default_color[0], default_color[1], default_color[2])

def putsi(*args):
	SendMessage(", ".join([str(arg) for arg in args]), info_color[0], info_color[1], info_color[2])

def putsw(*args):
	SendMessage(", ".join([str(arg) for arg in args]), warning_color[0], warning_color[1], warning_color[2])

def putsc(color, *args):
	SendMessage(", ".join([str(arg) for arg in args]), color[0], color[1], color[2])

def perror(*args):
	if len(args) == 1 and args[0].GetType().Name.EndsWith("Exception"):
		pexception(args[0])
		return
	SendErrorMessage(", ".join([str(arg) for arg in args]))

def say(*args):
	BroadcastMessage(", ".join([str(arg) for arg in args]), default_color[0], default_color[1], default_color[2])

def ptraceback():
	perror(traceback.format_exc())

def pexception(e):
	perror(env.GetExceptionTraceback(e))

def SendMessage(text, r, g, b):
	if loaded:
		console.SendInfoMessage(console_chat_prefix + text)
	else:
		print(console_chat_prefix + text)
	text = chat_prefix + text
	if loaded:
		iterate_players(lambda player: player.SendMessage(text, r, g, b), check_control_permission)

def BroadcastMessage(text, r, g, b):
	if loaded:
		console.SendInfoMessage(console_chat_prefix + text)
	else:
		print(console_chat_prefix + text)
	text = chat_prefix + text
	if loaded:
		iterate_players(lambda player: player.SendMessage(text, r, g, b), None)

def SendErrorMessage(text):
	if loaded:
		console.SendErrorMessage(console_chat_prefix + text)
	else:
		print(console_chat_prefix + text)
	text = chat_prefix + text
	if loaded:
		iterate_players(lambda player: player.SendErrorMessage(text), check_control_permission)
