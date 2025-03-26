from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.contrib import messages

# Create your views here.
@login_required(login_url="/authentication/login")
def index(request):
    categories = Category.objects.all()
    return render(request, "expenses/index.html")

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
