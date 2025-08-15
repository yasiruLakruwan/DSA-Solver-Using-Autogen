from autogen_agentchat.messages import TextMessage 
from config.docker_utils import start_docker,stop_docker
from team.dsa_team import dsa_team
from autogen_agentchat.base import TaskResult
import asyncio

async def main():
    team,docker = dsa_team()

    try:
        await start_docker(docker)
         
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
       await stop_docker(docker)

if __name__ == "__main__":
    asyncio.run(main())