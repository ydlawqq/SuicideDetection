FROM pytorch/pytorch:2.9.1-cuda12.6-cudnn9-runtime

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-emit-package torch -o /tmp/req.txt \
&& uv pip install --system -r /tmp/req.txt

RUN python -c "import torch; print('torch', torch.__version__, '| cuda:', torch.version.cuda)"


COPY model/ ./model/ 
COPY api/ ./api/
COPY worker.py logging_setup.py config.yaml ./
COPY weights/ ./weights/

ENV PATH="/app/.venv/bin:$PATH" \
    HF_HOME=/app/hf_cache \
    PYTHONUNBUFFERED=1  


 
EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]