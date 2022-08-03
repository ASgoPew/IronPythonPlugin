def tostring(o):
	return str(o)

def delay(ms, f):
	Task.Delay(ms).ContinueWith(lambda t: delayF(f))

def delayF(f):
	try:
		f()
	except:
		ptraceback()

def sleep(ms):
	Thread.Sleep(ms)

def create_timer(ms, f, repeat=True):
	t = Timer(ms)
	if repeat:
		t.AutoReset = True
	t.Elapsed += lambda sender, args: f()
	return t

def iterate2(arr, f):
	for i in range(arr.GetLength(0)):
		for j in range(arr.GetLength(1)):
			f(arr[i, j], i, j)

statusEnding = '\n' * 80
def player_status(player, text):
	player.SendData(PacketTypes.Status, text + statusEnding)

def measurems(f):
	start = time.clock()
	f()
	end = time.clock()
	return (end - start) * 1000

def emptyfunction():
	pass

def testspeedf(f, seconds=1):
	t = time.clock()
	count = 0
	while time.clock() - t < seconds:
		f()
		count = count + 1
	puts('function called ' +  str(count) + ' times per %s seconds' % seconds)

# You can use import threading and threading.Lock() instead of this
class lock(IDisposable):
	def __init__(self, obj):
		self.obj = obj
		Monitor.Enter(obj)

	def Dispose(self):
		Monitor.Exit(self.obj)

# def test():
# 	delay(1, testf1)
# 	testf2()
# def testf1():
# 	with lock(me):
# 		for i in range(1000):
# 			puts(1, i)
# def testf2():
# 	sleep(10)
# 	with lock(me):
# 		for i in range(1000):
# 			puts(2, i)

class WasField:
	def __init__(self, sizeW, sizeH, x=None, y=None, startingFrom=None):
		if startingFrom is None:
			startingFrom = 1
		was = {}
		for i in range(startingFrom, startingFrom + sizeW):
			was[i] = {}
			for j in range(startingFrom, startingFrom + sizeH):
			  was[i][j] = False
		if x is not None and y is not None:
			was[x][y] = True
		self.was = was

	def check(self, i, j):
		if self.was.ContainsKey(i) and self.was[i].ContainsKey(j):
			return self.was[i][j]
		return None

	def set(self, i, j, value):
		if not self.was.ContainsKey(i):
			self.was[i] = {}
		self.was[i][j] = value
