from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver


DEMO_USERNAME = 'susan'
DEMO_PASSWORD = 'susan123'
DEMO_EMAIL = 'susanacharya.sp@gmail.com'


def ensure_demo_user():
    user, _ = User.objects.get_or_create(
        username=DEMO_USERNAME,
        defaults={'email': DEMO_EMAIL},
    )
    user.email = DEMO_EMAIL
    user.set_password(DEMO_PASSWORD)
    user.save(update_fields=['email', 'password'])


@receiver(post_migrate)
def seed_demo_user_on_migrate(sender, **kwargs):
    if getattr(sender, 'name', None) != 'users':
        return
    ensure_demo_user()