from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ExpenseForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Project,Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
import json

# from .forms import
# Create your views here.

@login_required(login_url='loginPage')
def home(request):
    return render(request, 'first_app/index.html')

@login_required(login_url='loginPage')
def invoices(request):
    return render(request,'first_app/invoices.html')

@login_required(login_url='loginPage')
def accounts(request):
    return render(request, 'first_app/accounts.html')

def logoutPage(request):
    logout(request)
    return redirect('loginPage')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username = username , password = password)
            if user is not None:
                login(request, user)
                return redirect('invoices')
            else:
                messages.info(request,'Username or Password is wrong')
        context = {}
        return render(request, 'first_app/login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,f'The user {user} was created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'first_app/register.html',context)

def project_list(request):
    project_list = Project.objects.all()
    return  render(request, 'first_app/project-list.html',{'project_list': project_list})

def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        return render(request, 'first_app/project-detail.html', {'project': project, 'expense_list': project.expenses.all(), 'category_list': category_list})

    elif request.method == 'POST':
        # process the form_valid
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            amount = form.cleaned_data["amount"]
            category_name = form.cleaned_data["category"]

            category = get_object_or_404(Category, project=project, name=category_name)

            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    return HttpResponseRedirect(project_slug)
class ProjectCreateView(CreateView):
    model = Project
    template_name = 'first_app/add-project.html'
    fields = {'name','budget'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project = Project.objects.get(id=self.object.id),
                name = category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])