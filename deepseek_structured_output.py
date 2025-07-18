import re
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser

# 🎨 Step 1: Define your output structure
class Fragrance(BaseModel):
    """Data model for information about a fragrance profile."""
    notes: str = Field(description="the 3 scent notes that best correlate with the prompt (eg. vanilla, citrus, rose)")
    color: str = Field(description="3 colors that best match the note profile, ordered from lightest to darkest.")
    description_1: str = Field(description="A multi-line description explaining the first perfume, it's scent notes, and the impression they make.")
    description_2: str = Field(description="A multi-line description explaining the second perfume, it's scent notes, and the impression they make.")
    description_3: str = Field(description="A multi-line description explaining the third perfume, it's scent notes, and the impression they make.")
    description_4: str = Field(description="A multi-line description explaining the fourth perfume, it's scent notes, and the impression they make.")

# 🔍 Step 2: Create a parser
parser = PydanticOutputParser(pydantic_object=Fragrance)

# 🧠 Step 3: System and human prompts
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert in fragrance profiles. Always respond with structured data in the format provided. "
    "Keep responses vivid yet factual. Do not comment. Do not introduce. Do not include any preamble."
)

human_prompt = HumanMessagePromptTemplate.from_template("{format_instructions}\n{query}")

# 🔗 Step 4: Build the complete chat prompt
chat_prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    human_prompt,
]).partial(format_instructions=parser.get_format_instructions())

# 🔥 Step 5: Connect to Ollama
llm = Ollama(model="deepseek-r1:latest", temperature=0.0)

# ⚙️ Step 6: Combine prompt and model
chain = chat_prompt | llm

# 🗣️ Step 7: Send your query
query = "give me the fragrance profile for rose."
full_response = chain.invoke({"query": query})

# 🧼 Step 8: Clean response
pattern = r"<think>.*?</think>\s*"
cleaned_response = re.sub(pattern, "", full_response, flags=re.DOTALL).strip()

# 📦 Step 9: Parse structured response
try:
    structured_response = parser.parse(cleaned_response)

    # 🧾 Step 10: Use your structured data
    #print("--- Structured Output ---")
    #print(structured_response)
    print("\n--- Accessing Data ---")
    print(f"Fragrance Category: {structured_response.fragrance_category}")
    print(f"Description: {structured_response.description}")
    print(f"Common Notes: {structured_response.common_notes}")
    print(f"Subfamilies: {structured_response.subfamilies}")
    print(f"Popular In: {structured_response.popular_in}")

except Exception as e:
    print("--- Error parsing the response ---")
    print(f"Error: {e}")
    print("\n--- Raw, Cleaned LLM Output ---")
    print(cleaned_response)