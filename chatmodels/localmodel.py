# # This code demonstrates how to use the Hugging Face Transformers library to perform text generation using a pre-trained model (GPT-2 in this case). It is used generally for testing the model's capabilities in generating text based on a given prompt.
# from transformers import pipeline

# pipe = pipeline("text-generation", model="gpt2")

# print(pipe("the capital of india", max_length=20))


## using langchain using this we can make ai apps and also test the models:
from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=50,
        do_sample=False,
        repetition_penalty=1.03,
    ),
)

chat_model = ChatHuggingFace(llm=llm)

result = chat_model.invoke("write a poem")
print(result.content)




# Feature	        LangChain Code 🧠	Pipeline Code ⚡
# Complexity	        High	              Low
# Beginner-Friendly	    ❌	                ✅
# Speed	               Slower	            Faster
# Use case  	       AI apps	        Testing models
# Setup	                More	          Very easy