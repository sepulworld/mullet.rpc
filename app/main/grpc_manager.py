import subprocess
import datetime
from celery import Celery
from config import Config
from celery.utils.log import get_task_logger
from models import CeleryTaskLogs
from app import db  

logger = get_task_logger(__name__)

celery = Celery(__name__)
celery.conf.broker_url = Config.CELERY_BROKER_URL
celery.conf.result_backend = Config.CELERY_RESULT_BACKEND


@celery.task(name="grpcurl_tasks") 
def run_batch(self, grpc_url, grpc_port, proto, method, import_paths, json_input, user_id):
    all_results = []
    # Create a CeleryTaskLogs object
    celery_task_logs = CeleryTaskLogs(
        task_id=self.request.id,
        task_name=self.name,
        task_args=self.request.args,
        task_kwargs=self.request.kwargs,
        task_status=self.request.state,
        task_result=self.request.result,
        task_start_time=self.request.started,
        task_end_time=self.request.ended,
        task_duration=self.request.duration,
        task_traceback=self.request.traceback,
        task_exception=self.request.exception,
        task_user_id=user_id
    )
    # Add the CeleryTaskLogs object to the database
    db.session.add(celery_task_logs)
    db.session.commit()
        
    try:
        for obj in json_input:
            cmd = f"/root/bin/grpcurl -v -plaintext -d {obj}"
            for import_path in import_paths:
                cmd += f" -import-path {import_path}"
            cmd += f" -proto {proto} {grpc_url}:{grpc_port} {method}"
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            all_results.append(result.stdout.decode("utf-8"))
    except Exception as e:
        logger.error(e)
        raise e
    
    # Save the results to the database
    task = CeleryTaskLogs.query.filter_by(task_id=self.request.id).first()
    task.task_result = all_results
    task.task_end_time = datetime.utcnow()
    task.task_duration = task.task_end_time - task.task_start_time
    return all_results
