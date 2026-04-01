import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Vehicle, Driver, Trip


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['vehicle_count'] = Vehicle.objects.count()
    ctx['vehicle_car'] = Vehicle.objects.filter(vehicle_type='car').count()
    ctx['vehicle_van'] = Vehicle.objects.filter(vehicle_type='van').count()
    ctx['vehicle_truck'] = Vehicle.objects.filter(vehicle_type='truck').count()
    ctx['driver_count'] = Driver.objects.count()
    ctx['driver_active'] = Driver.objects.filter(status='active').count()
    ctx['driver_on_trip'] = Driver.objects.filter(status='on_trip').count()
    ctx['driver_off_duty'] = Driver.objects.filter(status='off_duty').count()
    ctx['driver_total_rating'] = Driver.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['trip_count'] = Trip.objects.count()
    ctx['trip_planned'] = Trip.objects.filter(status='planned').count()
    ctx['trip_in_progress'] = Trip.objects.filter(status='in_progress').count()
    ctx['trip_completed'] = Trip.objects.filter(status='completed').count()
    ctx['trip_total_distance_km'] = Trip.objects.aggregate(t=Sum('distance_km'))['t'] or 0
    ctx['recent'] = Vehicle.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def vehicle_list(request):
    qs = Vehicle.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(registration__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(vehicle_type=status_filter)
    return render(request, 'vehicle_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def vehicle_create(request):
    if request.method == 'POST':
        obj = Vehicle()
        obj.registration = request.POST.get('registration', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.make = request.POST.get('make', '')
        obj.model = request.POST.get('model', '')
        obj.year = request.POST.get('year') or 0
        obj.status = request.POST.get('status', '')
        obj.mileage = request.POST.get('mileage') or 0
        obj.fuel_type = request.POST.get('fuel_type', '')
        obj.save()
        return redirect('/vehicles/')
    return render(request, 'vehicle_form.html', {'editing': False})


@login_required
def vehicle_edit(request, pk):
    obj = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        obj.registration = request.POST.get('registration', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.make = request.POST.get('make', '')
        obj.model = request.POST.get('model', '')
        obj.year = request.POST.get('year') or 0
        obj.status = request.POST.get('status', '')
        obj.mileage = request.POST.get('mileage') or 0
        obj.fuel_type = request.POST.get('fuel_type', '')
        obj.save()
        return redirect('/vehicles/')
    return render(request, 'vehicle_form.html', {'record': obj, 'editing': True})


@login_required
def vehicle_delete(request, pk):
    obj = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/vehicles/')


@login_required
def driver_list(request):
    qs = Driver.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'driver_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def driver_create(request):
    if request.method == 'POST':
        obj = Driver()
        obj.name = request.POST.get('name', '')
        obj.license_number = request.POST.get('license_number', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.status = request.POST.get('status', '')
        obj.trips_completed = request.POST.get('trips_completed') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/drivers/')
    return render(request, 'driver_form.html', {'editing': False})


@login_required
def driver_edit(request, pk):
    obj = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.license_number = request.POST.get('license_number', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.status = request.POST.get('status', '')
        obj.trips_completed = request.POST.get('trips_completed') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/drivers/')
    return render(request, 'driver_form.html', {'record': obj, 'editing': True})


@login_required
def driver_delete(request, pk):
    obj = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/drivers/')


@login_required
def trip_list(request):
    qs = Trip.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(vehicle_reg__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'trip_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def trip_create(request):
    if request.method == 'POST':
        obj = Trip()
        obj.vehicle_reg = request.POST.get('vehicle_reg', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.distance_km = request.POST.get('distance_km') or 0
        obj.fuel_cost = request.POST.get('fuel_cost') or 0
        obj.start_date = request.POST.get('start_date') or None
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/trips/')
    return render(request, 'trip_form.html', {'editing': False})


@login_required
def trip_edit(request, pk):
    obj = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        obj.vehicle_reg = request.POST.get('vehicle_reg', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.origin = request.POST.get('origin', '')
        obj.destination = request.POST.get('destination', '')
        obj.distance_km = request.POST.get('distance_km') or 0
        obj.fuel_cost = request.POST.get('fuel_cost') or 0
        obj.start_date = request.POST.get('start_date') or None
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/trips/')
    return render(request, 'trip_form.html', {'record': obj, 'editing': True})


@login_required
def trip_delete(request, pk):
    obj = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/trips/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['vehicle_count'] = Vehicle.objects.count()
    data['driver_count'] = Driver.objects.count()
    data['trip_count'] = Trip.objects.count()
    return JsonResponse(data)
