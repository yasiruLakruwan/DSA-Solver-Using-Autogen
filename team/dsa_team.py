from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMessageTermination
from config.constant import TEXT_MENTION,MAX_TERNS
from agents.code_executer_agent import codeExecuter
from agents.problem_solver_agent import DSAAgent

def dsa_team():

    termination_condition = TextMessageTermination(TEXT_MENTION)

    problem_solver = DSAAgent()
    code_executer,docker = codeExecuter()

    team = RoundRobinGroupChat(
        participants=[problem_solver,code_executer],
        termination_condition=termination_condition,
        max_turns=MAX_TERNS
    )    

    return team,docker   