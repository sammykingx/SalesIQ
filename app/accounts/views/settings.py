from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, View
from accounts.domains.entities import UserEntity, BusinessEntity
from accounts.repository.user_repo import UserRepository
from accounts.selectors import UserSelector, BusinessSelector
from accounts.serializers import SocialLinksSchema
from core.template_names import APP_TEMPLATES
from datetime import timedelta
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
            data = json.loads(request.body)
            print(data)
            # self.user_repo.update_multiple_fields(user_id=request.user.id, **data)  # type: ignore
            return JsonResponse({"message": "Account data updated successfully."}, status=204)
            
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON payload."}, status=400)
        except Exception as e:
            return JsonResponse({"message": "An error occurred while updating the account data.", "status": "error"}, status=500)

    
    # def put(self, request: HttpRequest) -> JsonResponse:
    #     """
    #     Handles full replacements of the user's profile data.

    #     Expects a JSON payload containing all mandatory fields required to 
    #     completely replace or update the user model record.

    #     Args:
    #         request (HttpRequest): The HTTP request object containing the full payload.

    #     Returns:
    #         JsonResponse: A JSON response indicating success or failure.
    #     """
    #     return JsonResponse({"message": "Account data updated successfully."})
    
    
class UpdateBusinessDataView(LoginRequiredMixin, View):
    """Updates the users business data"""

    def put(self, request: HttpRequest) -> JsonResponse:
        try:
            # data = BusinessDataSchema.model_validate_json(request.body, strict=True)
            # UserRepository().update_business_data(
            #     user_email=self.request.user.email, # type: ignore
            #     instagram_url=data.instagram_url,
            #     tiktok_url=data.tiktok_url,
            #     website_url=data.website_url
            # )
            return JsonResponse({"message": "Business data updated successfully."})
            
        except Exception as e:
            return JsonResponse({"message": "Invalid data provided", "error": str(e)}, status=422)
