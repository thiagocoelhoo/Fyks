import re


def read(file):
    lines = file.read().split('\n')
    for line in lines:
        result = re.match(line, patterns)