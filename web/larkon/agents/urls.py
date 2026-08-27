from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, ExecutionLogViewSet, webhook_trigger_view

app_name = "agents"

router = DefaultRouter()
router.register(r"agents", AgentViewSet, basename="agent")
router.register(r"executions", ExecutionLogViewSet, basename="execution")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/webhooks/<str:token>/", webhook_trigger_view, name="webhook-trigger"),
]
