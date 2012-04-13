from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings
from zero.company.models import *
from json import dumps
from time import mktime
from datetime import date

def list(request):
    company = Company.objects.all().order_by('name')
    return render_to_response('company/list.html', { 'list': company }, context_instance=RequestContext(request))

def details(request, symbol):
    company = Company.objects.get(symbol=symbol)
    return render_to_response('company/details.html', { 'company': company }, context_instance=RequestContext(request))

def ohlc(request, symbol, days):
    callback   = request.GET.get('callback', False)
    company = Company.objects.get(symbol=symbol)
    response_data = company.ohlc(days)
    response_str = dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")


def movers(request, year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)
    dates = []

    for i in range(-5,5):
        dates.append(datetime.date(year, month, day - i))
    dates.reverse()

    prices = Price.objects.filter(date=date)
    p = []
    for i in prices:
        p.append({ 'company': i.company, 'opened': i.opened, 'high': i.high, 'low': i.low, 'closed': i.closed, 'change': round(i.closed - i.opened, 2), 'change_pct': round(((i.closed - i.opened)/i.opened) * 100,2) })
    return render_to_response('company/movers.html', { 'date': date, 'prices': p, 'dates': dates }, context_instance=RequestContext(request))

