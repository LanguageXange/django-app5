# Trip Tracking App

This app allows user to track their vacations with notes.
The project features login page, signup page, and application dashboard that allows users to create and edit their trips with photos.

## User Auth

Trip -> User is many to one relationship (`models.ForeignKey`)

```python
#user auth
from django.contrib.auth import get_user_model
User = get_user_model()


# Trip model
class Trip(models.Model):
    city = models.CharField(max_length=50)
    countryCode = models.CharField(max_length=2)
    start_date = models.DateField(blank=True, null=True) #optional
    end_date = models.DateField(blank=True, null=True) #optional
    # many to one relationship
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "mytrips")


    def __str__(self):
        return self.city


```

## Enable Images to be stored in DB

`pip install pillow`

Update `settings.py` and `urls.py`

```python
# urls.py
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('triptrack.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



# settings.py
MEDIA_URL = '/media/'  # www.mysite.com/media/img-1
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') # path to the actual file

```

## Built-in Django Auth to Set Up Auth URLs

we can go to `env/lib/django/contrib/auth/urls.py`
We can see that in `auth/views.py` the LoginView expects `template_name = "registration/login.html"`

```python
# urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('triptrack.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]



# settings.py
'DIRS': [os.path.join(BASE_DIR,'templates')]
# so that it can find the templates/registration/login.html

# Where should the user go after login - if not next
LOGIN_REDIRECT_URL = 'trip-list'

```

Resource: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

- accounts/ login/ [name='login']
- accounts/ logout/ [name='logout']
- accounts/ password_change/ [name='password_change']
- accounts/ password_change/done/ [name='password_change_done']
- accounts/ password_reset/ [name='password_reset']
- accounts/ password_reset/done/ [name='password_reset_done']
- accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
- accounts/ reset/done/ [name='password_reset_complete']
