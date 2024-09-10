from typing import Dict
from langchain.schema.runnable import Runnable
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

# template = """You are a movie recommender system that help users to find the best movie that match their preferences.
#             Question: {question}

#             Your response: Sure, here is a selection of movies."""
template = """Question: {question}

            Your response: Sure, here is a selection of movies."""

def load_model(config: Dict) -> Runnable:
    """Return a chain for movie recommender."""
    prompt = PromptTemplate.from_template(template)
    llm_model = LlamaCpp(
        model_path=config["model_path"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        verbose=False,
    )
    # template = """You are a {subject} recommender system that help users to find the best {subject} that match their preferences.
    #             Question: {question}

    #             Your response:"""
    

    return prompt | llm_model
