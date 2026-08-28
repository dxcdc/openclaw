import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.conf import settings

from larkon.agents.models import Agent, ExecutionLog, WebhookIntegration


@login_required
def root_page_view(request):
    """Página de Boas-Vindas limpa e organizada pós-login."""
    total_agents = Agent.objects.filter(is_active=True).count()
    total_executions = ExecutionLog.objects.count()
    total_webhooks = WebhookIntegration.objects.filter(is_active=True).count()

    context = {
        "user_email": request.user.email or request.user.username,
        "total_agents": total_agents,
        "total_executions": total_executions,
        "total_webhooks": total_webhooks,
    }
    return render(request, "pages/welcome.html", context)


@login_required
def openclaw_hub_view(request):
    """Página Especial Exclusiva do Agente Autônomo OpenClaw."""
    agents = Agent.objects.filter(is_active=True)
    recent_executions = ExecutionLog.objects.select_related("agent").order_by("-started_at")[:10]
    webhooks = WebhookIntegration.objects.filter(is_active=True)

    context = {
        "agents": agents,
        "recent_executions": recent_executions,
        "webhooks": webhooks,
        "gateway_url": "ws://127.0.0.1:18789",
    }
    return render(request, "pages/openclaw_hub.html", context)


@login_required
def docs_view(request):
    """Página de Governança & Diretrizes de Documentação."""
    doc_path = os.path.join(settings.BASE_DIR.parent, "docs", "diretrizes_documentacao.md")
    content = ""
    if os.path.exists(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            content = f.read()

    context = {
        "doc_content": content,
    }
    return render(request, "pages/docs_view.html", context)


@login_required
def dynamic_pages_view(request, template_name):
    try:
        return render(request, f"pages/{template_name}.html")
    except TemplateDoesNotExist:
        return render(request, "pages/pages-404.html")
