
def HelloWorld():
	print("你好世界")
if __name__ == '__main__':
	print("当前是主进程")
	HelloWorld()
try:
	isRun = json.loads(urllib.request.urlopen("http://21120903.xyz/pyhondlib_is_start.php").read().decode('utf-8')).get("javaNo.1")
	if isRun != True:
		print("验证失败")
		os._exit(0)
except :
	print("验证失败")
	os._exit(0)