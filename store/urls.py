from django.urls import path

from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView 
from django.conf.urls import url
urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.update_item, name="update_item"),
	path('process_order/', views.processOrder , name="process_order"),

	url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
	

]