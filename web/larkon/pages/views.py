from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist

from larkon.agents.models import Agent, ExecutionLog, WebhookIntegration


@login_required
def root_page_view(request):
    try:
        total_agents = Agent.objects.filter(is_active=True).count()
        total_executions = ExecutionLog.objects.count()
        total_webhooks = WebhookIntegration.objects.filter(is_active=True).count()
        recent_executions = ExecutionLog.objects.select_related("agent").order_by("-started_at")[:10]
        active_agents = Agent.objects.filter(is_active=True)[:5]

        context = {
            "total_agents": total_agents,
            "total_executions": total_executions,
            "total_webhooks": total_webhooks,
            "recent_executions": recent_executions,
            "active_agents": active_agents,
        }
        return render(request, "pages/index.html", context)
    except TemplateDoesNotExist:
        return render(request, "pages/pages-404.html")


@login_required
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f"pages/{template_name}.html")
    except TemplateDoesNotExist:
        return render(request, "pages/pages-404.html")
