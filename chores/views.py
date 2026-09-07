from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ChoreClaimForm, ChoreForm
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


def chore_claim(request, chore_id):
    chore = get_object_or_404(Chore, pk=chore_id)

    if chore.status != Chore.Status.UNCLAIMED:
        messages.error(request, "This chore is no longer available to claim.")
        return redirect("chores:list")

    if request.method == "POST":
        form = ChoreClaimForm(request.POST)
        if form.is_valid():
            updated = Chore.objects.filter(
                pk=chore.pk,
                status=Chore.Status.UNCLAIMED,
            ).update(
                claimed_by=form.cleaned_data["name"],
                claimed_at=timezone.now(),
                status=Chore.Status.CLAIMED,
            )
            if updated:
                messages.success(request, "Chore claimed successfully.")
            else:
                messages.error(request, "This chore is no longer available to claim.")
            return redirect("chores:list")
    else:
        form = ChoreClaimForm()

    return render(
        request,
        "chores/chore_claim.html",
        {"chore": chore, "form": form},
    )
