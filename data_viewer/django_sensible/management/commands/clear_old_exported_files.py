import os
from django.conf import settings
from django.core.management import BaseCommand
import time


class Command(BaseCommand):

	def handle(self, *args, **options):
		for filename in os.listdir(settings.EXPORTED_DATA_FOLDER):
			if not filename.endswith(settings.EXPORT_FILE_SUFFIX):
				continue
			file_path = os.path.join(settings.EXPORTED_DATA_FOLDER, filename)
			last_modified = os.path.getmtime(file_path)
			if time.time() - int(last_modified) > 3600:
				os.remove(file_path)