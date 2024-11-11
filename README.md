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

1. create a **key.py** file and paste there your *OPENAI_API_KEY*. The content of the **.env** should be identical to:
    ```py
    OPENAI_API_KEY='sk-xxxx'
    ```


2. Run the app using the command:
    ```py
    streamlit run app.py
    ```