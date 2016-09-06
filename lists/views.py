from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List


# Create your views here.
def view_list(request, list_id):
    List_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=List_)
    return render(request, 'list.html', {'items': items})


def new_list(request):
    List_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=List_)
    return redirect('/lists/the-only-list-in-the-world/')


@csrf_exempt
def home_page(request):
    return render(request, 'home.html')
