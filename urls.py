from django.contrib import admin
from django.urls import path
from Chat.views import LoginView, RegisterView, CreateMessageView, \
    WorkMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    #path('logout/', LogoutView.as_view()),
    path('messages/', CreateMessageView.as_view()),
    path('messages/<int:message_id>/', WorkMessageView.as_view()),
]
