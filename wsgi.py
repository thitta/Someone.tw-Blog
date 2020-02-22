import os

from django.core.wsgi import get_wsgi_application

print("---------- Someone-Blog Settings ----------")
print(f"$SOMEONE_USE_PROD_CFG   : {os.getenv('SOMEONE_USE_PROD_CFG')}")
print(f"$SOMEONE_USE_PROD_DB    : {os.getenv('SOMEONE_USE_PROD_DB')}")
print(f"$DJANGO_SETTINGS_MODULE : {os.getenv('DJANGO_SETTINGS_MODULE')}")
print("-------------------------------------------")

application = get_wsgi_application()
