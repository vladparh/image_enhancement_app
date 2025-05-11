FROM python:3.10-slim

RUN mkdir /streamlit_app

WORKDIR /streamlit_app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
