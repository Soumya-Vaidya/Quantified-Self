# hello

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Flask
```
python app.py
```

### Celery
```
celery -A tasks.celery worker -P gevent -l INFO
```

### Celery Beat
```
celery -A tasks.celery beat --max-interval 1 -l INFO
```

### Redis
```
redis-server
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
