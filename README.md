# **Alfred the Gala Host: An Agentic RAG System 🎩✨**

## **Project Overview**

Welcome to "Alfred the Gala Host," an innovative project demonstrating the power of **Agentic Retrieval Augmented Generation (RAG)** in a real-world scenario. This system creates an intelligent AI assistant, Alfred, designed to manage and enhance a grand gala event. Alfred can answer intricate questions about guests, event schedules, menus, and even provide real-time weather updates, acting as the ultimate digital concierge.

This project serves as a comprehensive example of building a multi-tool AI agent using modern LLM orchestration frameworks, showcasing a practical application of advanced AI concepts for event management and intelligent information retrieval.

## **The Challenge: A Gala to Remember**

Imagine hosting the most opulent party of the century. As the esteemed host, you need to ensure every detail is perfect, every guest is delighted, and every unforeseen circumstance is elegantly handled. This is where Alfred comes in. Our AI agent needs access to a vast array of information—from guest biographies and interests to the evening's meticulously planned schedule and dynamic weather forecasts.

Alfred's core responsibilities include:

* **Guest Engagement**: Answering questions about attendees, sharing intriguing anecdotes, and facilitating connections.  
* **Event Information**: Providing details on the menu, entertainment, and the evening's flow.  
* **Situational Awareness**: Offering real-time weather updates crucial for outdoor events like a grand fireworks display.  
* **Etiquette Adherence**: Maintaining a sophisticated tone and avoiding sensitive topics like politics or religion.

This project addresses these challenges by empowering Alfred with an Agentic RAG architecture, enabling him to intelligently retrieve and synthesize information from diverse sources.

## **Features**

* **Intelligent Information Retrieval**: Uses RAG to query structured and unstructured data about guests, menu, and schedule.  
* **Real-time Weather Updates**: Integrates with a public weather API (Open-Meteo.com) to provide current conditions.  
* **Agentic Reasoning**: Leverages the ReAct (Reasoning and Acting) framework, allowing Alfred to thoughtfully plan actions, use tools, and arrive at well-reasoned answers.  
* **Configurable LLM Integration**: Built with LangChain, allowing flexible integration with various Large Language Models (LLMs) like OpenAI's GPT series.  
* **Modular Design**: Clearly separated components for data loading, RAG, tools, and agent orchestration.  
* **Sophisticated Persona**: Alfred is programmed to maintain a polite, sophisticated, and informative persona befitting a gala host.

## **Technical Architecture**

Alfred's intelligence stems from a combination of several key components:

1. **Large Language Model (LLM)**: The "brain" of Alfred, responsible for understanding natural language queries, reasoning, and generating coherent responses. (e.g., OpenAI's GPT-4).  
2. **Retrieval Augmented Generation (RAG)**: A system that augments the LLM's knowledge with external, up-to-date information.  
   * **Data Sources**: Our "gala knowledge base" including guests.json, menu.md, and schedule.md.  
   * **Text Splitters**: Breaks down large documents into smaller, manageable chunks suitable for embedding.  
   * **Embeddings**: Converts text chunks into numerical vectors, capturing their semantic meaning.  
   * **Vector Store (FAISS)**: An efficient database for storing and performing rapid similarity searches on these embeddings, allowing Alfred to find relevant information quickly.  
   
3. **Tools**: External functions Alfred can call to perform specific actions or fetch real-time data.  
   * Gala\_Information\_Retriever: A custom tool wrapping the RAG system, allowing Alfred to query his internal knowledge base.  
   * get\_current\_weather: A tool that fetches real-time weather data from Open-Meteo.com.  
   
4. **Agent Orchestration (LangChain)**: The framework that ties everything together. It enables Alfred to:  
   * **Perceive**: Understand the user's query.  
   * **Reason**: Use the ReAct prompting strategy to think step-by-step (Thought:).  
   * **Act**: Choose the appropriate tool (Action:), provide the correct input (Action Input:), and execute it.  
   * **Observe**: Process the tool's output (Observation:).  
   * **Respond**: Generate a final, informed answer (Final Answer:).  
 

This architecture allows Alfred to go beyond the static knowledge of his LLM, providing dynamic, context-aware, and accurate responses.


![Generated Image September 05, 2025 - 5_43AM](https://github.com/user-attachments/assets/5f93febc-8588-464c-9f3f-9e5d451e5f15)

*Conceptual diagram illustrating Alfred's Agentic RAG architecture: The user query goes to the LLM agent, which uses its reasoning capabilities to decide whether to query the vector store via RAG or use external tools like the weather API, before synthesizing a final answer.*

## **Web Interface (Streamlit)**

To provide a more natural and engaging interaction with Alfred, a user-friendly web interface has been developed using **Streamlit**. This allows users to chat with Alfred as they would with a typical AI assistant, making the project highly accessible and demonstrating practical application.

### **Interface Features:**

* **Interactive Chat Window**: A familiar chat-based interface for sending queries and receiving Alfred's responses.  
* **Persistent Session History**: Remembers past interactions within a single browser session.  
* **Elegant Design**: Simple, clean, and intuitive UI, embodying the sophistication of the gala host.  
* **Real-time Feedback**: Displays a "Alfred is thinking..." spinner while processing requests.

### **How to use the Web Interface:**

1. Ensure your virtual environment is active.  
2. Navigate to the project's root directory in your terminal.  
3. Run the Streamlit application:  
4. codeBash  
5. streamlit run app.py  
6. Your default web browser will open, displaying the chat interface (usually at http://localhost:8501).  
7. Type your questions into the input box and press Enter to interact with Alfred\!

<img width="1633" height="740" alt="Screenshot 2025-09-05 3 40 54 PM" src="https://github.com/user-attachments/assets/a852012f-f048-4571-a93f-c770fadfa273" />


*A screenshot of Alfred's Streamlit web interface, showing a typical chat interaction with the user asking about a guest's interests.*
