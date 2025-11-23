from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END;
import psycopg as psql
from typing import TypedDict, Literal


connection = psql.connect("host=database password=senha123 user=postgres")

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
prompts = ["I want to create a table called students that will have an id, name and age", "I want to insert a student called lucas, age 21 into the table students", "i want to see all data from my table students"]

class PromptType(TypedDict):
    type: Literal['sql_command', 'non_sql']
    sql: Literal['select', 'insert', 'create', 'drop']

class MyState(TypedDict):
    prompt: str
    classification: PromptType
    count:int


def input_node(state: MyState):
    #user = input("Type the prompt: ")
    state["prompt"] = model.invoke(prompts[state["count"]]).content
    return state

def router(state: MyState):
    classification_prompt = f"""User prompt: {state["prompt"]}\nIf the user says something that can be perfomed by a SQL command, classify it as 'sql_command', but if the prompt does not give enough information to perform the action as SQL command, classify it as 'non_sql'. If it is a SQL COMMAND, classify it as select, insert, create or drop."""
    model_classifier = model.with_structured_output(PromptType)
    state['classification'] = model_classifier.invoke(classification_prompt)
    print(f"Classified as: {state['classification']}\n")
    return state
    
def sql_node(state: MyState):
    print("Just got in SQL_NODE!\n")
    sql_prompt = f"""User prompt: {state['prompt']}\nReturn only the SQL command that translates what the user is asking for, formatted in the exact and correct way for a POSTGRESQL command.\n"""
    sql_command = model.invoke(sql_prompt).content

    state["count"] = state["count"] + 1

    cursor = connection.cursor()
    sql_command_formatted = sql_command.replace("sql", "")
    sql_command_formatted = sql_command_formatted.replace("`", "")
    
    command = cursor.execute(sql_command_formatted)
    if(state["classification"]["sql"] == 'select'):
        for record in cursor:
            print(record)

    connection.commit()
    return state




graph = StateGraph(state_schema=MyState)

graph.add_node("input_node", input_node)
graph.add_node("router", router)
graph.add_node("sql_node", sql_node)

graph.add_edge(START, "input_node")
graph.add_edge("input_node", "router")
graph.add_conditional_edges("router", lambda state:state['classification']['type'], {'sql_command':'sql_node', 'non_sql':END})
graph.add_edge("sql_node", "input_node")


graph = graph.compile()
graph.invoke({"count":0})
