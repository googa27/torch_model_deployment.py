from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch

app = FastAPI()

class InputData(BaseModel):
    '''
    Input data model for the API.
    Attributes:
        input (list[float]): Input tensor (e.g., [1, 2, 3, 4]).
    '''
    input: list[float]

@app.post("/infer")
async def infer(data: InputData):
    '''
    API endpoint for model inference: y = 2x.

    Args:
        data.input (list[float]): Input tensor (e.g., [1, 2, 3, 4]).

    Returns:
        dict: {'output': list} with doubled values (e.g., [2, 4, 6, 8]).
    '''
    try:
        tensor = torch.tensor(data.input, dtype=torch.float32)
        model = torch.jit.load("doubleit_model.pt")
        result = model(tensor)
        return {"output": result.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))