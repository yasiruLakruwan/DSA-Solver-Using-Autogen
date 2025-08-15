from autogen_agentchat.agents import AssistantAgent
from config.settings import model_client

model_client = model_client()

def DSAAgent():
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
    return DSA_problem_solver_agent
