import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import math
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Fetch the API  from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define tools
@tool
def add(a, b):
    """
    Adds two numbers.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    return a + b

@tool
def subtract(a, b):
    """
    Subtracts the second number from the first.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The result of a - b.
    """
    return a - b

@tool
def multiply(a, b):
    """
    Multiplies two numbers.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    return a * b

@tool
def divide(a, b):
    """
    Divides the first number by the second.

    Parameters:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float or str: The result of a / b, or an error message if division by zero.
    """
    return a / b if b != 0 else "Error: Division by zero"

@tool
def power(base, exponent):
    """
    Raises a number to a power.

    Parameters:
        base (float): The base number.
        exponent (float): The exponent.

    Returns:
        float: The result of base raised to the power of exponent.
    """
    return base ** exponent

@tool
def sqrt(number):
    """
    Calculates the square root of a number.

    Parameters:
        number (float): The number to find the square root of.

    Returns:
        float or str: The square root of the number, or an error message for negative input.
    """
    return math.sqrt(number) if number >= 0 else "Error: Negative input"

@tool
def modulus(a, b):
    """
    Finds the remainder of the division of two numbers.

    Parameters:
        a (int): The dividend.
        b (int): The divisor.

    Returns:
        int: The remainder of a divided by b.
    """
    return a % b

@tool
def factorial(number):
    """
    Calculates the factorial of a number.

    Parameters:
        number (int): The number to calculate the factorial of.

    Returns:
        int or str: The factorial of the number, or an error message for negative input.
    """
    
    return math.factorial(number) if number >= 0 else "Error: Negative input"

@tool
def log(number, base=10):
    """
    Calculates the logarithm of a number.

    Parameters:
        number (float): The number to calculate the logarithm of.
        base (float, optional): The base of the logarithm. Default is 10.

    Returns:
        float or str: The logarithm of the number, or an error message for non-positive input.
    """
    return math.log(number, base) if number > 0 else "Error: Invalid input"

@tool
def sin(angle):
    """
    Calculates the sine of an angle.

    Parameters:
        angle (float): The angle in degrees.

    Returns:
        float: The sine of the angle.
    """
    return math.sin(math.radians(angle))

@tool
def cos(angle):
    """
    Calculates the cosine of an angle.

    Parameters:
        angle (float): The angle in degrees.

    Returns:
        float: The cosine of the angle.
    """
    return math.cos(math.radians(angle))

@tool
def tan(angle):
    """
    Calculates the tangent of an angle.

    Parameters:
        angle (float): The angle in degrees.

    Returns:
        float or str: The tangent of the angle, or an error message for undefined tangent.
    """
    try:
        return math.tan(math.radians(angle))
    except:
        return "Error: Undefined tangent"

@tool
def percent(number, total):
    """
    Calculates the percentage of a number with respect to a total.

    Parameters:
        number (float): The part value.
        total (float): The total value.

    Returns:
        float or str: The percentage value, or an error message if total is zero.
    """
    return (number / total) * 100 if total != 0 else "Error: Division by zero"


@tool
def out_of_context(txt):
    """
    Ensures that users stay focused on calculator-related queries.This tool checks 
    if the user's input is relevant to calculator functions 
    such as addition, subtraction, multiplication, division, or other mathematical 
    operations. If the query is unrelated, the tool will politely ask the user 
    to stick to calculator-related topics.It also don't reply to the user queries 
    like what is 2 and what is 4 etc. 

    Parameters:
        query (str): The user's input or question.

    Returns:
        str: A response reminding the user to ask calculator-related questions if the input is irrelevant.
    """

    return "kindly ask about the calculation only as I am only a calculator agent"


# Tools list
tools = [add, subtract, multiply, divide, power, sqrt, log, modulus, percent, tan, cos, sin, factorial,out_of_context]

# Initialize LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    api_key="AIzaSyDOL9wbBKxlJ8O9Di24bBsBiO04g4kkbk4"
)

# Create the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
)

# Streamlit UI
st.title("AI-Powered Calculator")

st.write("Write your Mathematical Expression to get solution")


# Get input from the user
user_input = st.text_input("Enter a Mathematical Expression:")
if st.button("Submit"):
    if user_input.strip():
        response = agent.invoke(user_input)
        output = response["output"]
    
    st.markdown(
        f"""
        <div style="border: 1px solid #d3d3d3; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
            <strong>Output:</strong> {output}
        </div>
        """,
        unsafe_allow_html=True,
    )

