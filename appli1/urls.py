from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path('',views.index,name="index"),
     path('dashboard/',views.dashboard_view,name="dashboard"),
     path('login/',views.login_view,name="login"),
     path('signup/',views.signup_view,name="signup"),
     path('logout/',views.logout_view,name="logged_out"),
     path('delete_product/<int:product_id>/',views.delete_product_view,name="delete_product"),
     path('delete_message/<int:message_id>/',views.delete_message_view,name="delete_message")

     
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
