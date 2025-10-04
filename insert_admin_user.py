import os
import django
from django.utils import timezone

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from mbamain.models import AUser  # adjust import if your model lives elsewhere


def insert_admin_user():
    """Insert a new admin user into mbamain_auser table with encrypted password."""

    email = "admin2@uj.ac.za"
    password_plain = "admin2@uj.ac.za"
    hashed_pw = make_password(password_plain)

    # Create and save the new user
    user = AUser.objects.create(
        username=email,
        email=email,
        password=hashed_pw,
        first_name="Admin2",
        last_name="UJ",
        is_superuser=True,
        is_staff=True,
        is_active=True,
        date_joined=timezone.now(),
        user_type=0,
        role_type=0,
        has_profile=False,
        has_signature=False,
        has_cv=False,
    )

    print(f"✅ User inserted successfully: {user.username}")
    print(f"🔐 Encrypted Password: {hashed_pw}")
    print(f"🕒 Date Joined: {user.date_joined}")


if __name__ == "__main__":
    insert_admin_user()
