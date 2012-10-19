from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings
from zero.company.models import *
from json import dumps
from time import mktime
from datetime import date, timedelta

def list(request):
    company = Company.objects.all().order_by('name')
    return render_to_response('company/list.html', { 'list': company }, context_instance=RequestContext(request))

def api_list(request):
    callback   = request.GET.get('callback', False)
    company = Company.objects.all().order_by('name')
    response_data = []
    for i in company:
        response_data.append({ 'symbol': i.symbol, 'name': i.name, 'exchange': i.exchange, 'sector': i.sector, 'location': i.location })
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def index_list(request):
    indexes = Index.objects.all()
    return render_to_response('company/indexes.html', { 'list': indexes }, context_instance=RequestContext(request))

def api_index_list(request):
    callback   = request.GET.get('callback', False)
    indexes = Index.objects.all()
    response_data = []
    for i in indexes:
        response_data.append({ 'name': i.name, 'slug': i.slug })
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def index(request, slug):
    index = Index.objects.get(slug=slug)
    company = IndexCompany.objects.filter(index=index)
    l = []
    for i in company:
        l.append(i.company)
    return render_to_response('company/list.html', { 'list': l, 'index': index }, context_instance=RequestContext(request))

def api_index(request, slug):
    callback   = request.GET.get('callback', False)
    index = Index.objects.get(slug=slug)
    company = IndexCompany.objects.filter(index=index)
    response_data = []
    for i in company:
        response_data.append({ 'symbol': i.company.symbol, 'name': i.company.name, 'exchange': i.company.exchange, 'sector': i.company.sector, 'location': i.company.location })
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def sector_list(request):
    sectors = Company.SECTOR_CHOICES
    return render_to_response('company/sectors.html', { 'list': sectors }, context_instance=RequestContext(request))

def api_sector_list(request):
    callback   = request.GET.get('callback', False)

    indexes = Index.objects.all()
    response_data = {}
    for i in Company.SECTOR_CHOICES:
        response_data[i[0]] = i[1]
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def sector(request, sector):
    company = Company.objects.filter(sector=sector)
    return render_to_response('company/sector.html', { 'list': company, 'sector': sector }, context_instance=RequestContext(request))

def api_sector(request, sector):
    callback   = request.GET.get('callback', False)
    company = Company.objects.filter(sector=sector)
    response_data = []
    for i in company:
        response_data.append({ 'symbol': i.symbol, 'name': i.name, 'exchange': i.exchange, 'sector': i.sector, 'location': i.location })
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def details(request, symbol):
    company = Company.objects.get(symbol=symbol)
    return render_to_response('company/details.html', { 'company': company }, context_instance=RequestContext(request))

def api_ohlc(request, symbol, days):
    callback   = request.GET.get('callback', False)
    company = Company.objects.get(symbol=symbol)
    response_data = company.ohlc(days)
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")


def movers_today(request):
    today = datetime.date.today()
    return movers(request, today.year, today.month, today.day)

def movers(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)
    dates = []
    oneday = datetime.timedelta(1)

    for i in range(-5,5):
        dates.append(date + (oneday * i))
    dates.reverse()

    prices = Price.objects.filter(date=date)
    p = []
    for i in prices:
        p.append({ 'company': i.company, 'opened': i.opened, 'high': i.high, 'low': i.low, 'closed': i.closed, 'change': round(i.closed - i.opened, 2), 'change_pct': round(((i.closed - i.opened)/i.opened) * 100,2) })
    return render_to_response('company/movers.html', { 'date': date, 'prices': p, 'dates': dates }, context_instance=RequestContext(request))

