from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constant import WORKDIR
from config.docker_executer_config import docker_executer

def codeExecuter():
    docker = docker_executer()
    code_executer_agent = CodeExecutorAgent(
        name='code_executer_agent',
        code_executor=docker
    )
    return code_executer_agent,docker 