import streamlit as st
from team.dsa_team import dsa_team
from config.docker_utils import start_docker,stop_docker
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

st.title("Data Structures and Algorithm Solver")
st.write("Welcome to Algogenie, your personal DSA problem solver! Here you" \
"can ask solutions for variosu data structures and algorithm problems.")

task = st.text_input("Enter your DSA problem and question")

async def run(team,docker,task):
    await start_docker(docker)

    async for message in team.run_stream(task=task):
        if isinstance(message,TextMessage):
            print(msg:= f"{message.source} : {message.content}")
            yield msg
        elif isinstance(message,TaskResult):
            print(msg:= f"Stop reason : ,{ message.stop_reason}")
            yield msg
    
    print("Task completed")
    await stop_docker(docker)


if st.button("Run"):
    st.write("Task is running.......")

    team,docker = dsa_team()

    async def collect_messages():
        async for msg in run(team,docker,task):
            if isinstance(msg, str):
                st.markdown(msg)
            elif isinstance(msg,TaskResult):
                st.markdown(f"Stop Reason : {msg.stop_reason}")
    
    asyncio.run(collect_messages())