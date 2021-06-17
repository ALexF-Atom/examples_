from typing import Any
from django.views.generic import View
from django import http
from django.shortcuts import render

# Create your views here.

def test(request):
    return  render(request, "hobby_helper.html", {})

