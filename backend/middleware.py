#!/usr/bin/env python3
"""Module for middleware"""

import logging
import traceback
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

class Middleware(BaseHTTPMiddleware):
    """Class to handle exceptions that breaks the program and should be shown to the user"""
    def __init__(self, app, templates):
        super().__init__(app)
        self.templates = templates
          
    async def dispatch(self, request: Request, call_next):
        """Method to dispatch intercepted requests"""
        try:
            response = await call_next(request)
            return response
        
        except Exception as error:
            logging.exception("An error occurred")
            return await self.handle_exception(error, request)
          
    async def handle_exception(self, exc: Exception, request: Request):
        """Method to catch and handle exceptions"""
        if isinstance(exc, (HTTPException, StarletteHTTPException)):
            status_code = exc.status_code
            error_message = str(exc.detail)
        else:
            status_code = 500
            truncated_traceback = "\n".join(traceback.format_exc().splitlines()[-6:])
            error_message = f"An unexpected error occurred: {truncated_traceback}"

        return self.templates.TemplateResponse("error.html", {
            "request": request,
            "status_code": status_code,
            "error_message": error_message,
        }, status_code=status_code)
