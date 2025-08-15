import streamlit as st
from team.dsa_team import dsa_team
from config.docker_utils import start_docker,stop_docker
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

st.title("Data Structures and Algorithm Solver")
st.write("Welcome to Algogenie, your personal DSA problem solver! Here you" \
"can ask solutions for variosu data structures and algorithm problems.")

task = st.text_input("Enter your DSA problem and question", value='write a function for adding two numbers')

async def run(team,docker,task):
    await start_docker(docker)

    try:

        async for message in team.run_stream(task=task):
            if isinstance(message,TextMessage):
                print(msg:= f"{message.source} : {message.content}")
                yield msg
            elif isinstance(message,TaskResult):
                print(msg:= f"Stop reason : ,{ message.stop_reason}")
                yield msg
        
        print("Task completed")
        
    except Exception as e:
        print(f"Error: ", e)
        yield f"Error: {e}"
    finally:
        await stop_docker(docker)


if st.button("Run"):
    st.write("Task is running.......")

    team,docker = dsa_team()

    async def collect_messages():
        async for msg in run(team,docker,task):
            if isinstance(msg, str):
                if msg.startswith('user:'):
                    with st.chat_message('user',avatar='🫠'):
                        st.markdown(msg)
                elif msg.startswith('DSA_problem_solver_agent'):
                    with st.chat_message('assistant',avatar='👨‍💻'):
                        st.markdown(msg)
                elif msg.startswith('code_executer_agent'):
                    with st.chat_message('assistant',avatar='🤖'):
                        st.markdown(msg)
            elif isinstance(msg,TaskResult):
                with st.chat_message('stopper',avatar='🫡'):
                    st.markdown(f"Task completed : {msg.result}")
    
    asyncio.run(collect_messages())