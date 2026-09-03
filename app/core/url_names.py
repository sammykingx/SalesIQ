from types import SimpleNamespace


# appName_grpNAme_urlName

ACCOUNTS = SimpleNamespace(
    PROFILE='accounts_profile',
    DASHBOARD='accounts_dashboard',
    SETTINGS='accounts_settings',
    ONBOARDING='accounts_onboarding',
    ACTIVATION='accounts_activation',
    AUTH=SimpleNamespace(
        LOGIN='accounts_auth_login',
        LOGOUT='accounts_auth_logout',
        REGISTER='accounts_auth_register',
        PASSWORD_RESET='accounts_auth_password_reset',
        PASSWORD_CHANGE='accounts_auth_password_change',
    ),
)

PRODUCTS = SimpleNamespace(
    LIST='products_list',
    ADD='products_add',
    DETAIL='products_detail',
    EDIT='products_edit',
)

CUSTOMERS = SimpleNamespace(
    LIST='customers_list',
    ADD='customers_add',
    DETAIL='customers_detail',
    EDIT='customers_edit',
)

SALES = SimpleNamespace(
    LIST='sales_list',
    ADD='sales_add',
    DETAIL='sales_detail',
    EDIT='sales_edit',
)

INVOICES = SimpleNamespace(
    LIST='invoices_list',
    ADD='invoices_add',
    DETAIL='invoices_detail',
    EDIT='invoices_edit',
)
