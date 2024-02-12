from celery import Celery
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.llms import AI21
import os
from langchain.prompts import PromptTemplate

# Set AI21 API key from environment variable
os.environ["AI21_API_KEY"] = "*******************************"
# Create an instance of the AI21 language model (LLM)
llm = AI21(ai21_api_key=os.environ.get('AI21_API_KEY'))

# Set up Wikipedia API wrapper with specified parameters
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# Create a WikipediaQueryRun tool using the API wrapper
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
# Define a list of tools (in this case, only one tool - WikipediaQueryRun)
tools = [tool]

# Define a prompt template for agent interactions
prompt = PromptTemplate.from_template(
    """after careful searching using relevant tools and once 
    finished complete execution, give the user a final response with 
    a minimum of 20 words including all relevant details from previous 
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

# Create a language processing agent using the AI21 LLM, tools, and prompt
agent = create_react_agent(llm, tools, prompt)

# Create an AgentExecutor for handling agent interactions
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# Set up Celery for asynchronous task processing
celery = Celery('celery_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Configure Celery settings
celery.conf.update(
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TASK_RESULT_EXPIRES=40
)

# Celery task for processing user requests
@celery.task
def process_request_task(user_input):
    try:
        # Invoke the agent to process the user input
        response = agent_executor.invoke({"input": user_input})
        return {"response": response}
    except Exception as e:
        # Return an error response if processing fails
        return {"error": str(e)}
