from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from django.core.exceptions import ValidationError


# Create your views here.
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': list_, 'error': error})


# def add_item(request, list_id):
#     List_ = List.objects.get(id=list_id)
#     Item.objects.create(text=request.POST['item_text'], list=List_)
#     return redirect('/lists/%d/' % (List_.id,))


def new_list(request):
    List_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=List_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        List_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(List_)


@csrf_exempt
def home_page(request):
    return render(request, 'home.html')
