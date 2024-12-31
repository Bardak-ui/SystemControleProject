import os
import sys

# Укажите путь к проекту
project_path = '/home/Bardak/SystemControleProject'
if project_path not in sys.path:
    sys.path.append(project_path)

# Укажите путь к виртуальному окружению
activate_env = '/home/Bardak/SystemControleProject/venv/bin/activate'
exec(open(activate_env).read(), {'__file__': activate_env})

# Укажите настройки Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'SystemControleProject.settings'

# Загрузка WSGI приложения
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
