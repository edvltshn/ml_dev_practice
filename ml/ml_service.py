import json
import os
from joblib import load
import pika

from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, SQLModel, func, String

from sqlmodel import Session

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


# Пути к файлам моделей
logreg_model_path = 'logistic_regression_model.joblib'
random_forest_model_path = 'random_forest_best_model.joblib'
xgboost_model_path = 'xgboost_optimized_model.joblib'

# Загрузка моделей
logreg_model = load(logreg_model_path)
random_forest_model = load(random_forest_model_path)
xgboost_model = load(xgboost_model_path)

def predict(predictor, data):
    if predictor == "logistic_regression":
        model = logreg_model
    elif predictor == "random_forest":
        model = random_forest_model
    elif predictor == "xgboost":
        model = xgboost_model
    else:
        raise ValueError(f"Неизвестная модель: {predictor}")
        
    prediction = model.predict(data)
    return prediction

def on_message_received(channel, method, properties, body):
    print("Получено сообщение:", body)
    channel.basic_ack(delivery_tag=method.delivery_tag)

    body = json.loads(body)
    print(body)

    try:
        prediction = predict(body["predictor"], body["input_data"])
        save_prediction_to_db(prediction, body["id"])
        
    except Exception as error:
        print(error)


# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters('amqp://user:user@localhost:5672/%2F'))
channel = connection.channel()

queue = channel.queue_declare('test_exchange', durable=True).method.queue

channel.basic_consume(queue, on_message_callback=on_message_received)

channel.start_consuming()


def save_prediction_to_db(prediction, task_id):
    with Session(engine) as session:
        task = session.get(Task, task_id) 
        if task:
            task.output_data = str(prediction)
            session.commit()
        else:
            print(f"Задача с ID {task_id} не найдена.")



class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now()))
    predicted_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
    predictor: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True), foreign_key="predictor.name")
    input_data: str
    output_data: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))



DB_FILE: str = os.getenv("DB_FILE", "../api/src/temp.db")

DATABASE_URI = "sqlite:///{dbfile}".format(dbfile=DB_FILE)

engine = create_engine(DATABASE_URI)



