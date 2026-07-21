from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Category, Dealer, Enquiry, Guide, SupplierApplication, Tool,
)


def _active_categories():
    return Category.objects.filter(is_active=True)


def home(request):
    cats = _active_categories()
    ctx = {
        "categories": cats,
        "tools": Tool.objects.filter(is_active=True)[:3],
        "featured_dealers": Dealer.objects.filter(is_active=True, is_verified=True)[:3],
        "n_categories": cats.count(),
        "n_dealers": Dealer.objects.filter(is_active=True).count(),
        "n_tools": Tool.objects.filter(is_active=True).count(),
    }
    return render(request, "directory/home.html", {**ctx, "nav": "home"})


def solutions(request):
    return render(request, "directory/solutions.html", {"categories": _active_categories(), "nav": "solutions"})


def category_detail(request, slug):
    cat = get_object_or_404(Category, slug=slug, is_active=True)
    dealers = cat.dealers.filter(is_active=True)
    return render(request, "directory/category.html", {"cat": cat, "dealers": dealers, "nav": "solutions"})


def dealers(request):
    qs = Dealer.objects.filter(is_active=True).prefetch_related("categories")
    cat = request.GET.get("cat", "")
    city = request.GET.get("city", "")
    q = request.GET.get("q", "").strip()
    if cat:
        qs = qs.filter(categories__slug=cat)
    if city:
        qs = qs.filter(city=city)
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(area__icontains=q)
    qs = qs.distinct()
    cities = (
        Dealer.objects.filter(is_active=True)
        .values_list("city", flat=True).distinct().order_by("city")
    )
    ctx = {
        "dealers": qs,
        "categories": _active_categories(),
        "cities": cities,
        "sel_cat": cat,
        "sel_city": city,
        "q": q,
        "count": qs.count(),
    }
    return render(request, "directory/dealers.html", {**ctx, "nav": "dealers"})


def tools(request):
    return render(request, "directory/tools.html", {"tools": Tool.objects.filter(is_active=True), "nav": "tools"})


def tool_detail(request, slug):
    tool = get_object_or_404(Tool, slug=slug, is_active=True)
    return render(request, "directory/tool.html", {"tool": tool, "nav": "tools"})


def learn(request):
    return render(request, "directory/learn.html", {"guides": Guide.objects.filter(is_active=True), "nav": "learn"})


def guide_detail(request, slug):
    guide = get_object_or_404(Guide, slug=slug, is_active=True)
    return render(request, "directory/guide.html", {"guide": guide, "nav": "learn"})


def enquiry(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Enquiry.objects.create(
                name=name,
                phone=request.POST.get("phone", ""),
                city=request.POST.get("city", ""),
                interest=request.POST.get("interest", ""),
                property_type=request.POST.get("property_type", ""),
                message=request.POST.get("message", ""),
            )
            messages.success(request, "Thanks! Your enquiry has been received — we'll connect you with the right dealers shortly.")
            return redirect("enquiry")
        messages.error(request, "Please enter your name.")
    return render(request, "directory/enquiry.html", {"categories": _active_categories(), "nav": ""})


def list_business(request):
    if request.method == "POST":
        biz = request.POST.get("business_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        if biz and phone:
            SupplierApplication.objects.create(
                business_name=biz,
                contact_name=request.POST.get("contact_name", ""),
                phone=phone,
                city=request.POST.get("city", ""),
                services=request.POST.get("services", ""),
                message=request.POST.get("message", ""),
            )
            messages.success(request, "Application received! We'll review and get back to you on WhatsApp.")
            return redirect("list_business")
        messages.error(request, "Please enter your business name and phone number.")
    return render(request, "directory/list_business.html", {"categories": _active_categories(), "cities": ["Faridabad", "Delhi", "Gurugram", "Noida", "Ghaziabad"], "nav": "list"})


def about(request):
    return render(request, "directory/about.html", {"nav": ""})
