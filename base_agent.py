from celery import Celery
from langchain.agents import AgentExecutor,create_react_agent
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.llms import AI21
import os
from langchain.prompts import PromptTemplate

os.environ["AI21_API_KEY"] = "tsvATwIXwXIhlKujLwgyCeebJWXcGs80"
llm = AI21(ai21_api_key=os.environ.get('AI21_API_KEY'))

api_wrapper = WikipediaAPIWrapper(top_k_results=1, 
                                  doc_content_chars_max=100)

tool = WikipediaQueryRun(api_wrapper=api_wrapper)
tools = [tool]

prompt = PromptTemplate.from_template(
    """after carefull searching using relevent tools and once 
    finished complete execution ,give user final response with 
    minimum of 20 words including all relevent details from prevoius 
    chains. You have access to the following tools:
    
    tools: {tools}
    
    Use the following format:

    Question: the input question you must answer
    
    Thought: you should always think about what to do
    
    Action: the action to take, should be one of [{tool_names}]
    
    Action Input: the input to the action
    
    Observation: the result of the action
    
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    
    Thought: I now know the final answer
    
    Final Answer: the final answer to the original input question
    
    Begin!

    Question: {input}
    
    Thought:{agent_scratchpad} """)

agent = create_react_agent(llm, 
                            tools, 
                            prompt)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

celery = Celery(
    'celery_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TASK_RESULT_EXPIRES=40
)

@celery.task
def process_request_task(user_input):
    try:
        response = agent_executor.invoke({"input": user_input})
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}