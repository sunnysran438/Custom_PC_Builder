from django.core.management.base import BaseCommand
import pc_builder.pc_builder_app.database_api as database_api

class Command(BaseCommand):
    help = 'Creates all database tables'

    def handle(self, *args, **options):
        try:
            database_api.create_tables()
            self.stdout.write(self.style.SUCCESS('Database tables created successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))