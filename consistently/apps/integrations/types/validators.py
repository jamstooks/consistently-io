from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class RequiredIfActive(object):
    """
    This validator makes it easy to add required fields to an Integration
    serializer that are only required when the integration `is_active`.
    """
    missing_message = _('This field is required when active.')

    def __init__(self, fields):
        self.fields = fields
        self.serializer_field = None

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)

    def enforce_required_fields(self, attrs):
        missing_items = {
            field_name: self.missing_message
            for field_name in self.fields
            if field_name not in attrs or attrs[field_name] == None
        }
        if missing_items:
            raise ValidationError(missing_items, code='required')

    def __call__(self, attrs):
        if 'is_active' in attrs and attrs['is_active']:
            self.enforce_required_fields(attrs)
