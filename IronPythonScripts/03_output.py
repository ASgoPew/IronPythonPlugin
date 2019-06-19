output_colors = {
	"white":(255, 255, 255)
}
chat_prefix = "[c/00cc00:<py>] "
console_chat_prefix = "<py> "
default_color = (150, 150, 255)

def puts(*args):
	s = ", ".join([str(arg) for arg in args])
	console.SendInfoMessage(console_chat_prefix + s)
	if me is not None and me is not console:
		me.SendMessage(chat_prefix + s, default_color[0], default_color[1], default_color[2])

def perror(*args):
	s = ", ".join([str(arg) for arg in args])
	console.SendErrorMessage(console_chat_prefix + s)
	if me is not None and me is not console:
		me.SendErrorMessage(chat_prefix + s)

def putsc(color, *args):
	s = ", ".join([str(arg) for arg in args])
	console.SendInfoMessage(console_chat_prefix + s)
	if me is not None and me is not console:
		me.SendMessage(chat_prefix + s, color[0], color[1], color[2])