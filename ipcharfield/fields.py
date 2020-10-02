from django.db.models import GenericIPAddressField
from netaddr import IPAddress

from db_field.lookups import RangeLookup, ContainsLookup, IExactLookup, ExactLookup
from ipcharfield.utils import leading_zeros_repr, ip_address_repr


class IPCharField(GenericIPAddressField):
    """
    IP field with a wide range of lookup types: lt, gt, lte, gte, contains, range.

    Implementation details:
    The idea is to use lexicographical order. The idea is that every string has the same length
    and thus we can compare with lt, gt and range whilst still being able to use contains.
    """

    description = 'An IP that can be looked by all the common operations (gt, lt, gte, etc) plus by substring'

    def to_python(self, value):
        if not value:
            return None
        return ip_address_repr(value)

    def from_db_value(self, value, *_args, **_kwargs):
        return self.to_python(value)

    def get_prep_value(self, value) -> (str, None):
        if value is None:
            return None
        if isinstance(value, str):
            value = IPAddress(value)
        return leading_zeros_repr(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def get_internal_type(self):
        return "IPCharField"

    def db_type(self, connection):
        return 'varchar(39)'


IPCharField.register_lookup(RangeLookup)
IPCharField.register_lookup(ContainsLookup)
IPCharField.register_lookup(IExactLookup)
IPCharField.register_lookup(ExactLookup)
