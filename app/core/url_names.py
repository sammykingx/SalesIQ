from types import SimpleNamespace


# appName_grpNAme_urlName

ACCOUNTS = SimpleNamespace(
    PROFILE='accounts_profile',
    DASHBOARD='accounts_settings',
    ONBOARDING='accounts_onboarding',
    AUTH=SimpleNamespace(
        LOGIN='accounts_auth_login',
        LOGOUT='accounts_auth_logout',
        REGISTER='accounts_auth_register',
        PASSWORD_RESET='accounts_auth_password_reset',
        PASSWORD_CHANGE='accounts_auth_password_change',
    ),
)
