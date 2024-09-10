from typing import Dict
from langchain.schema.runnable import Runnable
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate


template = """Question: {question}

Answer: Sure, here is a selection of movies."""

# template = """You are a movie recommender system that help users to find anime that match their preferences.
# Use the following pieces of context to answer the question at the end.
# For each question, suggest three anime, with a short description of the plot and the reason why the user migth like it.
# If you don't know the answer, just say that you don't know, don't try to make up an answer.

# {context}

# Question: {question}
# Your response:"""


def load_model(
    config: Dict
) -> Runnable:
    """Return a chain for movie recommender."""
    prompt = PromptTemplate.from_template(template)

    llm_model = LlamaCpp(
        model_path=config["model_path"],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        verbose=False,
    )

    return prompt | llm_model
