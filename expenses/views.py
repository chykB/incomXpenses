from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime


# Create your views here.
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(
            amount__startswith=search_str, owner=request.user) | Expense.objects.filter(
            date__startswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get("page")
    page_object = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "expenses":expenses,
        "page_object":page_object,
        "currency":currency
    }
    return render(request, "expenses/index.html", context)

@login_required(login_url="/authentication/login")
def add_expences(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "values": request.POST
    }
    if request.method == "GET":
        return render(request, "expenses/add_expenses.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expenses.html", context)
        date = request.POST["expense_date"]
        if not date:
            messages.error(request, "Date is required")
            return render(request, "expenses/add_expenses.html", context)
   
        description = request.POST["description"]
        
        category = request.POST["category"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/add_expenses.html", context)
    Expense.objects.create(owner=request.user, amount=amount, description=description, 
                           date=date, category=category)
    messages.success(request, "Expense saved successfully")
    return redirect("index")


def edit_expenses(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "values": expense,
        "categories" :categories,
    }
    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit-expense.html", context)
        date = request.POST["expense_date"]
        if not date:
            messages.error(request, "Date is required")
            return render(request, "expenses/edit-expense.html", context)
   
        description = request.POST["description"]
        
        category = request.POST["category"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/edit-expense.html", context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.description=description
        expense.date=date
        expense.category=category
        expense.save()

        messages.success(request, "Expense updated successfully")
        return redirect("index")
        # messages.info(request, "Handling post form")
        # return render(request, "expenses/edit-expense.html", context)

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("index")

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(
        date__gte=six_months_ago, 
        date__lte=todays_date, 
        owner=request.user)
    expense_dict = {}

    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))


    def get_expense_category_amount(category):
        amount = 0
        filtered_expenses = expenses.filter(category=category)
        for item in filtered_expenses:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            expense_dict[y] = get_expense_category_amount(y)
    return JsonResponse({"expense_category_data": expense_dict}, safe=False)

    
def stats_view(request):
    return render(request, "expenses/stats.html")
    
