from django.shortcuts import redirect, render

from .forms import ChoreForm
from .models import Chore


def chore_list(request):
    chores = Chore.objects.order_by("due_date", "title")
    return render(request, "chores/chore_list.html", {"chores": chores})


def chore_create(request):
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chores:list")
    else:
        form = ChoreForm()

    return render(request, "chores/chore_form.html", {"form": form})
