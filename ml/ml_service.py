import json
import os
from joblib import load
import numpy as np
import pandas as pd
import pika

from sqlmodel import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Task, User, Predictor


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
        feature_names = ["N_Days", "Age", "Sex", "Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT", "Tryglicerides", "Platelets", "Prothrombin", "Stage", "Ascites_Y", "Hepatomegaly_Y", "Spiders_Y", "Edema_S", "Edema_Y"]

        data = json.loads(data)
        data = pd.DataFrame([data], columns=feature_names)

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


def save_prediction_to_db(prediction, task_id):
    with Session(engine) as session:
        task = session.get(Task, task_id) 
        if task:
            task.output_data = str(prediction)
            session.commit()
        else:
            print(f"Задача с ID {task_id} не найдена.")

def subtract_from_balance(user_id, predictor):
    with Session(engine) as session:
        pass
        

# DB_FILE: str = os.getenv("DB_FILE", "../api/src/temp.db") .format(dbfile=DB_FILE)

DATABASE_URI = "sqlite:////mnt/c/Users/edavletshin/courses/practice_ml_dev/project/api/src/temp.db"

engine = create_engine(DATABASE_URI)


# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters('amqp://user:user@localhost:5672/%2F'))
channel = connection.channel()

queue = channel.queue_declare('test_exchange', durable=True).method.queue

channel.basic_consume(queue, on_message_callback=on_message_received)

channel.start_consuming()










