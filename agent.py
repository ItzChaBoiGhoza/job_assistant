from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

def create_job_agent(api_key):
    
    model = ChatAnthropic(
        model='claude-sonnet-4-6',
        temperature=0,
        api_key=api_key,
    )

    agent = create_agent(
        model=model,
        tools=[],
        system_prompt='You are an experienced career coach.'
    )
    
    return agent