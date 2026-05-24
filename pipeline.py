from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain

def run_research_pipeline(topic :str) -> dict:
    state={}

    # Search Agent
    print("\n"+"="*50)
    print("Running Search Agent...")
    print("="*50)

    search_agent = build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and relevant information on the topic: {topic}")]
    })

    state["search_result"]=search_result["messages"][-1].content
    print("\nSearch Results:\n",search_result)


    # Reader Agent
    print("\n"+"="*50)
    print("Running Reader Agent...")
    print("="*50)

    scrape_agent = build_scrape_agent()
    scrape_result=scrape_agent.invoke({
        "messages":[("user",
        f"Based on the following search results about '{topic}'," 
        f"pick the most relevant URL and Scrape it for deeper content.\n\n"       
        f"Search Results:\n {state['search_result'][:800]}")]
    })

    state["scrape_result"]=scrape_result["messages"][-1].content
    print("\nScraped Results:\n",scrape_result)

    
    # Writer Chain
    print("\n"+"="*50)
    print("Running Writer Chain...")
    print("="*50)

    research_combined=(
        f"Search Results:\n{state['search_result']}\n\n"
        f"Scraped Content:\n{state['scrape_result']}"
    )

    writer_chain.invoke(
        {
            "topic":topic,
            "research":research_combined
        }
    )

    state["report"]=writer_chain.invoke(
        {
            "topic":topic,
            "research":research_combined
        }
    )

    print("\nFinal Report:\n",state["report"])


    # Critic Chain
    print("\n"+"="*50)
    print("Running Critic Reviewing the Report...")
    print("="*50)

    state["Feedback"]=critic_chain.invoke({
        "report":state["report"]
    })
    print("\n Critic Report \n",state["Feedback"])

    
    return state

if __name__=="__main__":
    topic=input("Enter a research topic: ")
    run_research_pipeline(topic)
