from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [ 
    path('', views.home, name='home'), 
    path('store/', views.store, name='store'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('parametre-de-compte/', views.account_setting, name='asetting'),
    #password change
    path('password-change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('detail/<int:product_id>', views.product_detail, name='detail_product'),
    #search products 
    path('search/', views.search_products, name='search_products'),
    path('commander/<int:product_id>', views.command, name='command'),
    #command
    path('commande-effectuee/', views.command_done, name='command_done'),
    path('listes-des-commandes/', views.command_list, name='orders'),
     path('supprimer-commande/<int:command_id>/', views.delete_command, name='delete_command'),

]