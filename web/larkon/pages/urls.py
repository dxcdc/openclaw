from django.urls import path
from .views import (root_page_view, openclaw_hub_view, docs_view, dynamic_pages_view)

app_name = "pages"

urlpatterns = [
    path("", root_page_view, name="dashboard"),
    path("openclaw/", openclaw_hub_view, name="openclaw_hub"),
    path("docs-governance/", docs_view, name="docs_view"),
    path("<str:template_name>/", dynamic_pages_view, name="dynamic_pages"),
]
