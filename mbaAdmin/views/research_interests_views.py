from django.shortcuts import redirect, render, reverse, get_object_or_404
from mbaAdmin.utils import is_admin
from mbamain.models import ResearchInterest
from django.contrib import messages
from django.http import HttpResponseNotFound

@is_admin
def researchInterest(request):
    per_page = 10
    page = request.GET.get("page", 0)
    search = request.GET.get("search", '')
    is_searching = True if search and  (not search == '') else False
    try:
        page = int(page)
        if page < 0:
            page = 0
    except ValueError:
        page = 0
    search_query = f"&search={search}" if is_searching else ""
    has_next = True
    next_page = page + 1
    prev_page = page - 1 if page > 0 else 0
    next_url = reverse("mba_admin:research_interest") + f"?page={next_page}{search_query}"
    prev_url = reverse("mba_admin:research_interest") + f"?page={prev_page}{search_query}"

    if is_searching:
        research_interests = ResearchInterest.objects.all().filter(name__icontains=search).order_by("created_at")[page * per_page:(page + 1) * per_page]
    else:
        research_interests = ResearchInterest.objects.all().order_by("created_at")[page * per_page:(page + 1) * per_page]
    if len(research_interests) == 0 and page > 0:
        page = page - 1
        next_url = reverse("mba_admin:research_interest") + f"?page={page}{search_query}"
        return redirect(next_url)
    
    return render(request, "mbaAdmin/researchInterest.html", {
        "interests": research_interests,
        "next": next_url,
        "prev": prev_url,
        "has_next": has_next,
        "has_prev": True if page > 0 else False,
        "search": search
    })


@is_admin
def add_research_interest(request):
    if request.method == "POST":
        interest = request.POST.get("interest")
        try:
            ResearchInterest.objects.create(name=interest, created_by=request.user.email)  # Create a new research interest
            messages.success(request, "Research interest added successfully!")
            return redirect("mba_admin:research_interest")  # Redirect to the research interests page after adding
        except:
            messages.error(request, "Failed to add research interest. Please try again.")
            return redirect("mba_admin:add_research_interest")
        
    return HttpResponseNotFound()



@is_admin
def update_research_interest(request):
    if request.method == "POST":
        name = request.POST.get("name", '')
        id = request.POST.get("id", '')
        if name == '' or id == '':
            messages.error(request,f"Faild to update interest: name {name} id {id}")
            return redirect("mba_admin:research_interest")
        interest = get_object_or_404(ResearchInterest, pk=id)
        interest.name = name
        interest.save()
        messages.success(request,"updated research interest successfully")
    return redirect("mba_admin:research_interest")
    