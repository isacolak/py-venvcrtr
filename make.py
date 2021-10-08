import os
import sys
import shutil
import subprocess

args = sys.argv[1:]
accept_args = False

def main():
	if "--accept-args" in args or "-aa" in args:
		accept_args = True
		del args[args.index("--accept-args" if "--accept-args" in args else "-aa")]

	if "make" in args or len(args) == 0:
		print("\n\t[INFO] The necessary libraries are being installed\n")
		p = subprocess.Popen([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],stdout=sys.stdout,stderr=sys.stderr).communicate()
		print("\n\t[INFO] The necessary libraries were installed")
		print("\n\t[INFO] The executable file is created\n")
		p2 = subprocess.Popen(["{}/Scripts/pyinstaller.exe".format(sys.base_prefix),"py_venvcrtr.py","-F","-c","-n","py_venvcrtr"],stdout=sys.stdout,stderr=sys.stderr).communicate()
		shutil.move("./dist/py_venvcrtr.exe","./py_venvcrtr.exe")
		print("\n\t[INFO] The executable file has been created\n")
		print("\n\t[INFO] Unnecessary files and folders are deleted\n")
		shutil.rmtree("./dist")
		shutil.rmtree("./build")
		shutil.rmtree("./__pycache__")
		os.remove("py_venvcrtr.spec")
		print("\n\t[INFO] Unnecessary files and folders have been deleted\n")

	elif len(args) > 0 and accept_args:
		p2 = subprocess.Popen(["{}/Scripts/pyinstaller.exe".format(sys.base_prefix)]+sys.argv[1:],stdout=sys.stdout,stderr=sys.stderr).communicate()

	else:
		print("usage: make.py [make]")

if __name__=="__main__":
	main()
