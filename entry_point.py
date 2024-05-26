import subprocess
import sys

from robo_pier_lib.ProcessCallback import ProcessCallback
from robo_pier_lib.run import startRobot

class PythonRobot(ProcessCallback):

    def set_python_version(self, version):
        print("Setting python version to " + version)
        subprocess.run("pyenv global " + version, shell=True, check=True)

    def run(self):
        if self.get_config_value('python_version') is not None:
            self.set_python_version(self.get_config_value('python_version'))
        process = subprocess.Popen("python test.py ", shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, bufsize=0, text=True)

        while True:
            line = process.stdout.readline()
            if process.poll() != None:
                break
            if line != '':
                sys.stdout.write(line)
                sys.stdout.flush()
        rc = process.poll()
        print("aaa finished with return code: " + str(rc))
        return 0

startRobot(PythonRobot)