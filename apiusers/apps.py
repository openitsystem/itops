from django.apps import AppConfig


class ApiusersConfig(AppConfig):
    name = 'apiusers'
    # signals 配置
    # def ready(self):
    #     import apiusers.signals