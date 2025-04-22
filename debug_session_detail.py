import os
import django
from django.template import Context, Template
from django.template.loader import get_template

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formation_assmat.settings')
django.setup()

from core.models import Session

# Investigate session with ID 3
session = Session.objects.get(id=3)

# Get the template
template = get_template('core/session_detail.html')

# Create a context
context = {
    'session': session,
    'trainers': session.trainers.all(),
}

# Render the template section for trainers
print("Trainers in context:", list(context['trainers']))
try:
    rendered_trainers = template.render(context)
    print("Rendered template contains trainers section")
except Exception as e:
    print(f"Error rendering template: {e}")
