from django.shortcuts import render, redirect
from userincome.models import UserIncome, Source
from django.core.paginator  import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse



# Create your views here.
@login_required(login_url="/authentication/login")
def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        income = UserIncome.objects.filter(
            amount__startswith=search_str, owner=request.user
            ) | UserIncome.objects.filter(
            date__startswith=search_str, owner=request.user
            ) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user
            ) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        print(data)
        return JsonResponse(list(data), safe=False)
    else:
        return JsonResponse("Invalid", safe=False)


@login_required(login_url="/authentication/login")
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get("page")
    page_object = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "income":income,
        "page_object":page_object,
        "currency":currency
    }
    return render(request, "income/index.html", context)
@login_required(login_url="/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context = {
        "sources": sources,
        "values": request.POST
    }
    if request.method == "GET":
        return render(request, "income/add_income.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/add_income.html", context)
        date = request.POST["income_date"]
        if not date:
            messages.error(request, "Date is required")
            return render(request, "income/add_income.html", context)
   
        description = request.POST["description"]
        
        source = request.POST["source"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "income/add_income.html", context)
        
        UserIncome.objects.create(owner=request.user, amount=amount, description=description, 
                           date=date, source=source)
        messages.success(request, "Income saved successfully")
        return redirect("income")


@login_required(login_url="/authentication/login")
def edit_income(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        "income": income,
        "values": income,
        "sources" :sources,
    }
    if request.method == "GET":
        return render(request, "income/edit-income.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/edit-income.html", context)
        date = request.POST["income_date"]
        if not date:
            messages.error(request, "Date is required")
            return render(request, "income/edit-income.html", context)
   
        description = request.POST["description"]
        
        source = request.POST["source"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "income/edit-income.html", context)
        
        income.owner = request.user
        income.amount = amount
        income.description=description
        income.date=date
        income.source=source
        income.save()

        messages.success(request, "Record updated successfully")
        return redirect("income")
        # messages.info(request, "Handling post form")
        # return render(request, "expenses/edit-income.html", context)

def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income deleted successfully")
    return redirect("income")