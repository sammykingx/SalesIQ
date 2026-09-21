from types import SimpleNamespace


# appName_grpNAme_urlName

ACCOUNTS = SimpleNamespace(
    PROFILE='accounts_profile',
    DASHBOARD='accounts_dashboard',
    ANALYST_DASHBOARD='accounts_analyst_dashboard',
    SETTINGS='accounts_settings',
    ONBOARDING='accounts_onboarding',
    ACTIVATION='accounts_activation',
    AUTH=SimpleNamespace(
        LOGIN='accounts_auth_login',
        LOGOUT='accounts_auth_logout',
        REGISTER='accounts_auth_register',
        PASSWORD_RESET='accounts_auth_password_reset',
        PASSWORD_CHANGE='accounts_auth_password_change',
        PASSWORD_UPDATE='accounts_auth_password_update',
    ),
    UPDATES=SimpleNamespace(
        PROFILE='accounts_updates_profile',
        BUSINESS='accounts_updates_business',
    )
)

BUSINESS_DATA = 'business_data'

PRODUCTS = SimpleNamespace(
    LIST='products_list',
    ADD='products_add',
    DETAIL='products_detail',
    UPDATE='products_update',
)

CUSTOMERS = SimpleNamespace(
    LIST='customers_list',
    ADD='customers_add',
    DETAIL='customers_detail',
    EDIT='customers_edit',
)

INVOICES = SimpleNamespace(
    CREATE='create_invoices',
    VIEW='view_invoices',
    DOWNLOAD='download_invoices',
    LIST_SALES='list_sales_invoices'
)

METRICS = SimpleNamespace(
    BIZ_REVENUE="metrics_business_revenue",
    BUSIEST_DAYS="metrics_business_busiest_day",
    PLATFORM_GMV="metrics_platform_gmv",
    PLATFORM_ADOPTION="metrics_platform_adoption",
)
