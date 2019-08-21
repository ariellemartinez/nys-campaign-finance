from django.urls import path
from . import views

urlpatterns = [
	path('<str:category_in>/<int:year>/<int:zip_code_3>', views.contributions, name='contributions')
]