
 

from langchain_openai import ChatOpenAI

from langchain_community.llms import Ollama 
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import LanceDB
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama 
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

import os
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

debug=False
verbose=False

if os.environ.get("DEBUG", "").lower() == "true":
    debug=True
    verbose=True
    logging.getLogger().setLevel(logging.DEBUG)
    
 

if "OPENAI_API_KEY" not in os.environ:
    print("OPENAI_API_KEY not set")
    os._exit(1)

if "GOOGLE_AI_KEY" not in os.environ:
    print("GOOGLE_API_KEY not set")
    os._exit(1)
    

 
OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
gpt4=ChatOpenAI(openai_api_key=OPENAI_API_KEY,model_name="gpt-4",max_tokens=4000)
gpt3=ChatOpenAI(openai_api_key=OPENAI_API_KEY,model_name='gpt-3.5-turbo-16k',max_tokens=4000)
gemini= ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_AI_KEY"])
llm = gpt3
cliPrompt = 'gpt3> '
    
 

aggregate_input=""
while True:
    # Get the user's input
    user_input = input(cliPrompt)
    if user_input == 'exit':
        print("Exiting program.")
        os._exit(1)

    # Check if the user wants to switch models
    if user_input.startswith('use '):
        model_name = user_input.split(' ')[1]
        if model_name == 'gpt3':
            llm = gpt3
            cliPrompt = 'gpt3> '
        elif model_name == 'gpt4':
            llm = gpt4
            cliPrompt = 'gpt4> '
        elif model_name == 'gemini':
            llm = gemini
            cliPrompt = 'gemini> '
        else:
            print('Unknown model:', model_name)
    elif user_input=="go":
                
        aiPrompt="""Please do a rewrite of the following text. 
        The text is intended for a reasonably tech-literal general audience and is part 
        of a technical blog or article.  Correct any grammatical errors, and change 
        the phrasing to match the language typical of popular technology articles in mainstream journals 
        such as the new york times.  Feel free to change the wording but please preserve the overall sentence structure. 
        Here's the text: """+aggregate_input
        logging.debug(aiPrompt)
 
 
        chain = llm | StrOutputParser()
        logging.debug(chain)
 
        response = chain.invoke(aiPrompt)
 

        # Print the model's response
        print("===============================================")
        print(response)
        print("===============================================")
        aggregate_input=""
    else:
        aggregate_input+=user_input