import os
import subprocess
import sys

from robo_pier_lib.ProcessCallback import ProcessCallback
from robo_pier_lib.run import startRobot
import logging

logging.basicConfig(level=logging.INFO)

class PythonRobot(ProcessCallback):

    async def run(self):
        python_version = "3.9"
        if self.get_config_value('pythonVersion') is not None:
            python_version = self.get_config_value('pythonVersion')

        full_app_path = os.path.abspath("./"+self.get_app_dir())

        try:
            print("Installing requirements")
            subprocess.run("pyenv local "+python_version+" && python -m pip install -r requirements.txt ", cwd=full_app_path,
                                        shell=True, check=True)

        except Exception as e:
            print("Error: ", str(e))

        script = self.get_config_value('script')
        process = subprocess.Popen("pyenv local "+python_version+" && python "+script, cwd=full_app_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        while True:
            line = process.stdout.readline()
            if process.poll() != None:
                break
            if line != '':
                print(line.rstrip())
        rc = process.poll()
        return rc

startRobot(PythonRobot)
