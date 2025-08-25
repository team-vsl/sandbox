from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app_info = {
    "title": "VP Bank Challenge #23 API Demo - VSL Team",
    "version": "0.0.1",
    "description": "Đây là API Demo của Challenge #23 VPBank Hackathon (Smart data contract with genai empowerment)",
}


def create_custom_openapi_schema(app: FastAPI):
    """Tạo cấu hình FastAPI theo chuẩn của OpenAPI.

    Args:
        FastAPI: instance của FastAPI.

    Returns:
        _: schema theo chuẩn open api.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app_info.get("title", ""),
        version=app_info.get("version", ""),
        description=app_info.get("description", ""),
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    # Thêm security schemes (tương đương components.securitySchemes)
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Thêm global security (tương đương security)
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Thêm servers (tương đương servers)
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server",
        }
    ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema
