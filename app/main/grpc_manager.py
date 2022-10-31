import subprocess
import logging
from celery import Celery
from config import Config


celery = Celery(__name__)
celery.conf.broker_url = Config.CELERY_BROKER_URL
celery.conf.result_backend = Config.CELERY_RESULT_BACKEND

# run subprocess to /root/bin/grpcurl to grpc server url and port
def run(self, grpc_url, grpc_port, method, data):
    cmd = f"/root/bin/grpcurl -plaintext {grpc_url}:{grpc_port} {method} {data}"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')

@celery.task(name="grpcurl_tasks") 
def run_batch(self, grpc_url, grpc_port, method, json_input):
    for obj in json_input:
        cmd = f"/root/bin/grpcurl -plaintext {grpc_url}:{grpc_port} {method} {obj}"
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')