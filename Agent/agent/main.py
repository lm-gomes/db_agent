from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END;
import psycopg as psql
from typing import TypedDict, Literal


connection = psql.connect("host=database password=senha123 user=postgres")

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class Classification(TypedDict):
    classification: Literal['sql_command', 'non_sql']

class MyState(TypedDict):
    prompt: str


def input_node(state: MyState):
    #user = input("Type the prompt: ")
    state["prompt"] = model.invoke("I want to see all data of a table called students").content
    
    return state

def router(state: MyState):
    classification_prompt = f"""User prompt: {state["prompt"]}\nIf the user says something that can be perfomed by a SQL command, classify it as 'sql_command', but if the prompt does not give enough information to perform the action as SQL command, classify it as 'non_sql' """
    model_classifier = model.with_structured_output(Classification)
    classification = model_classifier.invoke(classification_prompt)
    print(f"Classified as: {classification['classification']}\n")
    return classification
    
def select_node(state: MyState):
    cursor = connection.cursor()

    cursor.execute(f"""CREATE TABLE test()""")



graph = StateGraph(state_schema=MyState)

graph.add_node("input_node", input_node)
graph.add_node("router", router)

graph.add_edge(START, "input_node")
graph.add_edge("input_node", "router")
graph.add_edge("router", END)

graph = graph.compile()
graph.invoke({})
