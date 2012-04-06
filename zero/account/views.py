from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings
from zero.account.models import Account, Asset, Transaction
from zero.company.models import Company
from datetime import datetime
import json

def details(request):
    assets = Asset.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render_to_response('account/details.html', { 'assets': assets, 'transactions': transactions }, context_instance=RequestContext(request))

def transaction(request):
    symbol   = request.GET.get('symbol', False)
    quantity = int(request.GET.get('quantity', 0))
    category = request.GET.get('category', False)
    company = Company.objects.get(symbol=symbol)
    if category == 'buy':
        status = request.user.account.buy(company, quantity)
    elif category == 'sell':
        status = request.user.account.sell(company, quantity)
    return HttpResponse(json.dumps({ 'status': status }), mimetype='application/json')
