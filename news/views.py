from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import redirect, render
import datetime as dt

from news.models import NewsLetterRecipients
from .forms import NewsLetterForm
from django.http.response import Http404

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def news_of_day(request):
    date = dt.date.today()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['email'] #cleaned-data property is a dictionary that saves values of the form.
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name = name,email = email)
            recipient.save()
            HttpResponseRedirect('news_of_day')
    else:
        form = NewsLetterForm()
    return render(request, 'all-news/today-news.html', {"date": date,"letterForm": form,})

def past_days_news(request,past_date):

    try:
        # Converts data from string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        #Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_of_day)
    
    return render(request, 'all-news/past-news.html', {"date": date})


