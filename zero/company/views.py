from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings

from zero.company.models import *
import urllib2
import json
import time
import random
import datetime

random.seed()

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="

    def get(self,symbol,exchange):
        exchange = ''
        url = self.prefix+"%s:%s" % (symbol,exchange)
        u = urllib2.urlopen(url)
        print url
        content = u.read()
        obj = json.loads(content[3:])
        return obj[0]

def list(request):
    company = Company.objects.all().order_by('name')
    return render_to_response('company/list.html', { 'list': company }, context_instance=RequestContext(request))

def details(request, symbol):
    company = Company.objects.get(symbol=symbol)
    return render_to_response('company/details.html', { 'company': company }, context_instance=RequestContext(request))

def stats(request, symbol, days):
    callback   = request.GET.get('callback', False)
    company = Company.objects.get(symbol=symbol)
    response_data = company.stats(days)
    response_str = json.dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="application/javascript")

def ohlc(request, symbol, days):
    callback   = request.GET.get('callback', False)
    company = Company.objects.get(symbol=symbol)
    response_data = company.ohlc(days)
    response_str = json.dumps(response_data);
    if callback:
        response_str = '%s(%s)' % (callback, response_str)
    return HttpResponse(response_str, mimetype="text/javascript")

def importer(request):
    in_file = open('sp500.csv', 'r')
    g = GoogleFinanceAPI();
    i = 0
    arr = []
    fail = []

    for line in in_file:
        error = False
        line = line.strip().replace('"','').split(',');
        o = { 'name': line[1], 'symbol': line[0], }


        company = Company.objects.filter(symbol=o['symbol'])
        if not len(company):
            try:
                n = random.random()
                time.sleep(n)
                r = g.get(o['symbol'])
            except:
                error = True
                fail.append(o)
                #return render_to_response('company/list.html', { 'list': o }, context_instance=RequestContext(request))
            if not error:
                o['exchange'] = r['e']
                Company.objects.create(name=o['name'], symbol=o['symbol'], exchange=o['exchange'])
                arr.append(o)
        i = i + 1
        if i == 500:
            break

    return render_to_response('company/list.html', { 'list': arr, 'fail': fail }, context_instance=RequestContext(request))

def historical(request):
    in_file = open('sp500_raw.csv', 'r')

    foo = []
    for line in in_file:
        error = False
        line = line.strip().split('|');
        o = { 'name': line[1], 'symbol': line[0], 'sector': line[2], 'location': line[3] }
        if o['sector'] == 'Telecommunications Services':
            o['sector'] = 'ts'
        elif o['sector'] == 'Industrials':
            o['sector'] = 'in'
        elif o['sector'] == 'Consumer Discretionary':
            o['sector'] = 'cd'
        elif o['sector'] == 'Utilities':
            o['sector'] = 'ut'
        elif o['sector'] == 'Consumer Staples':
            o['sector'] = 'cs'
        elif o['sector'] == 'Health Care':
            o['sector'] = 'hc'
        elif o['sector'] == 'Financials':
            o['sector'] = 'fi'
        elif o['sector'] == 'Energy':
            o['sector'] = 'en'
        elif o['sector'] == 'Information Technology':
            o['sector'] = 'it'
        company = Company.objects.get(symbol=o['symbol'])
        company.location = o['location']
        company.sector = o['sector']
        company.save();
        foo.append(company);

    return render_to_response('company/historical.html', { 'list': foo }, context_instance=RequestContext(request))



    companies = Company.objects.all().order_by('name')
    i = 0
    foo = []
    for company in companies:
        n = random.random()
        time.sleep(n)
        url = "http://ichart.finance.yahoo.com/table.csv?s=%s&d=2&e=28&f=2012&g=d&a=0&b=2&c=1962&ignore=.csv" % company.symbol
        req = urllib2.Request(url=url)
        f = urllib2.urlopen(req)
        res = f.read().split('\n')
        res.reverse()
        res.pop()
        res.reverse()
        for line in res:
            line2 = line.strip().split(',')
            if (len(line2) > 1):
                date = line2[0].strip().split('-')
                o = {
                    'date':         datetime.date(int(date[0]), int(date[1]), int(date[2])),
                    'opened':       line2[1],
                    'high':         line2[2],
                    'low':          line2[3],
                    'closed':       line2[4],
                    'volume':       line2[5],
                    'adj_closed':   line2[6],
                }
                try:
                    price = Price.objects.get(company=company, date=o['date'])
                except:
                    price = Price(
                        company=company,
                        category='d',
                        date=o['date'],
                        opened=o['opened'],
                        high=o['high'],
                        low=o['low'],
                        closed=o['closed'],
                        volume=o['volume'],
                        adj_closed=o['adj_closed'],
                    )
                    price.save()
                foo.append(price)
        i = i + 1
        if i == 1:
            break

    return render_to_response('company/historical.html', { 'list': foo }, context_instance=RequestContext(request))
