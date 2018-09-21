from celery import Celery

cel = Celery('tasks', broker='amqp://dcs:dcs@10.10.1.15:5672/myvhost')

@cel.task
def add(x, y):
	return x + y