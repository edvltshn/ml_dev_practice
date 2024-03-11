### Клонирование репозитория

```bash
git clone https://github.com/edvltshn/ml_dev_practice.git
```

### Сборка и запуск API-сервера

```bash
cd api
docker build -t api_service .
docker run -d -v ${PWD}:/app -p 8000:8000 api_service
```

### Сборка и запуск ML-сервера

```bash
cd ml
docker build -t ml_service .
docker run -d -v ${PWD}:/app ml_service
```

### Запуск RabbitMQ
```bash
docker run --restart=unless-stopped -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin --detach rabbitmq:3-management
```
