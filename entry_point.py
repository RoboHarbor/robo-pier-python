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

    def _stream_thread(self, stream, handler):
        print("stream_thread "+str(stream))
        for line in stream:
            handler(line.rstrip())
        stream.close()

    def stream_command(
            self,
            args,
            stdout_handler=logging.info,
            stderr_handler=logging.error,
            check=True,
            text=True,
            stdout=PIPE,
            stderr=PIPE,
            cwd=None,
            **kwargs,
    ):
        """Mimic subprocess.run, while processing the command output in real time."""
        with Popen(" ".join(args), text=text, stdout=stdout, stderr=stderr, cwd=cwd, shell=True, **kwargs) as process:
            if stdout_handler:
                print("stdout_handler")
                stdout_thread = threading.Thread(
                    target=partial(self._stream_thread, process.stdout, stdout_handler)
                )
                stdout_thread.start()
            if stderr_handler:
                print("stderr_handler")
                stderr_thread = threading.Thread(
                    target=partial(self._stream_thread, process.stderr, stderr_handler)
                )
                stderr_thread.start()
            process.wait()
            print("process.wait()")
            if stdout_handler:
                stdout_thread.start()
            if stderr_handler:
                stderr_thread.start()
            if check and process.returncode != 0:
                raise CalledProcessError(process.returncode, process.args)
            return CompletedProcess(process.args, process.returncode, None, None)

    async def run(self):
        python_version = "3.9"
        if self.get_config_value('pythonVersion') is not None:
            python_version = self.get_config_value('pythonVersion')
        print("Python version: ", python_version)

        full_app_path = os.path.abspath(self.get_app_dir())

        try:
            print("Installing requirements")
            subprocess.run("pyenv local "+python_version+" && python -m pip install -r requirements.txt ",
                                        cwd=full_app_path,
                                        shell=True)

        except Exception as e:
            print("Error: ", str(e))

        script = self.get_config_value('script')
        print("Running script: ", script)
        rc = self.stream_command(
            ["pyenv", "local", python_version, " && ", "python", script],
            cwd=full_app_path,
            stdout_handler = print,
            stderr_handler = print
        )

        if rc.returncode != 0:
            print("Error: ", rc)

        return rc

startRobot(PythonRobot)
