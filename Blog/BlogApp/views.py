from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string

from .models import UserProfile, Post, Like_Dislike
from django.contrib import messages, auth
from .forms import PostForm


def signup(request):
    if request.method == "POST":
        # import pdb
        # pdb.set_trace()
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password2)
        UserType = request.POST.get('UserType')
        print(UserType)
        if password1 == password2:
            if UserProfile.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('/signup')
            elif UserProfile.objects.filter(email=email).exists():
                messages.info(request, 'EMAIL taken')
                return redirect('/signup')
            else:
                user = UserProfile.objects.create_user(username=username, email=email, password=password1,
                                                       UserType=UserType)
                user.save()
                print("User created")
                return redirect('/')
        else:
            messages.info(request, 'password not matching...')
            return redirect('/signup')
    else:
        return render(request, 'BlogApp/Registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.UserType == "Publisher":
                login(request, user)
                print(request.user)
                return redirect('/Publish_Post')
            else:
                login(request, user)
                print(request.user)
                return redirect('/All_Post')
        else:
            return render(request, 'BlogApp/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'BlogApp/login.html')


@login_required(login_url='/')
def Publish_Post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.user
        content = request.POST.get('content')
        status = request.POST.get('status')
        postImg = request.FILES.get('img')
        print("Image  : ", postImg)
        if Post.objects.filter(title=title).exists():
            messages.info(request, 'Username taken')
            return redirect('/Publish_Post/')
        elif Post.objects.filter(content=content).exists():
            messages.info(request, 'content')
            return redirect('/Publish_Post/')
        elif Post.objects.filter(postImg=postImg).exists():
            messages.info(request, 'EMAIL taken')
            return redirect('/Publish_Post/')
        else:
            post = Post(title=title, content=content, postImg=postImg,
                        status=status, author=author)
            post.save()
            return redirect('/Publish_Post/')
    else:
        return render(request, 'BlogApp/Publish_Post.html')


@login_required(login_url='/')
def Publish_Post1(request):
    # post = PostForm()
    # return render(request, "BlogApp/Publish_Post1.html", {'form': post})
    if request.method == "POST":
        print(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save(commit=False)
                # return redirect('/show')
            except:
                pass
    else:
        form = PostForm()
    return render(request, 'BlogApp/Publish_Post1.html', {'form': form})


@login_required(login_url='/')
def All_Post(request):
    Allposts = Post.objects.all()
    return render(request, 'BlogApp/blog_list.html', {'Allposts': Allposts})


@login_required(login_url='/')
def blogpost(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'BlogApp/blog_detail.html', {'post': post})


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    return redirect('/')





# @login_required(login_url='/')
# def postpreference(request, postid, userpreference):
#     if request.method == "POST":
#         Allposts = get_object_or_404(Post, id=postid)
#         print('Allposts = ', Allposts)
#         obj = ''
#         valueobj = ''
#         try:
#             obj = Preference.objects.get(user=request.user, post=Allposts)
#             print('obj = ', obj)
#             valueobj = obj.value  # value of userpreference
#             valueobj = int(valueobj)
#             userpreference = int(userpreference)
#             if valueobj != userpreference:
#                 obj.delete()
#                 upref = Preference()
#                 upref.user = request.user
#                 upref.post = Allposts
#                 upref.value = userpreference
#                 if userpreference == 1 and valueobj != 1:
#                     Allposts.likes += 1
#                     Allposts.dislikes -= 1
#                 elif userpreference == 2 and valueobj != 2:
#                     Allposts.dislikes += 1
#                     Allposts.likes -= 1
#                 upref.save()
#                 Allposts.save()
#                 context = {'Allposts': Allposts,
#                            'postid': postid}
#                 return render(request, 'BlogApp/blog_detail.html', context)
#                 # return redirect('blogpost')
#             elif valueobj == userpreference:
#                 obj.delete()
#                 if userpreference == 1:
#                     Allposts.likes -= 1
#                 elif userpreference == 2:
#                     Allposts.dislikes -= 1
#                 Allposts.save()
#                 context = {'Allposts': Allposts,
#                            'postid': postid}
#                 return render(request, 'BlogApp/blog_detail.html', context)
#                 # return redirect('blogpost')
#         except Preference.DoesNotExist:
#             upref = Preference()
#             upref.user = request.user
#             upref.post = Allposts
#             upref.value = userpreference
#             userpreference = int(userpreference)
#             if userpreference == 1:
#                 Allposts.likes += 1
#             elif userpreference == 2:
#                 Allposts.dislikes += 1
#             upref.save()
#             Allposts.save()
#             context = {'Allposts': Allposts,
#                        'postid': postid}
#             return render(request, 'BlogApp/blog_detail.html', context)
#             # return redirect('blogpost')
#     else:
#         Allposts = get_object_or_404(Post, id=postid)
#         context = {'Allposts': Allposts,
#                    'postid': postid}
#         return render(request, 'BlogApp/blog_detail.html', context)

@login_required(login_url='/')
def like_dislike(request):
    if request.is_ajax() and request.method == "POST":
        print('post=', request.POST)
        post = request.POST.get('postid')
        print('post', post)
        # user = request.POST.get('usrid')
        user = request.user
        vote = request.POST.get('like_dislike')
        if vote == 'Like':
            data = Like_Dislike(post=post, user=user, vote=vote)
            return JsonResponse({'success': True, 'data': data})
        return JsonResponse({'success': False})


