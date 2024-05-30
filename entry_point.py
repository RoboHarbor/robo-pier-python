import subprocess
import sys

from robo_pier_lib.ProcessCallback import ProcessCallback
from robo_pier_lib.run import startRobot
import logging

logging.basicConfig(level=logging.INFO)

class PythonRobot(ProcessCallback):

    def set_python_version(self, version):
        print("Setting python version to " + version)
        subprocess.run("pyenv global " + version, shell=True, check=True)

    async def run(self):
        if self.get_config_value('pythonVersion') is not None:
            self.set_python_version(self.get_config_value('pythonVersion'))

        script = self.get_config_value('script')
        process = subprocess.Popen("python  "+script, cwd=self.get_app_dir(),
                                   shell=True, stdout=subprocess.PIPE,
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