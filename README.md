# CoZY Room
1. Front End: Streamlit
2. Back End
   1. speech-to-text (STT)
   2. OpenAI API
   3. LangChain(Summary, Retreival)
   4. VectorDB: Chroma
   5. text-to-speech


## Usage
- Python 3.10
- Necessary Packages

## Streamlit Usage
Having done the previous steps, it's time to chat. Follow the following steps, please.

1. create a **.env** file and paste there your *OPENAI_API_KEY*. The content of the **.env** should be identical to:
    ```py
    OPENAI_API_KEY=sk-xxxx
    ```


2. Run the app using the command:
    ```py
    streamlit run app.py
    ```