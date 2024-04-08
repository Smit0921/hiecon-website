from django.contrib import admin
from django.urls import path, include
from .import views
from .views import *

urlpatterns = [
    path('', views.Index,name='index'),
    path('about/', views.About,name='about'),
    path('services/', views.Service,name='services'),
    path('contact/', views.Contact,name='contact'),
    path('team/', views.Team,name='team'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('register/', views.create_user,name='register'),
    path('login/', views.Login_user,name='login'),
    path('logout/', views.Logout_view,name='logout'),
    path('cart/', views.view_cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('update_quantity/<int:cart_product_id>/', update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:cart_product_id>/', remove_from_cart, name='remove_from_cart'),
    path('submit_cart/', submit_cart, name='submit_cart'),
    path('check_availability/', check_availability, name='check_availability'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('solution/<str:solution>/', SolutionDetailView.as_view(), name='solution_detail'),
    # path('solution/<str:solution>/',SolutionDetailView.as_View(),name='solution_detail'),
    path('subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('handle_query_form/', handle_query_form, name='handle_query_form'),
    path('your-endpoint-for-fetching-solution-details/<str:category>/', SolutionDetailView.as_view(), name='fetch-solution-details'),


] 