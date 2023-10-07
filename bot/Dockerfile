FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

ENV PIP_NO_CACHE_DIR=1
RUN pip install -U pip \
	&& pip install -r requirements.txt

COPY ./ ./

CMD ["python", "-m", "bot"]
