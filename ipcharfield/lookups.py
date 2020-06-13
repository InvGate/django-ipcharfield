from django.db.models import Lookup
from netaddr import IPAddress


class RangeLookup(Lookup):
    lookup_name = 'range'

    def get_prep_lookup(self):
        if isinstance(self.rhs, (tuple, list)):
            if self.prepare_rhs and hasattr(self.lhs.output_field, 'get_prep_value'):
                return self.lhs.output_field.get_prep_value(self.rhs[0]), self.lhs.output_field.get_prep_value(self.rhs[1])
            else:
                return self.rhs
        else:
            raise LookupError('The lookup type must be a tuple or a list')

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        lhs_params.extend(*rhs_params)
        return "%s BETWEEN %s AND %s" % (lhs, rhs, rhs), lhs_params


class ContainsLookup(Lookup):
    lookup_name = 'contains'
    contains_key = 'LIKE'

    def transform_rhs(self):
        if not isinstance(self.rhs, str):
            raise LookupError('The contains param must be a str instance')

        if '.' not in self.rhs and ':' not in self.rhs:
            return [self.rhs]

        delimiter = '.' if '.' in self.rhs else ':'
        chunks_size = 3 if delimiter == '.' else 4
        value = self.rhs
        chunks = value.split(delimiter)
        last_chunk = chunks[-1]
        last_chunk = '{}{}'.format(''.join(['0' for _ in range(chunks_size - len(last_chunk))]), last_chunk)
        possible_last_chunks = [last_chunk]
        while possible_last_chunks[-1] != '000' and possible_last_chunks[-1][0] == '0':
            possible_last_chunks.append('{}0'.format(possible_last_chunks[-1][1:]))
        possible_contains = []
        for chunk in possible_last_chunks:
            chunks[-1] = chunk
            possible_contains.append('%{}%'.format(delimiter.join(chunks)))
        return possible_contains

    def get_prep_lookup(self):
        if isinstance(self.rhs, (str, IPAddress)):
            return tuple(self.transform_rhs())
        else:
            raise LookupError('The lookup type must be a tuple or a list')

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        lhs_params.extend(*rhs_params)
        return ' OR '.join(["{0} {1} {2}" for _ in range(len(*rhs_params))]).format(lhs, self.contains_key, rhs), lhs_params
