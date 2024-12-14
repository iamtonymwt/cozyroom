# CoZY Room

A Psychological Guidance and RAG based Chatbot
CSC 2526 Project By Angela and Tony @ UofT

## Explannation Video:
<iframe width="560" height="315" src="https://www.youtube.com/embed/Tc8CNeqy3yo" 
frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen></iframe>


## System Overview:
1. Front End: Streamlit
2. Back End
   1. speech-to-text (STT)
   2. OpenAI API
   3. LangChain(Summary, Retreival)
   4. VectorDB: Chroma
   5. text-to-speech


## Env Preparation:
- Python 3.10
- Necessary Packages

## Running:
1. create a **key.py** file and paste there your *OPENAI_API_KEY*. The content of the **.env** should be identical to:
    ```py
    OPENAI_API_KEY='sk-xxxx'
    ```
2. Run the app using the command:
    ```py
    streamlit run app.py
    ```