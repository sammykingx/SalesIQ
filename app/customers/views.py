from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from customers.serializers import CreateCustomerSchema
from utils.pydantic_formatter import format_pydantic_errors
from pydantic import ValidationError


class CreateCustomersView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest):
        try:
            data = CreateCustomerSchema.model_validate_json(request.body, strict=True)
            
        except ValidationError as err:
            return JsonResponse({
                "message": "Invalid data format", 
                "error": format_pydantic_errors(err), 
                "staus": "erro"
            }, status=422)
            
    