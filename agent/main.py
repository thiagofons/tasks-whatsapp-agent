from agents.routing import RoutingAgent
from agents.task import TaskAgent
from database.models import User
from fastapi import FastAPI
from tools.base import Tool
from tools.report import report_function
from utils import generate_query_context

# Agent
routing_agent = RoutingAgent(
    tools=[]
)

# API
app = FastAPI()

# Only to check if the agent is running
@app.get("/")
def read_root():
    return {"message": "Agent FastAPI is running!"}

# This endpoint will be called by the NestJS orchestrator  
@app.post("/request")
def process_data(request: dict):
    user_input = request.get("message", "")

    response = routing_agent.run(user_input)

    return {"response": response}
