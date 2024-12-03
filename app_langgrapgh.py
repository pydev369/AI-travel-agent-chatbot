import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.utilities import OpenAPISpec
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langgraph import StateGraph, AgentState
from datetime import datetime


# Initialize LangChain Model
model = ChatOpenAI(temperature=0.5)

# Define LangGraph Functions
def check_flights(state):
    if not state["destination"] or not state["dates"]:
        return False
    return True

def check_sightseeing(state):
    if not state["destination"]:
        return False
    return True

# Create StateGraph
graph = StateGraph(AgentState)
graph.add_node("get_flights", check_flights)
graph.add_node("get_sightseeing", check_sightseeing)
graph.add_conditional_edges(
    "get_flights",
    lambda state: state["destination"] and state["dates"],
    {True: "get_sightseeing", False: "get_flights"}
)
graph.set_entry_point("get_flights")
compiled_graph = graph.compile()


# Streamlit App
st.title("AI Travel Agent 🌍")
st.write("Plan your trips with personalized suggestions for flights, sightseeing, and more!")

# User Inputs
destination = st.text_input("Enter your destination:")
dates = st.text_input("Enter your travel dates (YYYY-MM-DD to YYYY-MM-DD):")
preferences = st.text_area("Enter your preferences (e.g., food, adventure):")

# Validate Inputs
if not destination:
    st.warning("Please provide a destination.")
if not dates:
    st.warning("Please provide travel dates.")
if destination and dates:
    try:
        start_date, end_date = map(lambda x: datetime.strptime(x.strip(), '%Y-%m-%d'), dates.split("to"))
        if start_date > end_date:
            st.error("End date must be after start date.")
    except ValueError:
        st.error("Please enter dates in YYYY-MM-DD to YYYY-MM-DD format.")

# Verbose Prompt
if st.button("Plan My Trip"):
    if not destination or not dates:
        st.error("Please complete all fields before proceeding.")
    else:
        # Generate Prompt
        prompt = f"""
        Plan a trip to {destination} between {dates}. Include:
        - Flights
        - Top sightseeing spots
        - Travel tips based on the user's preferences: {preferences}.
        """
        response = model(prompt)
        st.write("### Your Personalized Travel Plan:")
        st.write(response)

# Dockerize Instructions
st.write("To deploy, create a `Dockerfile` with Streamlit and LangChain dependencies.")
