# Names of all html templates used on salesIQ project 

_ACCOUNTS_BASE = 'accounts'
_AUTH_BASE = f'{_ACCOUNTS_BASE}/auth'
_SETTINGS_BASE = f'{_ACCOUNTS_BASE}/settings'
_SETTINGS_PERSONAL_BASE = f'{_SETTINGS_BASE}/personal'
_SETTINGS_BUSINESS_BASE = f'{_SETTINGS_BASE}/business'


class APP_TEMPLATES:
    class ACCOUNTS:
        PROFILE = f'{_ACCOUNTS_BASE}/profile.html'
        ONBOARDING = f'{_ACCOUNTS_BASE}/onboarding.html'

        class AUTH:
            LOGIN = f'{_AUTH_BASE}/login.html'
            REGISTER = f'{_AUTH_BASE}/register.html'
            PASSWORD_RESET = f'{_AUTH_BASE}/password_reset.html'
            PASSWORD_CHANGE = f'{_AUTH_BASE}/password_change.html'

        class SETTINGS:
            class PERSONAL:
                CHANGE_PASSWORD = f'{_SETTINGS_PERSONAL_BASE}/change_password.html'

            class BUSINESS:
                UPDATE_BUSINESS_DATA = f'{_SETTINGS_BUSINESS_BASE}/update_business_data.html'
                
# 1. padlock animation https://lottiefiles.com/free-animation/password-set-LjQJxPwnaB
# https://lottiefiles.com/free-animation/lock-Ds4qQXD1Bz
# 
