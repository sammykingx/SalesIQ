from typing import NamedTuple


class FailureDetail(NamedTuple):
    """
    A structured representation of a domain failure.

    Attributes:
        code (str): A unique, machine-readable string identifier (e.g., 'INVALID_AMOUNT').
        title (str): A brief, human-readable description intended for end-user display.
    """

    code: str
    title: str
    

class AccountRegistrationErrors:
    """Centralized error definitions for the account registration process."""
    DUPLICATE_EMAIL = FailureDetail(
        code="DUPLICATE_EMAIL",
        title="An account with this email address already exists."
    )
    WEAK_PASSWORD = FailureDetail(
        code="WEAK_PASSWORD",
        title="The provided password does not meet complexity standards."
    )
    PASSWORDS_MISMATCH = FailureDetail(
        code="PASSWORDS_MISMATCH",
        title="The entered passwords do not match."
    )


class AccountActivationErrors:
    """Centralized error definitions for the account activation process."""
    INVALID_TOKEN = FailureDetail(
        code="INVALID_TOKEN",
        title="The activation link is invalid or malformed."
    )
    EXPIRED_TOKEN = FailureDetail(
        code="EXPIRED_TOKEN",
        title="The activation link has expired. Please request a new one."
    )
    ALREADY_ACTIVATED = FailureDetail(
        code="ALREADY_ACTIVATED",
        title="This account has already been activated."
    )


class PasswordResetErrors:
    """Centralized error definitions for password reset and update workflows."""
    USER_NOT_FOUND = FailureDetail(
        code="USER_NOT_FOUND",
        title="No account was found matching this email address."
    )
    INVALID_RESET_TOKEN = FailureDetail(
        code="INVALID_RESET_TOKEN",
        title="The password reset link is invalid or has already been used."
    )
    EXPIRED_RESET_TOKEN = FailureDetail(
        code="EXPIRED_RESET_TOKEN",
        title="The password reset link has expired."
    )
    SAME_AS_OLD_PASSWORD = FailureDetail(
        code="SAME_AS_OLD_PASSWORD",
        title="Your new password cannot be the same as your previous password."
    )
