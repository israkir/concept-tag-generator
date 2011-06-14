# Create your views here.
from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse
import ConceptTagGenerator
#import tag

def mainPage(request):
    Key_title = ""
    temp = get_template('main.html')
    print 'main page'
    html = temp.render(Context())
    return HttpResponse(html)

def articleInput(request):
    Key_title = ""
    temp = get_template('article_input.html')
    print 'article input'
    html1 = temp.render(Context())
    return HttpResponse(html1)

def keywordsOutput(request):
    temp = get_template('keywords_output.html')
    print 'keywords output'
    html1 = temp.render(Context())
    return HttpResponse(html1)

def keywordsGenerator(request):
    Result_list = ""
    Text = ""
    Key_title = "Keywords: no recommendation"
    if request.POST.has_key('Text'):
        Text = request.POST['Text']
        if len(Text) != 0:
            Result_list = ConceptTagGenerator.parser(Text)
            #Result_list = tag.parser(Text)
            Key_title = "Keywords: "
        else:
            print 'no any words in the text!'
    else:
        print 'no textarea in web-page!'

    temp = get_template('keywords_output.html')
    html = temp.render(Context({'key_title':Key_title, 'key_list':Result_list}))
    print 'keywords generator'
    return HttpResponse(html)

def keywordsFeedback(request):
    Key_title = "Keywords: "
    input_key_list = []
    output_key_list = []

    input_key_list = request.POST.getlist('checkbox')
    for key in input_key_list:
        print key
        output_key_list.append(key)

    temp = get_template('keywords_output.html')
    print 'keywords feedback'
    html = temp.render(Context({'key_title':Key_title, 'key_list':output_key_list}))
    return HttpResponse(html)
