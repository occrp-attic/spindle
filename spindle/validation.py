from jsonschema import Draft4Validator, FormatChecker

from spindle.core import get_loom_config
from spindle.metadata import get_countries


format_checker = FormatChecker()


@format_checker.checks('country-code')
def is_country_code(code):
    if code is None or not len(code.strip()):
        return False
    return code in get_countries().keys()


def validate(data, schema):
    resolver = get_loom_config().resolver
    _, schema = resolver.resolve(schema)
    validator = Draft4Validator(schema, resolver=resolver,
                                format_checker=format_checker)
    return validator.validate(data, schema)
