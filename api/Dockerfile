FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN pip install --upgrade pip -i https://pypi.douban.com/simple

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./app /app
