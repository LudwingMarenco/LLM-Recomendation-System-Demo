from typing import Dict
from fastapi import FastAPI
from modules.movie_llm_chain import load_model
from pydantic import BaseModel
import uvicorn


class RecommenderAPI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RecommenderAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: Dict, host: str = "0.0.0.0", port: int = 8001):
        if not hasattr(self, 'initialized'):
            self.app = FastAPI(
                title="LangChain Server",
                version="1.0",
                description="A simple API server using LangChain",
            )
            self.llm_chain = load_model(config)
            self.setup_routes()
            self.host = host
            self.port = port

    def setup_routes(self):
        @self.app.post("/chat")
        async def chat_endpoint(chat_inputs: ChatInput):
            try:
                responses = {}
                print(chat_inputs.question)
                responses["response"] = str(
                    self.llm_chain.invoke({"question": chat_inputs.question})
                ).lstrip()
            except Exception as e:
                return {"error": str(e)}
            return responses

    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)


class ChatInput(BaseModel):
    question: str
