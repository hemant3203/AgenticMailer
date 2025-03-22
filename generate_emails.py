import random
import os
from crewai import Crew, Agent, Task
from email_templates import TEMPLATES
from extract_data import extract_data
from groq import Groq  # Ensure Groq API is set up

GROQ_API_KEY = "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"  # Replace with your actual API key
client = Groq(api_key=GROQ_API_KEY)

# **Agent 1: Data Analyst**
data_analyst = Agent(
    name="Data Analyst",
    goal="Extract and process user data from CSV or PDF files.",
    role="Data Extraction Specialist",
    description="This agent scans and extracts relevant user information such as name, email, phone, and address from structured CSV or PDF files.",
    backstory="A highly skilled data scientist with expertise in document processing, ensuring no detail is missed when extracting crucial user information.",
    verbose=True
)

# **Task 1: Extract User Data**
extract_data_task = Task(
    description="Analyze the given CSV or PDF file and extract first name, last name, email, phone number, and address.",
    agent=data_analyst,
    expected_output="A list of user data records in dictionary format."
)

# **Agent 2: Email Personalization Expert**
email_generator = Agent(
    name="Email Personalization Expert",
    goal="Generate personalized emails using different templates.",
    role="AI Email Generator",
    description="This agent selects a random email template and personalizes it for each recipient using their extracted details.",
    backstory="An AI-powered marketing assistant that crafts engaging, highly relevant emails to create a personalized user experience.",
    verbose=True
)

# **Task 2: Generate Personalized Emails**
generate_email_task = Task(
    description="Use predefined email templates to generate a personalized email for each recipient based on their details.",
    agent=email_generator,
    expected_output="A personalized email for each user."
)

# **Function to Execute Tasks**
def execute_tasks(data_file):
    try:
        users = extract_data(data_file)
    except ValueError as e:
        print(str(e))
        return []

    generated_files = []

    for user in users:
        email_template = random.choice(TEMPLATES)
        prompt = f"Generate a detailed and engaging personalized email for the following user using the template: {email_template}\n\nUser Details:\nFirst Name: {user.get('first_name', '')}\nLast Name: {user.get('last_name', '')}\nEmail: {user.get('email', '')}\nAddress: {user.get('address', '')}"

        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{"role": "system", "content": "You are an AI email assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.7
        )

        email_content = response.choices[0].message.content.strip()
        file_name = f"{user['first_name']}_{user['last_name']}.txt"
        generated_files.append((file_name, email_content))

    return generated_files  # Send data back to Streamlit
 # Send data back to Streamlit

# **Create the Crew**
crew = Crew(agents=[data_analyst, email_generator], tasks=[extract_data_task, generate_email_task])
