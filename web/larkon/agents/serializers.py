from rest_framework import serializers
from .models import Agent, ExecutionLog, WebhookIntegration


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "name", "slug", "description", "is_active", "created_at"]


class ExecutionLogSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source="agent.name", read_only=True)

    class Meta:
        model = ExecutionLog
        fields = [
            "id",
            "agent",
            "agent_name",
            "triggered_by",
            "status",
            "input_payload",
            "output_result",
            "error_message",
            "started_at",
            "finished_at",
        ]
        read_only_fields = ["id", "status", "output_result", "error_message", "started_at", "finished_at"]
