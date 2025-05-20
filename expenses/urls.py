from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='index'),
    path('expenses', views.add_expences, name="expenses"),
    path('edit_expense/<int:id>', views.edit_expenses, name="edit_expense"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete_expense"),
    path('search_expenses', csrf_exempt(views.search_expenses), name="search_expenses"),
    path("expense_category_summary", views.expense_category_summary, name="expense_category_summary"),
    path("stats", views.stats_view, name="stats"),
]