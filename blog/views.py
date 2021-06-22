from django.shortcuts import render
from django.utils import timezone
from models import Post,Comment
from .forms import PostForm,CommentForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import os
from django.conf import settings
from django.http import HttpResponse, Http404

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        comment_form=CommentForm(request.POST)
        comment_form.instance.author_id=request.user.id
        comment_form.instance.document_id=pk
        if comment_form.is_valid():
            comment=comment_form.save()
    comment_form=CommentForm()
    comments=post.comments.all()
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments,'comment_form':comment_form})

def post_new(request):
    if request.method== "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author= request.user
            post.published_date= timezone.now()
            post.save()
            return redirect('/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method== "POST":
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author= request.user
            post.published_date= timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('/')
