from django.urls import include, path
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("auth/", include(("neobank.authentication.urls", "authentication"))),
    path("users/", include(("neobank.users.urls", "users"))),
    path("bank_accounts/", include(("neobank.bank_accounts.urls", "bank_accounts"))),
]

if settings.USE_SWAGGER:
    schema_view = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version="v1",
            description="Neo Bank API documentation",
            contact=openapi.Contact(email="florezvalenciaandres@gmail.com"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
