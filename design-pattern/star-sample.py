# -*- coding: utf-8 -*-


def add_function(a=1, b=2):
    return a+b


def parse_names(*args):
    return args

def parse_values(**d):
    return [i for i in d.values()]

def parse_dict(**kwargs):
    return kwargs


print('https://medium.com/@rahulkp220/python-args-and-kwargs-5fb545b7a538')
print('* array as multiple params ...')
print(f'add_function(*[1, 2]) = {add_function(*[1, 2])}')

print('*args as function arguments, params convert to tuple ...')
print(f'parse_names("a", "b", "c") = {parse_names("a", "b", "c")}')

print('** dict as multiple params&values ...')
result = parse_values(**{"a":1, "b":2})
# escape character for brace
print(f'parse_values(**{{"a":1, "b":2}} ) = {result}')

print('**kwargs as pairs key:value convert to dict ...')
print(f'parse_dict(a=1, b=2) = {parse_dict(a=1, b=2)}')