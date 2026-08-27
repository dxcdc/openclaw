import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Nome do Agente"), max_length=150)
    slug = models.SlugField(_("Identificador / Slug"), unique=True)
    description = models.TextField(_("Descrição"), blank=True)
    command = models.CharField(_("Comando / Script"), max_length=255, help_text="Comando ou módulo python a ser executado")
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Agente")
        verbose_name_plural = _("Agentes")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.slug})"


class ExecutionLog(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pendente")
        RUNNING = "RUNNING", _("Em Execução")
        SUCCESS = "SUCCESS", _("Sucesso")
        FAILED = "FAILED", _("Falha")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="executions", verbose_name=_("Agente"))
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agent_executions",
        verbose_name=_("Disparado por"),
    )
    status = models.CharField(_("Status"), max_length=20, choices=Status.choices, default=Status.PENDING)
    input_payload = models.JSONField(_("Payload de Entrada"), default=dict, blank=True)
    output_result = models.JSONField(_("Resultado / Output"), default=dict, blank=True)
    error_message = models.TextField(_("Mensagem de Erro"), blank=True)
    started_at = models.DateTimeField(_("Iniciado em"), auto_now_add=True)
    finished_at = models.DateTimeField(_("Finalizado em"), null=True, blank=True)

    class Meta:
        verbose_name = _("Log de Execução")
        verbose_name_plural = _("Logs de Execução")
        ordering = ["-started_at"]

    def __str__(self):
        return f"[{self.status}] {self.agent.name} ({self.started_at.strftime('%Y-%m-%d %H:%M:%S')})"


class WebhookIntegration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Nome da Integração"), max_length=150)
    token = models.CharField(_("Token Secret"), max_length=64, unique=True, default=uuid.uuid4)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="webhooks", verbose_name=_("Agente Destino"))
    is_active = models.BooleanField(_("Ativo"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Integração Webhook")
        verbose_name_plural = _("Integrações Webhook")

    def __str__(self):
        return f"{self.name} -> {self.agent.name}"
