import re

COMMAND_PREFIX = '/'


def is_command(text=''):
    return isinstance(text, str) and text.startswith(COMMAND_PREFIX)


def parse_command_id(text=''):
    return text.split()[0].split('@')[0] if is_command(text) else None


def parse_command_params(text=''):
    regexp = re.compile("/\w*(@\w*)*\s*([\s\S]*)", re.IGNORECASE)
    result = regexp.match(text)
    return result.group(2) if is_command(text) else None
