def create_default_admin(
    username="admin", email="admin@example.com", password="111111"
):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    User.objects.create_superuser(username, email, password)
