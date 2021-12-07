from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import redirect, render
import datetime as dt
from .email import send_welcome_email
from news.models import NewsLetterRecipients
from .forms import NewsLetterForm, NewArticleForm
from .models import Article
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, JsonResponse
from .serializer import MerchSerializer
from .models import  MoringaMerch
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['email'] #cleaned-data property is a dictionary that saves values of the form.
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name = name,email = email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_of_day')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news,"letterForm": form,})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to the mailing list'}
    return JsonResponse(data) # The JSON response will tell us the action ahs been completed successfully

def past_days_news(request,past_date):
    
    try:
        # Converts data from string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        #Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date,"news":news})


def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    return render(request, 'all-news/today-news.html', {"date": date,"news":news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})
    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login')
def article(request, article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist: #need to import from django.core
        raise Http404()
    return render(request, 'all-news/article.html', {"article":article})

@login_required(login_url='/accounts/login')
def new_article(request):
    current_user = request.user
    if request.method == "POST":
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')
    
    else:
        form = NewArticleForm()
    return render(request, 'all-news/new_article.html', {"form": form})

class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)