# Create your views here.

# import django module
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
# import conceptnet module
from conceptnet.models import *
import ConceptTagGenerator

def TagRecommendation(request):
    Result_list = ""
    Text = ""
    temp = get_template('aai_project.html')
    if request.POST.has_key('Text'):
        Text = request.POST['Text']
        if len(Text) != 0:
            Result_list = ConceptTagGenerator.parser(Text)
        else:
            print 'no any words in the text!'
    else:
        print 'no textarea in web-page!'

    html = temp.render(Context({'content':Text,'key_list':Result_list}))
    return HttpResponse(html)

