# we will be using ollama which allows us to run llm in our local machine

# step-1-importing the required libraries

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="llama3.2")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

#this function should be given as the result in main.py file
def parsing_with_ollama(dom_chunks,parse_description):
    #creating a prompt from predefined template
    prompt = ChatPromptTemplate.from_template(template)

    #creating a chain
    chain = prompt | model

    #empty list for storing the results
    parsed_results = []
     
    #iterating over the dom chunks with indexing from 1
    for i, chunk in enumerate(dom_chunks, start=1):
        #invoking the chain with current chunk and parse description
        response = chain.invoke(
            {"dom_content":chunk, "parse_description":parse_description}
            )
        
        print(f"no of batches completed: {i} of {len(dom_chunks)}") #printing the progress
        parsed_results.append(response) #appending the response to the list
        
        return "\n".join(parsed_results) #returning the parsed results