from autogen_agentchat.agents import CodeExecutorAgent
import asyncio
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage 
from autogen_core import CancellationToken
import os
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
from autogen_agentchat.base import TaskResult

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gemini-1.5-flash-8b', api_key=api_key)
async def main():

    docker = DockerCommandLineCodeExecutor(
        work_dir='/tmp',
        timeout=200
    )

    code_executer_agent = CodeExecutorAgent(
        name='code_executer_agent',
        code_executor=docker
    )

    DSA_problem_solver_agent = AssistantAgent(
        name="DSA_problem_solver_agent",
        description="An agent that solves DSA problem",
        model_client=model_client,
        system_message='''
           You are a DSA problem solver agent working with a CodeExecutorAgent.

            When given a task:
            1. First, clearly state your PLAN to solve the problem in numbered steps.
            2. Then, provide exactly ONE Python code block containing the implementation.
            - The code must be self-contained, runnable as-is, and print the outputs.
            3. Do not explain the code before execution. Only send the code block to the CodeExecutorAgent for execution.
            4. After receiving execution results from the CodeExecutorAgent:
            - Explain the results concisely.
            - If the results match expectations, say "STOP" to end the conversation.
            - If there is an error, update the code and retry from step 2.

        '''
    ) 

    termination_condition = TextMentionTermination("STOP")

    team = RoundRobinGroupChat(
        participants=[DSA_problem_solver_agent,code_executer_agent],
        termination_condition=termination_condition,
        max_turns=10
    )
    
    try:
        await docker.start()
        task = "Write a python code to sum two numbers."
        
        async for message in team.run_stream(task=task):
           if isinstance(message,TextMessage):
               print("==" * 20)
               print(message.source," :", message.content)
           elif isinstance(message,TaskResult):
               print('Stop reason : ', message.stop_reason)
    
    except Exception as e:
        print("Error",e) 
    finally:
        await docker.stop()

if __name__ == "__main__":
    asyncio.run(main())

