import re

def specific_parse_arg_string(input_str, delimiter):
    if not isinstance(input_str, str) or not isinstance(delimiter, str):
        raise TypeError('Input and delimiter must be strings')
    result = input_str.split(delimiter)
    if len(result) == 1 and result[0] == '':
        return ['']
    if len(result) > 1 and result[-1] == '':
        result[-1] = ''
    return result

def parse_arg_string(input_str, delimiter):
    return specific_parse_arg_string(input_str, delimiter)

def parse_D_option(input_str):
    if not isinstance(input_str, str):
        raise TypeError('Input must be a string')
    parts = parse_arg_string(input_str, ':')
    if len(parts) < 2:
        raise ValueError('Invalid -D option')
    listen = parts[0]
    new_connection_chain = parts[1]
    return listen, new_connection_chain

def parse_L_option(input_str):
    if not isinstance(input_str, str):
        raise TypeError('Input must be a string')
    parts = parse_arg_string(input_str, ':')
    if len(parts) < 3:
        raise ValueError('Invalid -L option')
    bind_options = parts[0]
    remote_host = parts[1]
    remote_port = parts[2]
    return bind_options, remote_host, remote_port