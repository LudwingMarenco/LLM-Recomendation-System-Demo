from typing import Dict
from langchain.schema.runnable import Runnable
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


template = """You are a movie recommender system that help users to find movie that match their preferences.
Question: {question}

Your response:"""


def load_model(config: Dict) -> Runnable:
    """Return a chain for movie recommender."""
    llm_model = LlamaCpp(
        model_path=config["model_path"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        verbose=False,
    )
    prompt = PromptTemplate.from_template(template)


    return prompt | llm_model
