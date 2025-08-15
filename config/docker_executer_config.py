from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constant import WORKDIR,TIME_OUT

def docker_executer():
    
    docker = DockerCommandLineCodeExecutor(
            work_dir = WORKDIR,
            timeout = TIME_OUT
        )
    return docker