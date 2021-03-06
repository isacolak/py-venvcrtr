import os
import sys
import glob
import shutil
import argparse
import subprocess
from tqdm import tqdm
from itertools import chain

__author__ = "İsa Çolak"
__copyright__ = "Copyright (C) 2021 İsa Çolak"
__license__ = "MIT License"
__version__ = "0.1"

class printExecutablesAction(argparse.Action):
	def __init__(self,
			option_strings,
			dest=argparse.SUPPRESS,
			default=argparse.SUPPRESS,
			help=None
			):
		
		super(printExecutablesAction, self).__init__(
			option_strings=option_strings,
			dest=dest,
			default=default,
			nargs=0,
			help=help
			)

	def __call__(self, parser, namespace, values, option_string=None):
		executablesDict = findPythonExecutables()
		for executable in executablesDict:
			print(f"{executable} => {executablesDict[executable]}")
		parser.exit()

class printExecutablesVersionDictAction(argparse.Action):
	def __init__(self,
			option_strings,
			dest=argparse.SUPPRESS,
			default=argparse.SUPPRESS,
			help=None
			):
		
		super(printExecutablesVersionDictAction, self).__init__(
			option_strings=option_strings,
			dest=dest,
			default=default,
			nargs=0,
			help=help
			)

	def __call__(self, parser, namespace, values, option_string=None):
		executablesDict = findPythonExecutables(isReturnVersionDict=True)
		for executable in executablesDict:
			print(f"{executable} => {executablesDict[executable]}")
		parser.exit()

def venvCreator(args,executable,verbose):
	if isinstance(args,str):
		args = args.split()
	elif isinstance(args,list):
		pass
	else:
		raise TypeError("args must be list object or str object")
	
	args = ["virtualenv",f"--python={executable}"]+args
	
	if verbose:
		print("")
		p = subprocess.Popen(args,stdout=sys.stdout,stderr=sys.stderr).communicate()
	else:
		p = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

