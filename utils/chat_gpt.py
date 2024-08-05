from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.memory import VectorStoreRetrieverMemory
from dotenv import load_dotenv
import pinecone
import os

from utils.manage_pics import CeterniImage

load_dotenv()

OPENAI_API_TOKEN = os.getenv("OPENAI_API_TOKEN")
PINECONE_API_TOKEN = os.getenv("PINECONE_API_TOKEN")


def get_question_score(question, answer, options) -> int:
    """Classifies the sentiment of a conversation."""

    default_prompt = """Está es una conversación entre un humano y un asistente.
    El humano esta contestando a la pregunta: {question}
    Su respuesta es: {answer}
    Puntúa la respuesta de acuerdo a las siguientes opciones: {options}
    Only return a number.
    Puntuación:"""

    prompt = PromptTemplate(
        input_variables=["question", "answer", "options"],
        template=default_prompt,
    )

    chat_prompt = prompt.format(question=question, answer=answer, options=options)

    llm = OpenAI(
        openai_api_key=OPENAI_API_TOKEN,
        temperature=0.0,
    )

    res = llm.predict(text=chat_prompt)
    print(f"The score of the answer is: {res}")

    return int(res)


class CeterniChat:
    """Class to test the chatbot."""

    def __init__(self):
        # Initiate Pinecone index
        pinecone.init(api_key=PINECONE_API_TOKEN, environment="gcp-starter")
        index_name = "hackathon"

        embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_TOKEN,
        )

        memory_index = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embeddings,
        )

        retriever = memory_index.as_retriever()

        memory = VectorStoreRetrieverMemory(
            retriever=retriever,
        )

        llm = OpenAI(
            openai_api_key=OPENAI_API_TOKEN,
            temperature=1.1,
        )

        _DEFAULT_TEMPLATE = """You are an emotional assistant to help adolescents with their problems.
            You are talkative and provide lots of specific details from your context.
            If you do not know the answer to a question, you give emotional support.
            You are a good listener and you are empathetic.
            Answer to the human talking to you and have a conversation with them.
            Only answer to the human's messages as if you were the assistant.
            Do not complete or hallucinate the human's sentences.
            Do your best to answer the questions.
            Try to add emojis in any part of your response.
            Never say you are a robot or anything related to it.

            Relevant pieces of previous conversation:
            {history}

            (You do not need to use these pieces of information if not relevant)

            Current conversation:
            Human: {input}
            AI:
            """

        prompt = PromptTemplate(
            input_variables=["history", "input"], template=_DEFAULT_TEMPLATE
        )

        self.conversation_with_summary = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            verbose=True,
        )

    def conversation(self, message: str) -> str:
        """Returns a string with the response from the chatbot."""

        image = CeterniImage()

        emotion = image.detect_emotion(message)
        gif_data = image.handle_emotion(emotion)

        response = self.conversation_with_summary.predict(input=message)

        return response, gif_data
