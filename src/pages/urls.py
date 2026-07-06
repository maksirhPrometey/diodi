from django.urls import path

from src.pages import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('pro-nas/', views.about_view, name='about'),
    path('pro-nas/nasha-komanda/', views.team_list_view, name='team'),
    path('pro-nas/nasha-komanda/<slug:slug>/', views.team_member_view, name='team_member'),
    path('pro-nas/fotohalereia/', views.gallery_view, name='gallery'),
    path('posluhy/', views.services_view, name='services'),
    path('posluhy/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('labaratoriia/', views.laboratory_view, name='lab'),
    path('tsiny/', views.prices_view, name='prices'),
    path('vidhuky/', views.reviews_view, name='reviews'),
    path('kontakty/', views.contacts_view, name='contacts'),
    path('forms/<slug:variant>/', views.contact_form_partial_view, name='contact_form_partial'),
]
