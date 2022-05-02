import os


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    main()
