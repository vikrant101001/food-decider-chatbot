#The only Imports
import streamlit as st
import openai
from swarm import Swarm, Agent



# Define agents and transfer functions
def transfer_to_budgeter():
    return budgeter

def transfer_to_choser():
    return choser

def transfer_to_orderer():
    return orderer

def transfer_to_triage():
    return triage_agent

budgeter = Agent(
    name="budgeter",
    instructions="""
    You are a helpful agent who helps with planning the budget for your food order. Always begin sentence with 'Agent Budgeter : '
    You have knowledge regarding the prices of the available food:(in rupees)
    1. Momos: 150
    2. Pizza: 200
    3. Chicken Steak: 250
    4. Indian Chicken Meal: 200
    5. Indian Veg Meal: 150
    6. Pasta: 150
    7. Burger: 150
    8. Chinese chicken Meal: 150
    9. Chinese Veg Meal: 100
    
    """,
    functions=[transfer_to_triage],
)

choser = Agent(
    name="choser",
    instructions="""
    You are a helpful agent who helps with choosing what kind of food you would like to have today. Always begin sentence with 'Agent Chooser : '
    You have knowledge regarding the availability of food in the nearby stores.
    Available Catalogue:
    1. Momos
    2. Pizza
    3. Chicken Steak
    4. Indian Chicken Meal
    5. Indian Veg Meal
    6. Pasta
    7. Burger
    8. Chinese chicken Meal
    9. Chinese Veg Meal

    You should ask the user what kind of food they would like to have : chinese, italian,etc

    """,
    functions=[transfer_to_triage],
)

orderer = Agent(
    name="orderer",
    instructions="""
    You are a helpful agent who helps confirm the order and prints the order details properly. Always begin sentence with 'Agent Orderer : '
    You have knowledge regarding the availability of food in the nearby stores along with the name of the store.
    Available Catalogue:
    1. Momos : A1 food park
    2. Pizza : A1 food park
    3. Chicken Steak : Eat Well Plaza
    4. Indian Chicken Meal : Eat Well Plaza
    5. Indian Veg Meal : Eat Well Plaza
    6. Pasta : Italiano cafe
    7. Burger : Burger Queen
    8. Chinese chicken Meal : Spicy Wok
    9. Chinese Veg Meal : Spicy Wok

    You also know that the delivery charges are free and there is 5 % tax on the food and are very good at generating a receipt once order is completed.
    """,
    functions=[transfer_to_triage],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    Determine which agent is best suited to handle the user's request, and transfer the conversation to that agent. Always begin sentence with 'Agent Triage : '

    """,
    functions=[transfer_to_choser, transfer_to_budgeter, transfer_to_orderer],
)


# Initialize Streamlit chat interface
st.title("Food Decider Chatbot - OpenAI Swarm")
st.caption("This is an example multi Agent Chatbot built using OPENAI Swarm(experimental). For more info open the left sidebar")

# Sidebar for agent descriptions
with st.sidebar:
    st.header("OpenAI API Key")
    api_key = st.text_input("Paste your OpenAI API key here:", type="password")  # Hide input
    if api_key:
        openai.api_key = api_key
    else:
        st.warning("Please enter your OpenAI API key.")
            
    st.markdown("### OpenAI Swarm Agents")
    st.markdown("**Triage Agent**")
    st.caption("This agent is the main agent which is the part and parcel of OPENAI SWARM which chooses the appropriate agent for the task.")
    
    st.markdown("**Chooser Agent**")
    st.caption("This agent helps the user choose the food they would like to have.")
    
    st.markdown("**Budgeter Agent**")
    st.caption("This agent helps the user decide the food based on the budget.")
    
    st.markdown("**Orderer Agent**")
    st.caption("This agent helps the user finalize the order, place it, and print the receipt.")
    
    st.markdown("---")
    st.write("**Note:** [Click here](https://example.com) to read my Medium Article to know more about these AI Agents and about OpenAI Swarm in General")


model = "gpt-3.5-turbo"

# Initialize the client
llm_client = openai
client = Swarm(client=llm_client)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    with st.chat_message(role):
        st.markdown(content)

# User input section at the bottom
if user_input := st.chat_input("Type your message here..."):
    # Append user's message to conversation history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Initialize current agent to triage
    current_agent = triage_agent

    # Pass user input to the current agent
    response = client.run(
        agent=current_agent,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
    )
    
    # Retrieve the assistant's response from Swarm
    agent_reply = response.messages[-1]["content"]
    
    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(agent_reply)
    
    # Append the assistant's response to conversation history
    st.session_state.messages.append({"role": "assistant", "content": agent_reply})