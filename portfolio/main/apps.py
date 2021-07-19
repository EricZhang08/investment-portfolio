from django.apps import AppConfig
import sys

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .models import User, Stock, Ticker
        import csv
        with open('/Users/ding/investment-portfolio/portfolio/main/ticker.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ticker.objects.get_or_create(
                    stock_name=row[1],
                    ticker=row[0],
                    )