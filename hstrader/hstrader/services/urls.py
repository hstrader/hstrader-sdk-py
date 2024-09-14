""" ACCOUNTS URLS """

_BASE_ACCOUNT_URL = "/api/v1/accounts"
_GETMYPROFILE = _BASE_ACCOUNT_URL + "/me"


""" AUTH URLS """
_BASE_AUTH_URL = "/auth/v1/oauth2"
_LOGIN_URL = _BASE_AUTH_URL + "/login?remember_me=true"
_LOGIN_URL_CREDENTIALS = _BASE_AUTH_URL + "/token?grant_type=client_credentials"
_REFRESH_URL = _BASE_AUTH_URL + "/refresh/token"
_LOGOUT_URL = _BASE_AUTH_URL + "/logout"


""" POSITIONS URLS """
_BASE_ORDER_URL = "/api/v1/positions"
URL_GETMYPOSITIONS = _BASE_ORDER_URL + "/accounts/me"
URL_GETMYPOSITIONSHISTORY = _BASE_ORDER_URL + "/accounts/me?active=false"
URL_UPDATEMYPOSITION_POSITION_ID = _BASE_ORDER_URL + "/%v/accounts/me"
URL_CLOSEMYPOSITION_POSITION_ID = _BASE_ORDER_URL + "/%v/accounts/me"


""" MARKET URLS """
_BASE_URL = "/api/v1/market"
_HISTORY_URL = _BASE_URL + "/history"


""" ORDERS URLS """
_BASE_ORDER_URL = "/api/v1/orders"
_URL_UPDATEMYORDER_ORDER_ID = _BASE_ORDER_URL + "/%v/accounts/me"
_URL_CANCELMYORDER_ORDER_ID = _BASE_ORDER_URL + "/%v/accounts/me"
_URL_GETMYORDERS = _BASE_ORDER_URL + "/accounts/me"
_URL_GETMYORDERSHistory = _BASE_ORDER_URL + "/accounts/me?active=false"
_URL_CREATEMYORDER = _BASE_ORDER_URL + "/accounts/me"


""" SYMBOLS URLS """
_BASE_ORDER_URL = "/api/v1/symbols"
_GETMYSYMBOLS = _BASE_ORDER_URL + "/me"
_GETMYSYMBOL = _BASE_ORDER_URL + "/me/by_name?symbol=%v"

""" DEALS URLS """
_BASE_DEAL_URL = "/api/v1/deals"
_URL_GETMYDEALS = _BASE_DEAL_URL + "/accounts/me"
