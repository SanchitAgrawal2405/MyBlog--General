from django.shortcuts import render,redirect
from .models import Post
from .forms import PostForm,PostUpdateForm,CommentForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,'blog/about.html')

    
@login_required
def index(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user 
            instance.save() 
            return redirect('index')
    else:
        form = PostForm()
    context ={
        'posts' : posts ,
        'form' : form
    }
    return render(request,'blog/index.html',context)

@login_required
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('post-detail' , pk=post.id)
    else:
        c_form = CommentForm()
    context = {
        'post': post ,
        'c_form': c_form ,
    }
    return render(request,'blog/post_detail.html',context)

@login_required
def post_edit(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail',pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context={
        'post': post ,
        'form': form ,
    }
    return render(request,'blog/post_edit.html',context)

@login_required
def post_delete(request , pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context ={
        'post': post,
    }
    return render(request,'blog/post_delete.html',context)