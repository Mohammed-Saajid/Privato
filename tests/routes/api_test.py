import pytest
from fastapi import APIRouter
from unittest.mock import patch

import privato.app.api.routes.api as api_module


class TestApiRoutes:

    def test_router_instance(self):
        """Ensure the router is created as an APIRouter with correct configuration."""
        assert isinstance(api_module.router, APIRouter)
        assert api_module.router.prefix == "/api"
        assert "api" in api_module.router.tags
        assert 404 in api_module.router.responses
        assert api_module.router.responses[404]["description"] == "Not found"

    def test_included_routers(self):
        """Check that redactor and analyzer routers are included under /v1."""
        routes = {route.path: route for route in api_module.router.routes}

        # Redactor router should be included
        redactor_routes = [
            path for path in routes.keys() if path.startswith("/api/v1") and "redactor" in path
        ]
        assert redactor_routes, "Redactor router was not included under /api/v1"

        # Analyzer router should be included
        analyzer_routes = [
            path for path in routes.keys() if path.startswith("/api/v1") and "analyzer" in path
        ]
        assert analyzer_routes, "Analyzer router was not included under /api/v1"

