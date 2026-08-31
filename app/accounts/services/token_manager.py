from ..models.user_token import UserToken, TokenType, TokenResult
from typing import Union


class TokenService:
    def __init__(self):
        self.model = UserToken
        
    def create_token(self, *, user_email:str, token_type: TokenType) -> TokenResult:
        return self.model.objects.generate_token(user_email=user_email, token_type=token_type) # type: ignore
    
    def get_token_obj(self, token: str, tkn_type: TokenType) -> Union[UserToken, None]:
        """
        Retrieves a UserToken object matching the provided token string.

        Returns:
            UserToken | None: The token object if it exists, otherwise None.
        """
        try:
            user_token = UserToken.objects.get(
                token=token,
                token_type=tkn_type,
                is_valid=True,
            )
        except UserToken.DoesNotExist:
            return None
        return user_token
    
    def is_valid(self, token_obj: UserToken) -> bool:
        return token_obj.has_expired()
    

    def invalidate_token(self, token_obj: UserToken) -> None:
        """
        Marks the user’s email as verified and invalidates the token.

        Side effects:
            - Invalidates the token so it cannot be reused.
            - Updates the associated user account to mark it as verified.
        """
        token_obj.invalidate_token()
        return None