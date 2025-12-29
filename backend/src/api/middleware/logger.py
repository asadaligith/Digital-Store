"""
Structured logging middleware for API requests.

Logs all HTTP requests with structured JSON format including:
- Request method, path, query params
- Response status code
- Request duration
- Request ID for tracing
"""

import time
import uuid
from fastapi import Request
from typing import Callable


async def logger_middleware(request: Request, call_next: Callable):
    """
    Log all HTTP requests with structured format.

    Args:
        request: FastAPI request
        call_next: Next middleware/route handler

    Returns:
        Response from next handler
    """
    # Generate unique request ID for tracing
    request_id = str(uuid.uuid4())

    # Add request ID to request state for use in routes
    request.state.request_id = request_id

    # Record start time
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = round((time.time() - start_time) * 1000, 2)

    # Log request details
    log_data = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "status_code": response.status_code,
        "duration_ms": duration_ms,
        "client_ip": request.client.host if request.client else "unknown",
    }

    # Color code by status
    if response.status_code < 400:
        status_symbol = "✅"
    elif response.status_code < 500:
        status_symbol = "⚠️"
    else:
        status_symbol = "❌"

    print(
        f"{status_symbol} {log_data['method']} {log_data['path']} "
        f"[{log_data['status_code']}] {log_data['duration_ms']}ms "
        f"(ID: {request_id[:8]})"
    )

    # Add request ID to response headers for client tracing
    response.headers["X-Request-ID"] = request_id

    return response
