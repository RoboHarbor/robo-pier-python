import asyncio
import os
import subprocess
import sys
import threading
from queue import Queue
from subprocess import Popen, PIPE
from threading import Thread
from robo_pier_lib.ProcessCallback import ProcessCallback
from robo_pier_lib.run import startRobot
import logging
import select
import subprocess as sp
from asyncio import create_subprocess_shell
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from subprocess import PIPE, CalledProcessError, CompletedProcess, Popen
import pty


logging.basicConfig(level=logging.INFO)

class PythonRobot(ProcessCallback):

    async def run(self):
        python_version = "3.9"
        if self.get_config_value('pythonVersion') is not None:
            python_version = self.get_config_value('pythonVersion')
        print("Python version: ", python_version)

        full_app_path = os.path.abspath(self.get_app_dir())

        try:
            print("Installing requirements")
            subprocess.run("pyenv local "+python_version+" && pyenv exec pip install -r requirements.txt ",
                                        cwd=full_app_path,
                                        shell=True)

        except Exception as e:
            print("Error: ", str(e))

        script = self.get_config_value('script')
        print("Running script: ", script)

        p1 = await create_subprocess_shell("pyenv local "+python_version+" && pyenv exec python "+script,
                                           cwd=full_app_path,
                                           stdout=PIPE, stderr=PIPE)
        async def reader(s, out):
            while True:
                if s.at_eof():
                    break
                stdout = (await s.readline()).decode()
                if stdout:
                    S = "\n".join(stdout.split('\n')[:-1])
                    print(f'{S}', file=out)
                    #flush the output
                    out.flush()

        task = asyncio.create_task(reader(p1.stdout, sys.stdout))
        task2 = asyncio.create_task(reader(p1.stderr, sys.stderr))
        asyncio.gather(task, task2)

        await p1.wait()

        return p1.returncode

startRobot(PythonRobot)
