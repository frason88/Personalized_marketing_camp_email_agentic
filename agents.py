
import os
import json
import autogen
import sqlite3
from contextlib import contextmanager
import panel as pn
import requests
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

conn = sqlite3.connect('customer_netcore.db')
cursor = conn.cursor()

# gpt-4o
config_list = [
    {
        "model": "gpt-4o-2024-08-06",
        # "model": "gpt-3.5-turbo",
        "api_key": os.getenv("OPENAI_API_KEY"), # Use environment variable
    }
]

# config_list = [
#     {
#         "api_type": "bedrock",
#         "model": "us.meta.llama3-2-11b-instruct-v1:0",
#         "aws_region": "us-east-1",
#         "aws_access_key": os.getenv("AWS_ACCESS_KEY"),
#         "aws_secret_key": os.getenv("AWS_SECRET_KEY"),
#     }
# ]

code_interpreter = autogen.UserProxyAgent(
    "code_interpreter",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    max_consecutive_auto_reply=1,
)

data_retriever = autogen.AssistantAgent(
    "data_retriever",
    system_message="""
    You are the data engineer who retrieves the data from the database. Your task is to utilize the 'retrieve_user_data' function that fetches the customer 
    data from the database based on the user_id provided. The data includes various attributes such as total_spent, transaction_frequency, 
    average_transaction_value, preferred_payment_method, purchase_channel, preferred_device, preferred_language, loyalty_program_member, 
    loyalty_points_balance, email_open_rate, email_click_rate, SMS_opt_in, product_browsing_history, coupon_usage_frequency, social_media_engagement, 
    preferred_communication_channel, click_through_rate, conversion_rate, brand_loyalty_index, lifetime_value_estimate, and product_affinity. 
    """,
    description="You are a data engineer and you are the first person in this pipeline, your task is to retrieve the data from the database based on the user_id provided.",
    llm_config={"config_list": config_list},
)

analyst = autogen.AssistantAgent(
    "analyst",
    system_message="""
    You are a data analyst specializing in marketing segmentation. Your task is to analyze distinct audience segments based on their preferences, behaviors, and engagement metrics from the data generated by the data_retriever and generate a research report.
    Utilize the following features to provide a detailed report: total_spent, transaction_frequency, average_transaction_value, preferred_payment_method, purchase_channel, preferred_device, 
    preferred_language, loyalty_program_member, loyalty_points_balance, email_open_rate, email_click_rate, SMS_opt_in, product_browsing_history, 
    coupon_usage_frequency, social_media_engagement, preferred_communication_channel, click_through_rate, conversion_rate, brand_loyalty_index, 
    lifetime_value_estimate, and product_affinity. Provide insights into each segment's buying behavior, communication preferences, and potential engagement 
    strategies.
    <Goals>
    - Identify customer segments with deep insights into their spending habits, engagement patterns, and preferred communication channels.
    - Analyze loyalty program participation, social media engagement, and product affinities.
    - Suggest personalized content themes that cater to each segment's unique behaviors and preferences.
    </Goals>

    <Key Tasks>
    - Segment customers based on metrics such as spending patterns, engagement rates, and loyalty points.
    - Provide actionable insights on how to tailor content for segments like "High-Value Customers," "Occasional Shoppers," "Loyalty Program Members," etc.
    - Recommend optimal communication channels (email, SMS, social media) and timing for each segment.
    </Key Tasks>
    """,
    description="You are an analyst, your task it to identify and analyze distinct audience segments and generate a research report from the user data given by the data_retriever before the email is generated.",
    llm_config={"config_list": config_list},
)

email_agent = autogen.AssistantAgent(
    "email_agent",
    system_message="""
    You are an expert email marketing agent tasked with generating complete, personalized email content. Your job is to create engaging and visually 
    appealing emails that are ready to be sent, using dynamic placeholders to ensure each email is fully customized for the recipient. Use placeholders such 
    as, [DISCOUNT], [PRODUCT_NAME], and [MSP] to integrate personalized data seamlessly. The emails should be optimized for readability and 
    display correctly on both desktop and mobile devices, using simple and effective HTML formatting.

    <Example Emails>

    - Example 1:

Dear [USER_NAME],

        Your wardrobe deserves an upgrade! Get [DISCOUNT]% off on the latest [PRODUCT_NAME] from StylishThreads. With prices as low as [MSP], there’s no better time to shop. Don’t miss out on this special offer!

        Happy Shopping,
        The StylishThreads Team


    - Example 2:

Dear [USER_NAME],

        Discover our newest range of [PRODUCT_NAME] at StylishThreads! Even without a discount, you'll love the new collection starting at [MSP]. Don't miss out on the latest trends.

        Best Regards,
        The StylishThreads Team


    <Instructions>

    - Create personalized email content** that is ready to be sent to the recipient. The emails should be more than templates – they should be complete and fully written out.
    - Ensure the email content has a clear structure with appropriate greetings, body content, and sign-off lines.
    - Use HTML only where necessary to format the text, such as bolding key elements, but avoid unnecessary HTML tags.
    - Ensure that the email content is conversational, warm, and fits the brand’s tone and voice, and is designed to engage the reader effectively.

    Keep in mind that the emails should be personalized based on the user data provided by the analyst and should be very simple and optimized for 
    engagement and conversion.
    </Instructions>
    """,
    llm_config={"config_list": config_list},
)


@contextmanager
def get_db_connection():
    conn = sqlite3.connect('customer_netcore.db')
    try:
        yield conn
    finally:
        conn.close()


@code_interpreter.register_for_execution()
@data_retriever.register_for_llm(
    name="retrieve_user_data", description="Get the information from the database about the user."
)
def retrieve_user_data(user_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer_data WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            columns = [col[0] for col in cursor.description]
            user_data_dict = dict(zip(columns, user_data))
            return user_data_dict
    return None


user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
)

# Put them in a virtual room
groupchat = autogen.GroupChat(
    agents=[data_retriever, code_interpreter, analyst, email_agent],
    messages=[],
    allow_repeat_speaker=True,
    speaker_selection_method="round_robin",
    max_round=15,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={
        "config_list": config_list,
    },
)
# Give it a task or assign a goal

task = """
Analyze the customer data with user_id '1' and create an email marketing campaign targeting different audience segments with personalized content. Use metrics such as total_spent, purchase_frequency, loyalty_points_balance, email_click_rate, and preferred_payment_method to inform your strategies. Ensure the campaign is optimized for engagement and conversion, with real-time adaptation based on feedback.
"""

avatar = {user_proxy.name: "👨‍💼", manager.name: "👩‍💻", data_retriever.name: "👩‍🔬", code_interpreter.name: "🛠",
          email_agent.name: '📝', analyst.name: '📊'}


def print_messages(recipient, messages, sender, config):
    # chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
    print(
        f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")

    if all(key in messages[-1] for key in ['name']):
        chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']],
                            respond=False)
    else:
        chat_interface.send(messages[-1]['content'], user='SecretGuy', avatar='🥷', respond=False)

    return False, None


user_proxy.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

data_retriever.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

code_interpreter.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

analyst.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

email_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

pn.extension(design="material")


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    user_proxy.initiate_chat(manager, message=contents)


chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Welcome! How can I assist you with your marketing campaign today? Please mention the 'user_id' you want write the marketing campaign for.",
    user="Campaign Agent", respond=False, avatar='🧠')
chat_interface.servable()
pn.serve(chat_interface, port=8080, show=True)

# start the agents to work
# user_proxy.initiate_chat(manager, message=task)
# last_messages = groupchat.messages