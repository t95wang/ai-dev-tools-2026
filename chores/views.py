from django.shortcuts import redirect, render

from .forms import ChoreForm


def chore_list(request):
    """Minimal redirect target; the chore list is implemented in Task #3."""
    return render(request, "chores/chore_list.html")


def chore_create(request):
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chores:list")
    else:
        form = ChoreForm()

    return render(request, "chores/chore_form.html", {"form": form})
