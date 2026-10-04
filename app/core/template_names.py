# Names of all html templates used on salesIQ project 

_ACCOUNTS_BASE = 'accounts'
_AUTH_BASE = f'{_ACCOUNTS_BASE}/auth'

_CUSTOMERS_BASE = 'customers'
_PRODUCTS_BASE = 'products'
_SALES_BASE = 'sales'
_INVOICES_BASE = 'invoices'

_EMAIL_BASE_FOLDER = "email"
_PUBLIC_BASE_FOLDER = "public"
_ERROR_BASE_FOLDER = "errors"


class APP_TEMPLATES:
    class ACCOUNTS:
        PROFILE = f'{_ACCOUNTS_BASE}/profile.html'
        SETTINGS = f'{_ACCOUNTS_BASE}/settings.html'
        ONBOARDING = f'{_ACCOUNTS_BASE}/onboarding.html'
        ACTIVATION = f'{_ACCOUNTS_BASE}/activation.html'
        DASHBOARD = f'{_ACCOUNTS_BASE}/dashboard.html'
        ANALYST_DASHBOARD = f'{_ACCOUNTS_BASE}/analyst-dashboard.html'

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
            
    class PRODUCTS:
        LIST = f'{_PRODUCTS_BASE}/store-products.html'
        DETAIL = f'{_PRODUCTS_BASE}/detail.html'
        ADD = f'{_PRODUCTS_BASE}/add.html'
        EDIT = f'{_PRODUCTS_BASE}/edit.html'
        
    class SALES:
        LIST = f'{_SALES_BASE}/list.html'
        DETAIL = f'{_SALES_BASE}/detail.html'
        ADD = f'{_SALES_BASE}/record-sale.html'
        EDIT = f'{_SALES_BASE}/edit.html'
        
    class INVOICE:
        VIEW=f'{_INVOICES_BASE}/inv-view.html'
        INVOICE_PDF=f'{_INVOICES_BASE}/inv-pdf.html'
        
class EMAIL_TEMPLATES:
    ACCOUNT_ACTIVATION = f'{_EMAIL_BASE_FOLDER}/account-activation.html'
    ACCOUNT_RECOVERY = f'{_EMAIL_BASE_FOLDER}/account-recovery.html'
    
class ERROR_PAGES:
    FORBIDDEN = f'{_ERROR_BASE_FOLDER}/403.html'
    NOT_FOUND = f'{_ERROR_BASE_FOLDER}/404.html'
    INETERNAL_ERROR = f'{_ERROR_BASE_FOLDER}/500.html'
    
class PUBLIC:
    INDEX = f'{_PUBLIC_BASE_FOLDER}/index.html'
    COMING_SOON = f'{_PUBLIC_BASE_FOLDER}/coming-soon.html'
    FEEDBACK = f'{_PUBLIC_BASE_FOLDER}/feedback.html'
    