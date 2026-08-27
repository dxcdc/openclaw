from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Agent, ExecutionLog, WebhookIntegration
from .serializers import AgentSerializer, ExecutionLogSerializer
from .tasks import run_agent_execution


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.filter(is_active=True)
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        agent = self.get_object()
        input_payload = request.data.get("payload", {})

        execution = ExecutionLog.objects.create(
            agent=agent,
            triggered_by=request.user,
            input_payload=input_payload,
            status=ExecutionLog.Status.PENDING,
        )

        run_agent_execution.delay(str(execution.id))

        return Response(
            {
                "message": f"Agente '{agent.name}' disparado com sucesso.",
                "execution_id": str(execution.id),
                "status": execution.status,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class ExecutionLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([AllowAny])
def webhook_trigger_view(request, token):
    integration = get_object_or_404(WebhookIntegration, token=token, is_active=True)
    agent = integration.agent

    if not agent.is_active:
        return Response({"error": "Agente inativo"}, status=status.HTTP_400_BAD_REQUEST)

    input_payload = request.data if isinstance(request.data, dict) else {"raw": request.data}

    execution = ExecutionLog.objects.create(
        agent=agent,
        triggered_by=None,
        input_payload=input_payload,
        status=ExecutionLog.Status.PENDING,
    )

    run_agent_execution.delay(str(execution.id))

    return Response(
        {
            "status": "received",
            "execution_id": str(execution.id),
            "agent": agent.name,
        },
        status=status.HTTP_202_ACCEPTED,
    )
