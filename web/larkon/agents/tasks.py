import subprocess
from celery import shared_task
from django.utils import timezone
from .models import ExecutionLog


@shared_task(bind=True)
def run_agent_execution(self, execution_id):
    try:
        execution = ExecutionLog.objects.get(id=execution_id)
    except ExecutionLog.DoesNotExist:
        return f"Execution {execution_id} not found"

    execution.status = ExecutionLog.Status.RUNNING
    execution.save(update_fields=["status"])

    agent = execution.agent
    command = agent.command

    try:
        # Example shell execution of agent command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            execution.status = ExecutionLog.Status.SUCCESS
            execution.output_result = {
                "stdout": result.stdout,
                "returncode": result.returncode,
            }
        else:
            execution.status = ExecutionLog.Status.FAILED
            execution.error_message = result.stderr or f"Command failed with exit code {result.returncode}"
            execution.output_result = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

    except Exception as exc:
        execution.status = ExecutionLog.Status.FAILED
        execution.error_message = str(exc)

    execution.finished_at = timezone.now()
    execution.save(update_fields=["status", "output_result", "error_message", "finished_at"])

    return f"Execution {execution_id} finished with status {execution.status}"
