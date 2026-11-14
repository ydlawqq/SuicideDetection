from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI, Request
from shared.setup_logger import setup_logger
from model.predictor import Model
from pathlib import Path
from model.model_config import load_config
from worker import BatchWorker
from .schemas.predict_schema import PredictRequest, PredictResponse

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"



@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    cfg = load_config(CONFIG_PATH)
    predictor = Model(cfg)
    worker = BatchWorker(predictor, 
                                   batch_size=cfg.model.batch_size,
                                   time_limit=2.0)
    await worker.start()
    app.state.worker = worker
    yield
    await worker.stop()

app = FastAPI(lifespan=lifespan)


@app.post("/predict", response_model=PredictResponse)
async def predict(payload: PredictRequest, request: Request):
    worker = request.app.state.worker
    scores = await asyncio.gather(*[worker.score(t) for t in payload.texts])
    return PredictResponse(scores=scores)

