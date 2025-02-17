from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from groq import Groq
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__,template_folder="templates")

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "medichatbot"

# embed each chunk and upset the embeddings into the pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

retriever = docsearch.as_retriever(search_type="similarity",search_kwargs={"k":3})

system_prompt = (
    "you are an assistant for question-answering tasks."
    "Use the following pieces of retrieved context to answer"
    "the question. if you don't khnow the answer , say that you"
    "don't know. Use three sentences maximum and keep the"
    "answer concise."
    "\n\n"
    "{context}"

)

llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human","{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt) # had fonction khasa tkhdem ila khdmat safi kolxi mzyan
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET" , "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input":msg})
    print("response : ",response["answer"])
    return str(response["answer"])



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)

