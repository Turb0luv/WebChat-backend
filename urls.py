from django.contrib import admin
from django.urls import path
from Chat.views import LoginView, RegisterView, LogoutView, CreateMessageView, DestroyMessageView, EditMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    #path('logout/', LogoutView.as_view()),
    path('messages/', CreateMessageView.as_view()),
    path('messages/<int:message_id>/', DestroyMessageView.as_view()),  # Using <int:message_id> to capture the ID
    path('messages/<int:message_id>/edit/', EditMessageView.as_view()),  # Using <int:message_id>
]
