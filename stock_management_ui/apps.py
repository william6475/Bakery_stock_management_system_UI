from django.apps import AppConfig


class StockManagementUiConfig(AppConfig):
    name = 'stock_management_ui'

    def ready(self):
        import stock_management_ui.signals
