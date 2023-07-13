from django.db import models
import bcrypt
import re

class CarsManager(models.Manager):
    errors = {}
    EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    def presence_validator(self, postData):
        self.errors = {}
        for key, value in postData.items():
            if len(value) < 1:
                self.errors['required'] = f"All fields are required!"
                break
        return self.errors

    def regi_validator(self, postData):
        self.errors = {}
        for key, value in postData.items():
            if len(value) < 1:
                self.errors['required'] = f"All fields are required!"
                break
        if len(postData['first_name']) < 3:
            self.set_error('first_name', 'First name must be at least 3 characters')
        if len(postData['last_name']) < 3:
            self.set_error('last_name', 'Last name must be at least 3 characters')
        if not self.EMAIL_REGEX.match(postData['email']):
            self.set_error('email', 'Invalid email address')
        if len(postData['password']) < 8:
            self.set_error('password', 'Password must be at least 8 characters')
        if postData['password'] != postData['conf_password']:
            self.set_error('conf_password', 'Passwords do not match')
        return self.errors

    def set_error(self, key, value):
        self.errors[key] = value

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarsManager()

class Car(models.Model):
    price=models.CharField(max_length=30)
    model = models.CharField(max_length=255)
    make=models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="cars", on_delete = models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarsManager()

def register(request):
    user = request.POST
    first_name = user['first_name']
    last_name = user['last_name']
    email = user['email']
    password = user['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)

def login(request):
    post = request.POST
    user = User.objects.filter(email=post['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(post['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return True

def validate_regi(request):
    return User.objects.regi_validator(request.POST)

def validate_presence(request):
    return Car.objects.presence_validator(request.POST)

def get_user_by_id(id):
    return User.objects.get(id=id)

def get_user_cars(id):
    user = get_user_by_id(id)
    return user.cars.all()

def add_car(request, user):
    car = request.POST
    price = car['price']
    model = car['model']
    make= car['make']
    year = car['year']
    description=car['description']
    Car.objects.create(price=price,model=model,make=make, year=year, created_by = user,description=description)

def get_car_by_id(id):
    return Car.objects.get(id=id)

def get_cars_all():
    return Car.objects.all()

def is_car_added_by_id(car_id, user_id):
    car = get_car_by_id(car_id)
    user = get_user_by_id(user_id)
    for user in car.added_by.all():
        if user.id == user_id:
            return True
        else: return False
    

def delete_car(car_id):
    car = get_car_by_id(car_id)
    car.delete()

def update_car(request):
    car = request.POST
    price = car['price']
    model = car['model']
    make= car['make']
    year = car['year']
    description=car['description']
    id = car['car_id']
    old_car = get_car_by_id(id)
    old_car.price = price
    old_car.model = model
    old_car.make = make
    old_car.year = year
    old_car.description = description
    old_car.save()