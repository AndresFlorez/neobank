from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import filter_none, force_real_str
from rest_framework.schemas import AutoSchema

deprecated_method = {"deprecated": True, "tags": ["deprecated"]}


def make_mock_object(**kwargs):
    return type("", (object,), kwargs)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue

        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."

        stringified_not_present = ", ".join(not_present)

        raise ImproperlyConfigured(f"{error_message_prefix} Could not find: {stringified_not_present}")

    return values


class CustomAutoSchema(SwaggerAutoSchema):
    def __init__(self, view, path, method, components, request, overrides, operation_keys=None):
        super(SwaggerAutoSchema, self).__init__(view, path, method, components, request, overrides)
        self._sch = AutoSchema()
        self._sch.view = view
        self.operation_keys = operation_keys
        self._method = method.lower()

    def get_view_method_doc(self):
        """Returns the doc in view method if is available else None"""
        try:
            doc = getattr(self._sch.view, self._method).__doc__  # type: str or None
            return doc if isinstance(doc, str) else None
        except AttributeError:
            return None

    def get_summary(self):
        """Return a summary description for this operation.

        If `operation_summary` is available will override the first line of the docstring.

        :return: the summary
        :rtype: str or None
        """
        doc = self.get_view_method_doc()
        first_string_line = doc.split(sep="\n")[0] if doc else None
        operation_summary = self.overrides.get("operation_summary", None)

        return operation_summary if operation_summary else first_string_line

    def get_summary_and_description(self):
        """Return an operation summary and description determined from the view's docstring.

        :return: summary and description
        :rtype: (str,str)
        """
        description = self.overrides.get("operation_description", None)
        summary = self.overrides.get("operation_summary", None)
        if description is None:
            description = self._sch.get_description(self.path, self.method) or ""
            description = description.strip().replace("\r", "")

            if description and (summary is None):
                # description from docstring... do summary magic
                summary, description = self.split_summary_from_description(description)
                summary = description

        return summary, description
