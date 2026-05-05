from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

DEMO_USERNAME = 'susanacharya'
DEMO_PASSWORD = 'susan123'
DEMO_EMAIL = 'susanacharya.sp@gmail.com'


def seed_demo_user():
    """Create or reset the demo account. Called once after migrations."""
    user, created = User.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={'email': DEMO_EMAIL},
    )
    if created or not user.check_password(DEMO_PASSWORD):
        user.email = DEMO_EMAIL
        user.set_password(DEMO_PASSWORD)
        user.save(update_fields=['email', 'password'])


@receiver(post_migrate)
def on_migrate(sender, **kwargs):
    if getattr(sender, 'name', None) == 'users':
        seed_demo_user()
