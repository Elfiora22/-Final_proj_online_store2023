from django.http.response import HttpResponse


def index(request):
    return HttpResponse('Welcome!')


#def orders_page(request):
    #return HttpResponse('Orders are here')



