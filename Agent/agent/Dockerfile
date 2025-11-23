FROM python:3.14
WORKDIR /usr/local/app

RUN pip install -U langchain
RUN pip install -U langgraph
RUN pip install -U langchain-groq
RUN pip install psycopg[binary]
ENV GROQ_API_KEY={your_groq_api_key}

COPY . .

CMD ["python", "main.py"]