import os
from fastapi import FastAPI, Request
import uvicorn
from llama_cpp import Llama


auth_token = os.environ['auth_token']

app = FastAPI()

llm = Llama(
    #model_path="/home/yarolit/Models/llm/qwen2.5-14b-instruct-q5_k_m-00001-of-00003.gguf",
    #model_path="/home/yarolit/Models/llm/qwen2.5-coder-32b-instruct-q3_k_m.gguf",
    model_path="/home/yarolit/Models/llm/qwen2.5-14b-instruct-q3_k_m-00001-of-00002.gguf",
    seed=42,
    n_ctx=15000,
    n_gpu_layers=-1,
    verbose=True,
)

@app.get("/")
async def root():
    return {"message": "ОК"}

@app.post("/answer/")
async def post_transcribe(request: Request):
    """
    Обрабатываем post запрос с транскрибированным диалогом
    """
    prompt_request = await request.json()
    if prompt_request["auth_token"] == auth_token:
        prompt = prompt_request["prompt"]
        answer = llm_analyze(prompt)
        return answer
    else:
        return {"message": "token not valid"}

def llm_analyze(prompt: str) -> str:
    output = llm.create_chat_completion(
        max_tokens = 15000,
        temperature = 0.2,
        messages = [{
				"role": "assistant",
				"content": prompt
		}]
	)
    return output['choices'][0]['message']['content']


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")