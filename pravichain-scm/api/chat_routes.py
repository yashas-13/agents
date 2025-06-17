"""Chatbot API routes."""

from fastapi import APIRouter
import subprocess

router = APIRouter()


@router.get('/chat')
def chat_endpoint(q: str):
    result = subprocess.run(['./agents/chatbot/llama_runner.sh', q], capture_output=True, text=True)
    return {"response": result.stdout}
