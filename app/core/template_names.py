# Names of all html templates used on salesIQ project 

_ACCOUNTS_BASE = 'accounts'
_AUTH_BASE = f'{_ACCOUNTS_BASE}/auth'

_CUSTOMERS_BASE = 'customers'


class APP_TEMPLATES:
    class ACCOUNTS:
        PROFILE = f'{_ACCOUNTS_BASE}/profile.html'
        SETTINGS = f'{_ACCOUNTS_BASE}/settings.html'
        ONBOARDING = f'{_ACCOUNTS_BASE}/onboarding.html'
        ACTIVATION = f'{_ACCOUNTS_BASE}/activation.html'
        DASHBOARD = f'{_ACCOUNTS_BASE}/dashboard.html'

        class AUTH:
            LOGIN = f'{_AUTH_BASE}/login.html'
            REGISTER = f'{_AUTH_BASE}/register.html'
            PASSWORD_RESET = f'{_AUTH_BASE}/password_reset.html'
            PASSWORD_CHANGE = f'{_AUTH_BASE}/password_change.html'

        class CUSTOMERS:
            LIST = f'{_CUSTOMERS_BASE}/list-all.html'
            DETAIL = f'{_CUSTOMERS_BASE}/detail.html'
            ADD = f'{_CUSTOMERS_BASE}/add.html'
            EDIT = f'{_CUSTOMERS_BASE}/edit.html'
            
                
# 1. padlock animation https://lottiefiles.com/free-animation/password-set-LjQJxPwnaB
# https://lottiefiles.com/free-animation/lock-Ds4qQXD1Bz
# 

_EMAIL_BASE_FOLDER = "email"
class EMAIL_TEMPLATES:
    ACCOUNT_ACTIVATION = f'{_EMAIL_BASE_FOLDER}/account-activation.html'
    ACCOUNT_RECOVERY = f'{_EMAIL_BASE_FOLDER}/account-recovery.html'
    
    
class LANDING_PAGES:
    FEEDBACK = 'public/feedback.html'
    
class ERROR_PAGES:
    NOT_FOUND = "errors/404.html"
    INETERNAL_ERROR = "errors/500.html"
    