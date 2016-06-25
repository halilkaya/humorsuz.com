from django.shortcuts import render
from headline.helpers import NewsHelper


def index(request):
    nh = NewsHelper()

    data = {'news': []}
    for i in range(11):
        data['news'].append(nh.getHeadline(request))
    
    return render(request, 'index.html', data)
