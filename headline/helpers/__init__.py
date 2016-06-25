from django.template.defaultfilters import slugify
from headline.models import Category, Object, Headline, News
from django.db.models import Q
from conj import conj
import random

class HeadlineFormatter(object):
    """
    String formatter for headline template
    """

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
            category = Category.objects.filter(Q(is_active=True),
                                               Q(name=params[0])).first()
            objects = Object.objects.filter(Q(is_active=True),
                                            Q(category=category))

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


class NewsHelper(object):
    """
    Helper class for news and headlines
    """

    def getClientIP(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def makeSlug(self, title):
        trCharMap = {
            ord('ı'): 'i', ord('ğ'): 'g', ord('ü'): 'u',
            ord('ç'): 'c', ord('ş'): 's', ord('ö'): 'o'
        }
        title = title.lower()
        title = title.translate(trCharMap)
        return slugify(title)

    def saveHeadline(self, request, title, background, image):
        """
        Saves generated headline to News
        """
        slug = self.makeSlug(title)
        ip_address = self.getClientIP(request)

        if News.objects.filter(slug=slug).count() == 0:
            News(title=title, slug=slug, background=background, image=image,
                 view_count=0, ip_address=ip_address, is_active=True).save()

    def getHeadline(self, request):
        """
        Generates a random headline
        """
        headlines = Headline.objects.filter(is_active=True)
        formatter = HeadlineFormatter()
        headline = random.choice(headlines).text.format(random=formatter)
        headline = conj.makeProperName(headline) # Start with capital letter

        if formatter.background:
            background = formatter.background
        else:
            background = random.choice(
                Object.objects.filter(Q(is_active=True),
                                      Q(image__isnull=False),
                                      ~Q(image=''),
                                      Q(image_position=1))).image

        if formatter.image:
            image = formatter.image
        else:
            image = random.choice(
                Object.objects.filter(Q(is_active=True),
                                      Q(image__isnull=False),
                                      ~Q(image=''),
                                      Q(image_position=0))).image

        self.saveHeadline(request, headline, background, image)

        return {
            'headline': headline,
            'background': background,
            'image': image
        }
