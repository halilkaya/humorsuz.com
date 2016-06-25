from django.shortcuts import render
from headline.models import Category, Object, Headline
from django.db.models import Q
from conj import conj
import random


class HeadlineFormatter(object):

    def __init__(self):
        self.background = None
        self.image = None

    def bool(self, text):
        if text == 'True':
            return True
        return False

    def __format__(self, text):
        params = text.split(', ')

        try:
            category = Category.objects.filter(name=params[0]).first()
            objects = Object.objects.filter(category=category)

            obj = random.choice(objects)

            if obj.image and obj.image != '':
                if obj.image_position == 1 and not self.background:
                    self.background = obj.image
                elif obj.image_position == 0 and not self.image:
                    self.image = obj.image

            if len(params) == 1:
                return obj.name
            elif len(params) == 3:
                return conj(obj.name, self.bool(params[1]), params[2])

            return params[0]
        except:
            return params[0]


def getHeadline():
    headlines = Headline.objects.all()
    formatter = HeadlineFormatter()
    headline = random.choice(headlines).text.format(random=formatter)
    headline = conj.makeProperName(headline) # Start with capital letter

    if formatter.background:
        background = formatter.background
    else:
        background = random.choice(
            Object.objects.filter(Q(image__isnull=False),
                                  ~Q(image=''),
                                  Q(image_position=1))).image

    if formatter.image:
        image = formatter.image
    else:
        image = random.choice(
            Object.objects.filter(Q(image__isnull=False),
                                  ~Q(image=''),
                                  Q(image_position=0))).image

    return {
        'headline': headline,
        'background': background,
        'image': image
    }


def index(request):
    data = {'news': []}
    for i in range(11):
        data['news'].append(getHeadline())
    return render(request, 'index.html', data)
