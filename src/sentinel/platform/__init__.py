__all__ = ['linux']

from platform import uname

def load_platform_api():
    system = uname()
    if system[0] == 'Linux':
        import linux
        return linux
    else:
        return None
