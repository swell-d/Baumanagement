import os


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BM.settings')
    print('http://127.0.0.1:8000/')
    os.system('python manage.py runserver 0.0.0.0:8000')


if __name__ == '__main__':
    main()
