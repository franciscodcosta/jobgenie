import os
from azure.functions import TimerRequest
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobgenie.settings')
django.setup()

def main(mytimer: TimerRequest) -> None:
    call_command('check_old_cards')
