from django.contrib import admin

# Register your models here.
from app.users.models import User

admin.site.register(User)