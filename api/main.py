#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""Entry point for the api."""

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from api.routers.opps import opp_router
from api.routers.users import user_router

middleware = [
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)
app.include_router(user_router)
app.include_router(opp_router)
