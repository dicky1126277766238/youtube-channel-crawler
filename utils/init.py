import sys
import os


def init_db():
    sys.dont_write_bytecode = True
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting')
    import django
    django.setup()
