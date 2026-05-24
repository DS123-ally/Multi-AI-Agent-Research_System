from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=1024,
)

AGENT_CONFIG = {"recursion_limit": 10}

# Keep downstream prompts within Groq free-tier TPM (~6000/min)
MAX_RESEARCH_CHARS = 2500
MAX_REPORT_CHARS = 3500
STEP_COOLDOWN_SEC = 3

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a research search agent. Always call web_search with a focused query. "
            "Summarize findings with titles, URLs, and key facts."
        ),
    )

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a content reader agent. Pick the best URL from the user's context "
            "and call scrape_url to extract detailed text. Summarize the scraped content."
        ),
    )

# Writer Chain 

writer_prompt=ChatPromptTemplate.from_messages([
    ("system","You are an expert writer.Write clear,structured and insightful report"),
    ("human","""Write a detailed research report on the topic below.
     
    Topic: {topic}

    Research Gathered:
    {research}
     
    Structure the report as follows:
    - Introduction
    - Key Finding (minimum 5 well-explained points)
    - Conclusion
    - Sources (list all URL's found in the research) 
     
    Ensure the report is comprehensive and well-organized and professional.""")
])

writer_chain =writer_prompt | llm | StrOutputParser() 

# Critic Chain

critic_prompt=ChatPromptTemplate.from_messages([
    ("system","You are an expert critic. Evaluate the following research report for accuracy, clarity, and completeness."),
    ("human","""Evaluate the research report below for accuracy, clarity, and completeness.

    Report:
    {report}
     
    Respond in this exact format:

    Score: X/10
     
    Strengths:
    - List the strengths of the report here.
    
    Areas for Improvement:
    - List the areas where the report can be improved here.
     
    Overall Feedback:
    - Provide overall feedback on the report here.
  """),
])

critic_chain = critic_prompt | llm | StrOutputParser()


