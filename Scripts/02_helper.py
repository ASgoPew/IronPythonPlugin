def delay(ms, f):
	Task.Delay(ms).ContinueWith(lambda t: delayF(f))

def delayF(f):
	try:
		f()
	except Exception as e:
		puts(e)
	return env.Engine.Execute(script, env.Scope)

def iterate2(arr, f):
	for i in range(arr.GetLength(0)):
		for j in range(arr.GetLength(1)):
			f(arr[i, j], i, j)

def measurems(f):
	start = time.clock()
	f()
	end = time.clock()
	return (end - start) * 1000