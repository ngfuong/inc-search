from contextlib import closing

__all__ = ['gen_source']


def gen_source(source):
    """
    TODO
    """
    if hasattr(source, 'read'):
        input_file = source
    else:
        input_file = open(source, 'r')

    with closing(input_file):
        for line in input_file:
            yield line.strip()
