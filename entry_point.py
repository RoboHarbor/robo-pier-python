import asyncio
import os
import subprocess
import sys
import threading

from robo_pier_lib.ProcessCallback import ProcessCallback
from robo_pier_lib.run import startRobot
import logging
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen


logging.basicConfig(level=logging.INFO)

class PythonRobot(ProcessCallback):

    def stream_command(
            self,
            args,
            *,
            stdout_handler=logging.info,
            stderr_handler=logging.error,
            check=True,
            text=True,
            stdout=PIPE,
            stderr=PIPE,
            **kwargs,
    ):
        """Mimic subprocess.run, while processing the command output in real time."""
        with Popen(args, text=text, stdout=stdout, stderr=stderr, **kwargs) as process:
            with ThreadPoolExecutor(2) as pool:  # two threads to handle the streams
                exhaust = partial(pool.submit, partial(deque, maxlen=0))
                exhaust(stdout_handler(line[:-1]) for line in process.stdout)
                exhaust(stderr_handler(line[:-1]) for line in process.stderr)
        retcode = process.poll()
        if check and retcode:
            raise CalledProcessError(retcode, process.args)
        return CompletedProcess(process.args, retcode)

    async def run(self):
        python_version = "3.9"
        if self.get_config_value('pythonVersion') is not None:
            python_version = self.get_config_value('pythonVersion')
        print("Python version: ", python_version)

        full_app_path = os.path.abspath(self.get_app_dir())

        try:
            print("Installing requirements")
            subprocess.run("pyenv local "+python_version+" && pip install -r requirements.txt ", cwd=full_app_path,
                                        shell=True, check=True)

        except Exception as e:
            print("Error: ", str(e))

        script = self.get_config_value('script')
        """process = subprocess.Popen("python"+python_version+" "+script,
                                   shell=True,
                                   cwd=full_app_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)"""

        rc = self.stream_command(
            ["python"+python_version, script],
            cwd=full_app_path,
             stdout_handler = print, stderr_handler = print
        )

        if rc.returncode != 0:
            print("Error: ", rc)

        return rc

startRobot(PythonRobot)
