from langchain.agents import AgentExecutor, create_react_agent 
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from gala_rag import GalaRAG
from gala_tools import get_current_weather # Import your tools
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

load_dotenv()

class AlfredAgent:
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=self.gemini_api_key)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=self.gemini_api_key,
            model="models/gemini-2.5-flash"
        )
        self.gala_rag = GalaRAG(gemini_api_key=self.gemini_api_key)
        self.gala_rag.initialize_vectorstore()
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        # 1. Define the Tools available to Alfred
        tools = [
            self.gala_rag.retrieve_info, # The RAG retrieval function as a tool
            get_current_weather # The weather tool
        ]
        
        # We need to wrap retrieve_info in a tool decorator for the agent to use it
        # LangChain's create_react_agent expects tools that are already Tool objects
        from langchain.tools import Tool
        rag_tool = Tool(
            name="Gala_Information_Retriever",
            func=self.gala_rag.retrieve_info,
            description="""
            Useful for answering questions about the gala, including guest details (interests, background, gossip, fun facts),
            menu items, and the event schedule. Input should be a specific question or keyword related to the gala information.
            """
        )
        
        tools = [rag_tool, get_current_weather] # Update tools list

        # 2. Define the Agent's Prompt
        # This is crucial for guiding the agent's behavior.
        # We use a ReAct style prompt for better reasoning.
        prompt_template = PromptTemplate.from_template(
            """You are Alfred, the ultimate gala host. Your goal is to provide helpful,
            engaging, and accurate information about the gala, its guests, and arrangements.
            
            You have access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            You must adhere to the following guidelines:
            - Be polite, sophisticated, and always in character as a gala host.
            - When asked about guests, share interesting facts, gossip, or background info using the available tools.
            - Avoid discussing politics or religion. If asked about these topics, politely steer the conversation to more appropriate gala topics.
            - Keep an eye on the weather for planning outdoor activities like fireworks.
            - Provide detailed and informative answers.

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}"""
        )

        # 3. Create the Agent
        # create_react_agent creates an agent that uses the ReAct framework.
        agent = create_react_agent(self.llm, tools, prompt_template)

        # 4. Create the Agent Executor
        # This executes the agent's plan, including using tools and interacting with the LLM.
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        return agent_executor

    def run(self, query: str) -> dict: #str:
        
        """
        Runs the agent with the given query and returns the full invocation result.
        """
        
        return self.agent_executor.invoke({"input": query})
        #result = self.agent_executor.invoke({"input": query})
        time.sleep(1.1)  # Add a delay to stay within the free tier (60 requests/minute)
        #return result["output"]

if __name__ == "__main__":
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    alfred = AlfredAgent(gemini_api_key=gemini_api_key)
    print("\n--- Alfred Responds: What's the main course tonight? ---")
    response = alfred.run("What's the main course tonight?")
    print(f"\nAlfred: {response}")

    print("\n--- Alfred Responds: Tell me about Dr. Eleanor Vance. ---")
    response = alfred.run("Tell me about Dr. Eleanor Vance.")
    print(f"\nAlfred: {response}")

    print("\n--- Alfred Responds: Is it a good time for fireworks in London? ---")
    response = alfred.run("Is it a good time for fireworks in London?")
    print(f"\nAlfred: {response}")

    print("\n--- Alfred Responds: What do you know about Professor Aris Thorne's hobbies? ---")
    response = alfred.run("What do you know about Professor Aris Thorne's hobbies?")
    print(f"\nAlfred: {response}")

    print("\n--- Alfred Responds: What is the meaning of life? ---") # Testing guideline adherence
    response = alfred.run("What is the meaning of life?")
    print(f"\nAlfred: {response}")
    
    