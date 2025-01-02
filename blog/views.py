from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, reverse, redirect
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash

from blog.forms import PubBlogForm
from blog.models import BlogCategory, Blog, BlogComment
from django.db.models import Q

# Create your views here.


def index(request):
    page = request.GET.get('page', 1)
    blogs = Blog.objects.all().order_by('-pub_time')
    paginator = Paginator(blogs, 2)  # 10 posts per page
    page_obj = paginator.get_page(page)
    return render(request, "index.html", context={"page_obj": page_obj})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
        # Get comments and paginate
        page = request.GET.get('page', 1)
        comments = blog.comments.all().order_by('-pub_time')
        paginator = Paginator(comments, 2)  # 10 comments per page
        comments_page = paginator.get_page(page)
        return render(request, "blog_detail.html", {
            "blog": blog,
            "comments_page": comments_page
        })
    except Blog.DoesNotExist:
        raise Http404


@require_http_methods(["GET", "POST"])
@login_required()
def pub_blog(request):
    if request.method == "GET":
        categories = BlogCategory.objects.all()
        return render(request, "pub_blog.html", context={"categories": categories})
    else:
        forms = PubBlogForm(request.POST)
        print(forms)
        if forms.is_valid():
            title = forms.cleaned_data.get("title")
            category_id = forms.cleaned_data.get("category")
            content = forms.cleaned_data.get("content")
            blog = Blog.objects.create(
                title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': 'blog is successfully released', 'data': {'blog_id': blog.id}})
        else:
            print(forms.errors)
            return JsonResponse({'code': 400, 'message': 'bad request'})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get("blog_id")
    content = request.POST.get("content")
    BlogComment.objects.create(
        blog_id=blog_id, content=content, author=request.user)
    return redirect(reverse('blog:blog_detail', kwargs={'blog_id': blog_id}))


@require_GET
def search_blog(request):
    query = request.GET.get('q', '')
    if query:
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-pub_time')

        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 2)
        page_obj = paginator.get_page(page)

        return render(request, "index.html", {
            "page_obj": page_obj,
            "search_query": query
        })
    return redirect('blog:index')


@login_required
def profile(request):
    return render(request, "profile.html", {
        "user": request.user
    })


@login_required
def settings(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(old_password):
            return render(request, "settings.html", {"error": "Current password is incorrect"})

        if new_password != confirm_password:
            return render(request, "settings.html", {"error": "New passwords do not match"})

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return render(request, "settings.html", {"success": "Password updated successfully"})

    return render(request, "settings.html")
