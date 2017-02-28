from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages
from datetime import datetime
# Create your views here.

def index(request):
  return render(request, 'practice/index.html')
  
def register(request):
  if request.method=='GET':
    return redirect('/')
  user = User.objects.register(request.POST)
  if 'error' in user:
    error = user['error']
    for msg in error:
      messages.error(request, msg)
      return redirect('/')
  else:
    user = User.objects.filter(username = request.POST['username'])
    request.session['userid'] = user[0].id
    messages.success(request, "Successful Registration, you are now logged in!")
  return redirect('/success')
  
def login(request):
  if request.method=='GET':
    return redirect('/')
  user = User.objects.login(request.POST)
  if 'error' in user:
    error = user['error']
    for msg in error:
      messages.error(request, msg)
    return redirect('/')
  else:
    user = User.objects.filter(username = request.POST['username'])
    request.session['userid'] = user[0].id
  return redirect('/success')
  
def success(request):
  if 'userid' not in request.session:
    return redirect('/')
  context = {'loggeduser':User.objects.get(id=request.session['userid']), 'trips': Trip.objects.filter(join__id=request.session['userid']), 'othertrips': Trip.objects.exclude(join__id=request.session['userid'])}
  return render(request, 'practice/success.html', context)

def join(request, trip):
  if request.method == "GET":
    return redirect('/')
  join = Trip.objects.join(trip, request.session['userid'])
  return redirect('/success')
  
def logout(request):
  if request.method == "GET":
    return redirect('/')
  del request.session['userid']
  return redirect('/')

def addplan(request):
  print 'helloooooooooooo'
  return render(request, 'practice/addplan.html')
  
def settrip(request):
  if request.method=='GET':
    return redirect('/')
  trip = Trip.objects.settrip(request.POST, User.objects.get(id=request.session['userid']))
  if 'error' in trip:
    error = trip['error']
    for msg in error:
      messages.error(request, msg)
    return redirect('/addplan')
  else:
    messages.success(request, "Trip Added! Hopefully no weirdos try to tag along....!")
  return redirect('/success')
  
def description(request, tripid):
  if request.method=='GET':
    return redirect('/')
  trip = Trip.objects.get(id=tripid)
  joiners = User.objects.filter(userjoin__id=tripid).exclude(id = trip.creator.id)
  print "MADE IT!!!!!!!!!!!!!!", joiners
  context = { 'trip' : trip, 'joiners' : joiners }
  return render(request, 'practice/description.html', context)
  
