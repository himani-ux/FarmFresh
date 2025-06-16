"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AgroSeed import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home), 
    path('register/',views.register),
    path('login/', views.ulogin),
    path('logout/',views.ulogout),
    path('productsdetail/<pid>/',views.productdetails),
    path('products/',views.products),
    path('filterbycategory/<cat>/',views.filterbycategory),
    path('sortbyprice/<x>/',views.sortbyprice),
    path('filterbyprice/',views.filterbyprice),
    path('addtocart/<pid>/',views.addtocart),
    path('viewcart/',views.viewcart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('removecart/<cid>/',views.removecart),
    path('checkaddress/',views.checkaddress),
    path('edit-address/', views.edit_address, name='edit_address'),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('makepayment/',views.makepayment),
    path('mail/',views.mail_send),
    path('change_status/',views.change_status),
    path('myorders/',views.myorders),
    path('about_section/',views.about_section),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)