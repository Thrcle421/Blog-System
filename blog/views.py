from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, reverse, redirect
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from blog.forms import PubBlogForm
from blog.models import BlogCategory, Blog, BlogComment
from django.db.models import Q

# Create your views here.


def index(request):
    blogs = Blog.objects.all()
    return render(request, "index.html", context={"blogs": blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404
    return render(request, "blog_detail.html", {"blog": blog})

@require_http_methods(["GET", "POST"])
@login_required()
def pub_blog(request):
    if request.method == "GET":
        categories=BlogCategory.objects.all()
        return render(request, "pub_blog.html",context={"categories": categories})
    else:
        forms = PubBlogForm(request.POST)
        print(forms)
        if forms.is_valid():
            title = forms.cleaned_data.get("title")
            category_id = forms.cleaned_data.get("category")
            content = forms.cleaned_data.get("content")
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': 'blog is successfully released', 'data': {'blog_id': blog.id}})
        else:
            print(forms.errors)
            return JsonResponse({'code': 400, 'message': 'bad request'})

@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get("blog_id")
    content = request.POST.get("content")
    BlogComment.objects.create(blog_id=blog_id, content=content,author=request.user)
    return redirect(reverse('blog:blog_detail',kwargs={'blog_id': blog_id}))

@require_GET
def search_blog(request):
    q=request.GET.get("q")
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request, 'index.html', {'blogs': blogs})