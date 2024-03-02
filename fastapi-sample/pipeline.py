from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

model = ChatOpenAI()

template = """
You are a helpful assitant please answer the following:

{question}
"""

def make_chain():
    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    return chain