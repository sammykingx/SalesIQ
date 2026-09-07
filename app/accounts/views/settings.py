from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, View
from accounts.domains.entities import UserEntity, BusinessEntity
from accounts.repository import UserRepository, BusinessRepo
from accounts.selectors import UserSelector, BusinessSelector
from accounts.serializers import AccountUpdateSchema
from core.template_names import APP_TEMPLATES
from utils.pydantic_formatter import format_pydantic_errors
from datetime import timedelta
from pydantic import BaseModel, ValidationError
import json


class AccountSettingsView(LoginRequiredMixin, TemplateView):
    """
    Renders the account settings page for authenticated users, 
    hydrating the template context with the user and their associated business data.

    Attributes:
        template_name (str): The path to the account settings HTML template.
        user_selector (UserSelector): Selector used to fetch user-related data.
        business_selector (BusinessSelector): Selector used to fetch business-related data.
    """
    template_name = APP_TEMPLATES.ACCOUNTS.SETTINGS
    user_selector = UserSelector()
    business_selector = BusinessSelector()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.template_context())
        return context
    
    def template_context(self):
        user_entity = self.user_selector.get_by_email(email=self.request.user.email) #type: ignore
        biz_entity = self.business_selector.get_user_business(user_email=self.request.user.email) #type: ignore
        cool_down_date = timezone.now() + timedelta(days=10)
        return {
            "user": user_entity,
            "business": biz_entity,
            "cool_down": None, #cool_down_date,
        }
        
class UpdateAccountProfileDataView(LoginRequiredMixin, View):
    """
    Handles updating authenticated user account profile information.

    Supports two types of update operations:
        - PATCH: Performs a partial update, modifying only the specific fields 
          provided in the request payload (e.g., changing just the phone number).
        - PUT: Performs a full replacement/update, requiring all user profile 
          data to be provided to overwrite the existing record.

    Attributes:
        request (HttpRequest): The HTTP request object.
    """
    
    user_selector = UserSelector()
    user_repo = UserRepository()
    biz_repo = BusinessRepo()
        

    def patch(self, request: HttpRequest) -> JsonResponse:
        """
        Handles partial updates to the user's profile data.

        Expects a JSON payload containing only the fields that need to be changed.

        Args:
            request (HttpRequest): The HTTP request object containing the partial payload.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """
        try:
            payload = AccountUpdateSchema.model_validate_json(request.body, strict=True)
            update_type = payload.update_type
            print(payload.model_dump_json(indent=2))
            
            if  update_type == 'profile':
                self.user_repo.update_multiple_fields(user_id=request.user.id, **payload.data.model_dump())  # type: ignore
            
            elif update_type == 'socials':
                self.biz_repo.update_multiple_fields(owner=self.request.user.email, **payload.data.model_dump()) # type: ignore
                
            return JsonResponse({"message": "Account data updated successfully."}, status=204)
            
        except ValidationError as e:
            error_message = format_pydantic_errors(e)
            print(error_message)
            
            return JsonResponse({
                "message": "Your data is looking a bit confused, double-check your fields and formats before we try this again!", 
                "status": "error", 
                "errors": error_message
            }, status=422)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"message": "An error occurred while updating the account data.", "status": "error"}, status=500)
