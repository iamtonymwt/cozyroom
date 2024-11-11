import os
from glob import glob

import openai
from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

from key import OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] =  OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY


SYSTEM_PROMPT = "You are a student stress relief assistant. Your goal is to use your own words and stories to keep chatting with the user and help them feel better. You have to remember these chatting paradigms and generate your words:\n1. Active Listening: Encourage individuals to express their emotions without judgment, and offer validation by reflecting back on what they are saying to show empathy.\n2. The experience and effects of emotional support: Use empathetic communication, gentle reassurance, and emotional validation when offering support to someone stressed.\n3. Peer support: Make yourself a supportive peer, emphasizing shared experiences to create emotional bonds that help reduce stress."


def base_model_chatbot(messages):
    system_message = [
        {"role": "system", "content": SYSTEM_PROMPT}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1,
        messages=messages
    )
    return response.choices[0].message.content


class VectorDB:
    """Class to manage document loading and vector database creation."""
    
    def __init__(self, docs_directory:str):

        self.docs_directory = docs_directory

    def create_vector_db(self):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

        files = glob(os.path.join(self.docs_directory, "*.pdf"))

        loadPDFs = [PyPDFLoader(pdf_file) for pdf_file in files]

        pdf_docs = list()
        for loader in loadPDFs:
            pdf_docs.extend(loader.load())
        chunks = text_splitter.split_documents(pdf_docs)
            
        return Chroma.from_documents(chunks, OpenAIEmbeddings()) 
    
class ConversationalRetrievalChain:
    """Class to manage the QA chain setup."""

    def __init__(self, model_name="gpt-4o-mini", temperature=1):
        self.model_name = model_name
        self.temperature = temperature
      
    def create_chain(self):

        model = ChatOpenAI(model_name=self.model_name,
                           temperature=self.temperature,
                           )

        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
            )
        vector_db = VectorDB('docs/')
        retriever = vector_db.create_vector_db().as_retriever(search_type="similarity",
                                                              search_kwargs={"k": 2},
                                                              )
        # retriever = vector_db.create_vector_db().as_retriever(search_type="similarity_score_threshold",
        #                                                       search_kwargs={'score_threshold': 0.2},
        #                                                       )

        return RetrievalQA.from_chain_type(
            llm=model,
            retriever=retriever,
            memory=memory,
            )
    
def with_pdf_chatbot(messages):
    """Main function to execute the QA system."""
    query = messages[-1]['content'].strip()

    qa_chain = ConversationalRetrievalChain().create_chain()

    result = qa_chain({"query": query})
    return result['result']