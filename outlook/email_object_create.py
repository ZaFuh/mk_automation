import os
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI

# Initialize the OpenAI client (ensure your API key is in your environment variables)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define the structured output using Pydantic
class EmailObject(BaseModel):
    summary: str = Field(description="A concise, 1-2 sentence summary of the email.")
    action_items: List[str] = Field(description="A list of specific tasks or actions required from the recipient. Empty list if none.")
    suggested_replies: List[str] = Field(description="An array of 2-3 contextual, ready-to-send replies.")

def process_email_with_llm(sender: str, subject: str, body: str) -> EmailObject:
    """
    Sends email content to OpenAI and returns a structured EmailObject.
    """
    system_prompt = """
    You are an intelligent email assistant. Analyze the provided email and extract a summary, 
    any actionable items, and generate 2-3 appropriate replies. Respond strictly in the required format.
    """
    
    email_content = f"From: {sender}\nSubject: {subject}\nBody: {body}"
    
    try:
        # Using the beta parse method for guaranteed structured JSON output
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini", # Using the mini model for cost efficiency
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_content}
            ],
            response_format=EmailObject,
        )
        
        # Extract the parsed Pydantic object
        email_analysis = completion.choices[0].message.parsed
        return email_analysis

    except Exception as e:
        print(f"Error processing email: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    sample_sender = "boss@example.com"
    sample_subject = "Q3 Project Deliverables"
    sample_body = "Hi team, please ensure all Q3 reports are submitted by Friday. Also, let me know your availability for a quick sync on Wednesday."

    result = process_email_with_llm(sample_sender, sample_subject, sample_body)
    
    if result:
        print(f"Summary: {result.summary}\n")
        print("Action Items:")
        for item in result.action_items:
            print(f"- {item}")
        print("\nSuggested Replies:")
        for reply in result.suggested_replies:
            print(f"- {reply}")