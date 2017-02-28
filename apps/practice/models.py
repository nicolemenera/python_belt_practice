from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime
NAME_REGEX = re.compile(r'[a-zA-Z]\D{2,}$')

# Create your models here.

class UserManager(models.Manager):
  def register(self, data):
    status = True
    errorList = []
    if not NAME_REGEX.match(data['name']):
      status = False
      errorList.append("Name may only contain letters and be greater than two characters in length!")
    if len(data['username']) < 2:
      status = False
      errorList.append("Username must be greater than two characters in length")
    if len(data['password']) < 8:
      status = False
      errorList.append("Password must be greater than eight characters in length")
    if data['password'] != data['confirm_pw']:
      status = False
      errorList.append("Passwords must match!") 
    if status == False:
      return {'error':errorList}
    if status == True:
      password = data['password']
      hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
      User.objects.create(name=data['name'], username=data['username'], password=hashed)
      return {}
  
  def login(self, data):
    status = True
    errorList = []
    
    user = User.objects.filter(username=data['username'])
    if len(data['username']) < 2:
      status == False
      errorList.append("Username must be provided, dumbass.")
    if len(user) < 1:
      status == False
      errorList.append("Username does not exist, please register!")
    if status == False:
      return {'error' : errorList}
    else: 
      if bcrypt.hashpw(data['password'].encode(), user[0].password.encode()) == user[0].password:
        return {}
      else:
        errorList.append("Password does not match record")
        return {'error' : errorList}

class User(models.Model):
  name = models.CharField(max_length=255)
  username = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  
class TripManager(models.Manager):
  def settrip(self, data, user):
    status = True
    errorList = []
    today = str(datetime.datetime.today()).split()[0]
    
    if len(data['destination']) < 1:
      status = False
      errorList.append("A destination must be provided!")
    if len(data['description']) < 1:
      status = False
      errorList.append("A description must be provided!")
    if len(data['date_from']) < 1:
      status = False
      errorList.append("Date From must be filled out!")
    if len(data['date_to']) < 1:
      status = False
      errorList.append("Date To must be filled out!")
    elif data['date_from'] < today:
      status = False
      errorList.append("This isn't 'Back to the Future', please have your trip start on a day later than today.")
    elif data['date_from'] == today:
      status = False
      errorList.append("Travel From Date can't start today. It just can't. Please select a date sometime AFTER today.")
    if data['date_from'] > data['date_to']:
      status = False
      errorList.append("Travel From Date must be earlier than Travel To Date!")
    if status == False:
      return {'error' : errorList}
    else:
      new_trip = Trip.objects.create(creator=user, destination=data['destination'], description=data['description'], start=data['date_from'], end=data['date_to'])
      Trip.objects.join(new_trip.id, user.id)
      return {}
      
  def join(self, trip, user):
    this_trip = Trip.objects.get(id=trip)
    this_user = User.objects.get(id=user)
    this_trip.join.add(this_user)
    return {}
    

  
class Trip(models.Model):
  creator = models.ForeignKey(User)
  destination = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  start = models.DateField()
  end = models.DateField()
  join = models.ManyToManyField(User, related_name = "userjoin")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = TripManager()