from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('code-compiler/<int:qus_id>/', code_Compiler_view, name='code_Compiler_view'),
    path('logout/', logout_view, name='logout'),
]