def findPythonExecutables(isReturnVersionDict=False):
	executables = {}
	executablesDict = {}

	try:
		p = subprocess.Popen(["py","-0p"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
		exeL = p[0].decode("utf-8")[3:].split("\n")
		for exe in exeL:
			exeV = exe.split()[0].split("-")[1]
			exeP = exe.split(" "*8)[-1].replace(os.sep,"/")

			executablesDict[exeP] = exeV

	except FileNotFoundError as e:
		folders = ["/usr/bin","/bin"]
		folders = map(lambda path:glob.glob(path), folders)
		folders = list(chain(*folders))

		files = []

		for i in folders:
			if os.path.isdir(i):
				for dirpath, dirnames, filenames in os.walk(i):
					files.extend(os.path.join(dirpath,f) for f in filenames if len(f) >= 5 and f.startswith("python"))
		
		executablesL = []

		for f in files:
			f = f.replace(os.sep, "/").split("/")[-1].split("-")[0]

			if f not in executablesL:
				executablesL.append(f)
		
		# if "python3" in executablesL: executablesL.remove("python3")
		# if "python" in executablesL: executablesL.remove("python")
		
		for e in executablesL:
			p = subprocess.Popen([e,"-c","import sys; print(sys.executable);print('.'.join([str(sys.version_info.major),str(sys.version_info.minor),str(sys.version_info.micro)]))"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8").replace("\r","").split("\n")

			executablesDict[p[0].replace(os.sep,"/")] = p[1]

	for exeP in executablesDict:
		exeV = executablesDict[exeP]

		if isReturnVersionDict:
			exeVO = exeV
			s = 1

			while exeV in executables:
				exeV = exeVO+f"({s})"
				s+=1

			executables[exeV] = exeP
		else:
			executables[exeP] = exeV
	
	return executables

def main():
	p = subprocess.Popen(["python3","-c","import sys; print(sys._base_executable);print('.'.join([str(sys.version_info.major),str(sys.version_info.minor),str(sys.version_info.micro)]))"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8").replace("\r","").split("\n")
	defaultExecutable = p[0].replace(os.sep,"/")
	defaultExecutableVersion = p[1]

	parser = argparse.ArgumentParser(prog="py_venvcrtr",allow_abbrev=False,
		description='Creates a virtual environment for Python.')
	parser.add_argument('dir', metavar='ENV_DIR',
		help='Directory of the created virtual environment.')
	parser.add_argument('libraries', metavar='LIBRARIES', nargs='*', action='append',
		help='Libraries to be downloaded when creating virtual environment.')
	parser.add_argument('-pyv','--python-version', default=None, action='store',
		dest='python_version', help=f'Python executable version.Note: Please run the -pyvl argument before using this (Default= {defaultExecutableVersion}).')
	parser.add_argument('-pyvl','--python-versions-list', default=False, action=printExecutablesVersionDictAction,
		dest='python_versions_list', help='Python executable versions list.')
	parser.add_argument('-py','--python', default=None, action='store',
		dest='python', help=f'Python executable path.Note: Please run the -pyl argument before using this (Default= {defaultExecutable}).')
	parser.add_argument('-pyl','--pythons-list', default=False, action=printExecutablesAction,
		dest='pythons_list', help='Python executables paths list.')
	parser.add_argument("-W","--overwrite", default=False, action="store_true",
		dest='overwrite', help="Overwriting the existing virtualenv")
	parser.add_argument('-V','--version', action='version',
		version=f"%(prog)s {__version__}",help="Show program's version number and exit.")
	parser.add_argument('--system-site-packages', default=False, action='store_true',
		dest='system_site', help='Give the virtual environment access to the system site-packages dir (Default= False).')
	parser.add_argument('--verbose', default=False, action='store_true',
		dest='verbose', help='Show verbose of the process (Default = False).')
	parser.add_argument('--no-update', default=False, action='store_true',
		dest='no_update', help='Do not update pip and setuptools (Default= False).')
	
	options = parser.parse_args()
	libraries = options.libraries
	verbose = options.verbose
	pipLibraries = ["pip","setuptools"]
	env_dir = options.dir
	env_exe = None
	args = []
	pythonExecutablesVersionDict = findPythonExecutables(True)
	pythonExecutables = findPythonExecutables()
	executable = None

	args.append(env_dir)
	
	if options.system_site:
		args.append("--system-site-packages")
	
	if options.python_version and options.python:
		raise ValueError('You cannot supply --python and --python-version together.')
	
	if options.python:
		if options.python in pythonExecutables:
			executable = options.python
		else:
			raise ValueError(f'Executable not found. Executable: {options.python}')
	elif options.python_version:
		if options.python_version in pythonExecutablesVersionDict:
			executable = pythonExecutablesVersionDict[options.python_version]
		else:
			raise ValueError(f'Version not found. Version: {options.python_version}')
	else:
		executable = defaultExecutable
	
	if os.path.exists(env_dir):
		if options.overwrite:
			print("\n[INFO] Existing virtualenv with the same name is being deleted.")
			shutil.rmtree(env_dir)
			print("\n[INFO] Existing virtualenv with the same name has been deleted.")
		else:
			parser.error(f"A virtualenv named {env_dir} already exists. If you want to overwrite, please use the -W/--overwrite argument.")
	
	print("\n[INFO] The required modules are being installed.")
	if verbose:
		p = subprocess.Popen(["python3","-m","pip","install","virtualenv"],stdout=sys.stdout,stderr=sys.stderr).communicate()
	else:
		p = subprocess.Popen(["python3","-m","pip","install","virtualenv"],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

	print("\n[INFO] The necessary modules have been installed.")

	print("\n[INFO] Virtualenv is being created.")
	venvCreator(args,executable,verbose)
	print("\n[INFO] Virtualenv was created.")
	
	g = glob.glob(f"{env_dir}/Scripts/python*")
	
	if not g:
		g = glob.glob(f"{env_dir}/bin/python*")

		if not g:
			parser.exit(2, f"\n{parser.prog}: error: The executable file in the virtualenv cannot be reached. Please make sure that the virtual environment is properly created or try to re-create with the --verbose argument.\n")

	env_exe = g[0]

	if not options.no_update:
		print("\n[INFO] pip libraries are being updated.\n")

		if verbose:
			p = subprocess.Popen([env_exe,"-m","pip","install","--upgrade"]+pipLibraries,stdout=sys.stdout,stderr=sys.stderr).communicate()
		else:
			pbar = tqdm(pipLibraries,desc="[PROCESS] Updated pip libraries :",bar_format="{desc} {n_fmt}/{total_fmt}")
			for library in pbar:
				pbar.set_description(f"[PROCESS] Updated pip libraries - {library} ")
				p = subprocess.Popen([env_exe,"-m","pip","install","--upgrade",library],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
			
			pbar.set_description(f"[PROCESS] Updated pip libraries ")
		
		print("\n[INFO] pip libraries have been updated.")
	
	if len(libraries[0]) > 0:
		print("\n[INFO] Libraries are established.\n")
		if verbose:
			p = subprocess.Popen([env_exe,"-m","pip","install"]+libraries[0],stdout=sys.stdout,stderr=sys.stderr).communicate()
		else:
			pbar = tqdm(libraries[0],desc="[PROCESS] Libraries established :",bar_format="{desc} {n_fmt}/{total_fmt}")
			for library in pbar:
				pbar.set_description(f"[PROCESS] Libraries established - {library} ")
				p = subprocess.Popen([env_exe,"-m","pip","install",library],stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()

			pbar.set_description(f"[PROCESS] Libraries established ")
		
		print("\n[INFO] Libraries were established.")

if __name__ == "__main__":
	main()
