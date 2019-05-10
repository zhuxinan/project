from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from django.views.decorators.cache import cache_page
from PIL import Image,ImageDraw,ImageFont
import random,io
from .models import MyUser,Collections,Movies
from .views_constant import HTTP_OK, HTTP_USER_EXIST
import requests
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def index(request):
    allmovies = get_movies_image('https://www.vmovier.com/apiv3/index/getBanner')
    allimages = []
    for movie in allmovies:
        image = movie.get('image')
        images = str(image)
        allimages.append(images)

    movies = get_movies('https://www.vmovier.com/apiv3/post/getPostInCate?cateid=0&p=1')

    try:
        for movie in movies:
            movies = Movies()
            title = movie.get('title')
            movies.title = title

            ima = movie.get('image')
            movies.image = ima

            duration = movie.get('duration')
            movies.duration = duration
            movies.save()
    except Exception as e:
        amovies = Movies.objects.all()
        p = Paginator(amovies, 3)
        page = request.GET.get('page')
        try:
            amovie = p.page(page)
        except PageNotAnInteger:
            amovie = p.page(1)
        except EmptyPage:
            amovie = p.page(p.num_pages)
        return render(request,'movies/index.html',locals())
    amovies = Movies.objects.all()
    return render(request,'movies/index.html',locals())

def login(request):
    if request.method == 'GET':
        return render(request,'movies/login.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = MyUser.objects.filter(username=name).first()
        if user:
            password = user.password
            if pwd == password:
                request.session['username'] = name
                all_movies = get_movies_image('https://www.vmovier.com/apiv3/index/getBanner')
                all_images = []
                for movie in all_movies:
                    image = movie.get('image')
                    images = str(image)
                    all_images.append(images)
                # 获取全部电影
                a_movies = Movies.objects.all().order_by('-id')
                icons_url = "/static/upload/" + user.uicon.url
                user = user
                p = Paginator(a_movies, 3)
                page = request.GET.get('page')
                try:
                    amovie = p.page(page)
                except PageNotAnInteger:
                    amovie = p.page(1)
                except EmptyPage:
                    amovie = p.page(p.num_pages)
                return render(request,'movies/logined.html',locals())
            else:
                error = '密码错误'
                return render(request,'movies/login.html',locals())
        else:
            error = '用户不存在'
            return render(request, 'movies/login.html', locals())
    return render(request,'movies/login.html')

def register(request):
    if request.method == 'GET':
        return render(request,'movies/register.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        spwd = request.POST.get('s_password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        if pwd != spwd:
            error = '两次密码输入不一致'
            return render(request,'movies/register.html',locals())
        else:
            try:
                user = MyUser()
                user.username = name
                user.password = pwd
                user.email = email
                user.uicon = icon
                user.save()
            except Exception:
                return render(request,'movies/register.html')
        return render(request,'movies/login.html')

def collected(request,id):
    all_movies = get_movies_image('https://www.vmovier.com/apiv3/index/getBanner')
    all_images = []
    for movie in all_movies:
        image = movie.get('image')
        images = str(image)
        all_images.append(images)
    user = MyUser.objects.get(pk=id)
    name = user.username
    y_icons_url = "/static/upload/" + user.uicon.url
    collections = Collections.objects.filter(uid=id)
    return render(request,'movies/collected.html',locals())

def addcollect(request,id):
    movie = Movies.objects.get(pk=id)
    user = MyUser.objects.get(username=request.session.get('username'))
    try:
        Collections.objects.get(mid=movie)
        return redirect(reverse('movies:collected', args=str(user.id)))
    except:
        try:
            collection = Collections()
            collection.mid = movie
            collection.uid = user
            collection.save()
        except Exception:
            return HttpResponse('收藏失败')
        return redirect(reverse('movies:collected',args=str(user.id)))

def delcollect(request,id):
    try:
        movie = Movies.objects.get(pk=id)
        del_movie = Collections.objects.get(mid=movie)
        del_movie.delete()
        user = MyUser.objects.get(username=request.session.get('username'))
        return redirect(reverse('movies:collected',args=str(user.id)))
    except Exception:
        return HttpResponse('删除失败')

def userinfo(request,id):
    user = MyUser.objects.get(pk=id)
    icons_url = "/static/upload/" + user.uicon.url
    email = user.email
    name = user.username
    return render(request, 'movies/userinfo.html',locals())

def edituser(request,id):
    user = MyUser.objects.get(pk=id)
    a_movies = Movies.objects.all()
    all_movies = get_movies_image('https://www.vmovier.com/apiv3/index/getBanner')
    all_images = []
    for movie in all_movies:
        image = movie.get('image')
        images = str(image)
        all_images.append(images)
    if request.method == 'GET':
        return render(request, 'movies/userinfo.html',locals())
    else:
        email = request.POST['email']
        icon = request.FILES['uicon']
        user.email = email
        user.uicon = icon
        user.save()
        icons_url = "/static/upload/" + user.uicon.url
        return redirect(reverse('movies:logined',args=str(id)))

def logout(request):
    del request.session['username']
    return redirect(reverse('movies:index'))

def logined(request,id):
    user = MyUser.objects.get(pk=id)
    all_movies = get_movies_image('https://www.vmovier.com/apiv3/index/getBanner')
    all_images = []
    for movie in all_movies:
        image = movie.get('image')
        images = str(image)
        all_images.append(images)
    icons_url = "/static/upload/" + user.uicon.url
    a_movies = Movies.objects.all().order_by('-id')
    p = Paginator(a_movies, 3)
    page = request.GET.get('page')
    try:
        amovie = p.page(page)
    except PageNotAnInteger:
        amovie = p.page(1)
    except EmptyPage:
        amovie = p.page(p.num_pages)
    return render(request,'movies/logined.html',locals())

def get_movies_image(url):

    resp = requests.get(url)

    # print(resp.status_code)

    result = resp.json()

    movies = result.get("data")

    # print(movies)

    return movies

def get_movies(url):

    resp = requests.get(url)

    # print(resp.status_code)

    result = resp.json()

    movies = result.get("data")

    return movies