from django.contrib import admin
from .models import Agent, ExecutionLog, WebhookIntegration


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "description", "command")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ExecutionLog)
class ExecutionLogAdmin(admin.ModelAdmin):
    list_display = ("agent", "status", "triggered_by", "started_at", "finished_at")
    list_filter = ("status", "started_at")
    search_fields = ("agent__name", "error_message")
    readonly_fields = ("started_at", "finished_at")


@admin.register(WebhookIntegration)
class WebhookIntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "agent", "token", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "token", "agent__name")
