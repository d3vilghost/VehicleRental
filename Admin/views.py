from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from Admin.models import UserProfile, VehicleType, Vehicle, RentVehicle
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def ChoiceUser(request):
    return render(request,'choice-user.html')


def Search(request):
    if request.method == "POST":
        search = request.POST.get('search')
        print(search)
        v = Vehicle.objects.filter(vehiclenumber__icontains=search)
        page = request.GET.get('page', 1)

        paginator = Paginator(v, 10)
        try:
            v = paginator.page(page)
        except PageNotAnInteger:
            v = paginator.page(1)
        except EmptyPage:
            v = paginator.page(paginator.num_pages)
        return render(request, 'all-vehicles.html', {'vehicle':v})



def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(user=request.user)
    user_booked_vehicle = RentVehicle.objects.filter(user=u).count()
    user_paid_vehicle = RentVehicle.objects.filter(user=u, paid_status="Paid").count()
    user_unpaid_vehicle = RentVehicle.objects.filter(user=u, paid_status="UnPaid").count()

    owner_total_vehicle = Vehicle.objects.filter(user=u).count()
    owners_total_completed_booking = RentVehicle.objects.filter(user=u, status="Completed Rent").count()
    owners_total_onrent_booking = RentVehicle.objects.filter(user=u, status="On Rent").count()

    total_public_user = UserProfile.objects.filter(userType="Public").count()
    total_owner_user = UserProfile.objects.filter(userType="Owner").count()
    total_admin_user = UserProfile.objects.filter(userType="Admin").count()

    total_booking = RentVehicle.objects.all().count()
    completed_booking = RentVehicle.objects.filter(status="Completed Rent").count()
    onrent_booking = RentVehicle.objects.filter(status="On Rent").count()
    approved_booking = RentVehicle.objects.filter(status="Approved").count()
    rejected_booking = RentVehicle.objects.filter(status="Rejected").count()
    total_pending_booking = RentVehicle.objects.filter(status="Pending").count()
    unpaid_booking = RentVehicle.objects.filter(paid_status="UnPaid", status="Completed Rent").count()
    paid_booking = RentVehicle.objects.filter(paid_status="Paid", status="Completed Rent").count()

    total_earned = RentVehicle.objects.filter(paid_status="Paid", status="Completed Rent").aggregate(Sum('total_price'))['total_price__sum']

    if total_earned == None:
        total_earned = 0

    Dict = {
        'booked_vehicle':user_booked_vehicle,
        'user_paid_vehicle':user_paid_vehicle,
        'user_unpaid_vehicle':user_unpaid_vehicle,

        'owner_total_vehicle':owner_total_vehicle,
        'owners_total_completed_booking':owners_total_completed_booking,
        'owners_total_onrent_booking':owners_total_onrent_booking,

        'total_booking':total_booking,
        'completed_booking':completed_booking,
        'onrent_booking':onrent_booking,
        'approved_booking':approved_booking,
        'rejected_booking':rejected_booking,
        'total_pending_booking':total_pending_booking,
        'unpaid_booking':unpaid_booking,
        'paid_booking':paid_booking,

        'total_public_user':total_public_user,
        'total_owner_user':total_owner_user,
        'total_admin_user':total_admin_user,

        'total_earned':total_earned
    }
    return render(request,"dashboard.html", Dict)


def Profile(request):
    return render(request,"profile.html")

def UserDetails(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)
    return render(request,"userprofile.html", {'details':u})


def EditSingleUser(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        pic = request.FILES.get('pic')
        
        if len(contact) != 10:
            msg = 'Phone number should be 10 digit!!'
            return render(request, 'edit-profile.html', {'msg':msg})
        
        u.user.first_name = first_name
        u.user.last_name = last_name
        u.user.email = email
        

        u.contact_No = contact
        u.address = address
        u.dob = dob
        if pic:
            u.profilePicture = pic
        u.user.save()
        u.save()
        return redirect('users')
    return render(request,"edit-user.html", {'details':u})



def DeleteUser(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(id=id)
    u.delete()
    return redirect('users')



def EditProfile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        pic = request.FILES.get('pic')
        
        if len(contact) != 10:
            msg = 'Phone number should be 10 digit!!'
            return render(request, 'edit-profile.html', {'msg':msg})
        
        u = UserProfile.objects.get(user=request.user)

        u.user.first_name = first_name
        u.user.last_name = last_name
        u.user.email = email
        

        u.contact_No = contact
        u.address = address
        u.dob = dob
        if pic:
            u.profilePicture = pic
        u.user.save()
        u.save()
        return redirect('profile')

    return render(request, 'edit-profile.html')


def ChangePassword(request):
    msg =''
    if request.method == "POST":
        oldpass = request.POST.get('oldpass')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1!=password2:
            msg='Password should be same.'
            return render(request,'changepasswordadmin.html', {'msg':msg})
        try:
            user = User.objects.get(username=request.user.username)
        except:
            msg='Invalid Username.'
            return render(request, 'changepasswordadmin.html', {'msg':msg})
        
        t = user.check_password(oldpass)
        if t:
            user.set_password(password1)
            user.save()
            data=authenticate(username=request.user.username, password=password1)
            if data !=None:
                login(request,data)
                return redirect('profile')
        msg='Old password is incorrect.'
    return render(request,"changepasswordadmin.html", {'msg':msg})


def AllUsers(request):
    alluser = UserProfile.objects.all().exclude(user=request.user)
    return render(request, 'users.html', {'users':alluser})

def AllOwner(request):
    allowner = UserProfile.objects.filter(userType="Owner")
    return render(request, 'users.html', {'users':allowner})

def AllPublic(request):
    allpublic = UserProfile.objects.filter(userType="Public")
    return render(request, 'users.html', {'users':allpublic})


def TotalVehicle(request):
    u = UserProfile.objects.get(user=request.user)
    if u.userType == "Owner":
        v = Vehicle.objects.filter(
            user = u
        )
    else:
        v = Vehicle.objects.all().order_by('-id')
    if request.method == "POST":
        search = request.POST.get('search')
        
        v = Vehicle.objects.filter(vehiclenumber__contains=search)
    page = request.GET.get('page', 1)

    paginator = Paginator(v, 10)
    try:
        v = paginator.page(page)
    except PageNotAnInteger:
        v = paginator.page(1)
    except EmptyPage:
        v = paginator.page(paginator.num_pages)
    return render(request, 'all-vehicles.html', {'vehicle':v})


def AddVehicleType(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        name=request.POST.get('name').upper()
        try:
            VehicleType.objects.get(name=name)
        except:
            VehicleType.objects.create(user=UserProfile.objects.get(user=request.user), name=name)
            return redirect('add-vehicle')
        msg = 'Vehicle Type Already Exist.'
        return render(request, 'add-vehicle-type.html', {'msg':msg})
        
    return render(request, 'add-vehicle-type.html')


def AddVehicle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    vehicleType = VehicleType.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        vehicle_number = request.POST.get('vehicle_number')
        image = request.FILES.get('image')
        price=request.POST.get('price')
        price=int(price)
        v = request.POST.get("vehicle_type")

        vt = VehicleType.objects.get(id=int(v))
        Vehicle.objects.create(
            user=UserProfile.objects.get(user=request.user), 
            vehicle_type=vt,
            vehiclenumber=vehicle_number,
            name = name,
            image = image,
            price_per_day=price
        )
        return redirect('total-vehicle')
    return render(request, 'add-vehicle.html',{'types':vehicleType})


def EditVehicle(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = Vehicle.objects.get(id=id)
    vt = VehicleType.objects.all().exclude(id=v.vehicle_type.id)
    if request.method == "POST":
        vehicle_type = request.POST.get('vehicle_type')

        new_vt = VehicleType.objects.get(id=int(vehicle_type))
        name = request.POST.get('name')
        vehicle_number = request.POST.get('vehiclenumber')
        status = request.POST.get('status')
        image = request.FILES.get('image')
        if image:
            v.image = image
        
        if status:
            v.status = status
        
        v.vehicle_type = new_vt
        v.name=name
        v.vehiclenumber = vehicle_number
        v.save()
        return redirect('total-vehicle')
    return render(request, 'edit-vehicle.html', {'details':v, 'v_type': vt})

def DeleteVehicle(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = Vehicle.objects.get(id=id)
    v.delete()
    return redirect('total-vehicle')


def AvailableVehicle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    v = Vehicle.objects.filter(status="Available")
    if request.method == "POST":
        search = request.POST.get('search')
        
        v = Vehicle.objects.filter(Q(vehicle_type__name__icontains=search) | Q(name__icontains=search))
    page = request.GET.get('page', 1)

    paginator = Paginator(v, 10)
    try:
        v = paginator.page(page)
    except PageNotAnInteger:
        v = paginator.page(1)
    except EmptyPage:
        v = paginator.page(paginator.num_pages)
    return render(request, 'available-vehicle.html', {'vehicle':v})


def BookVehicle(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = Vehicle.objects.get(id=id)
    if request.method == "POST":
        days = request.POST.get('days')
        aadhar = request.POST.get('aadhar')
        id_proof = request.FILES.get('id_proof')
        book_from = request.POST.get('book_from')
        book_to = request.POST.get('book_to')

        RentVehicle.objects.create(
            user = UserProfile.objects.get(user=request.user),
            vehicle = v,
            aadhar_number = aadhar,
            id_proof = id_proof,
            book_day = days,
            book_from = book_from,
            book_to = book_to,
            total_price = int(days)*int(v.price_per_day)
        )

        body = f'Hello {request.user.first_name},\nYou have booked {v.name} with number {v.vehiclenumber} for {days} days.\n\nYour Total price is {int(days)*int(v.price_per_day)} Rs/-. Please pay in cash. \n\nThanks, \nVehicle Rental Support'
        subject = 'Vehicle Rental Services'
        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]
        
        send_mail(subject, body, from_email, to_email, fail_silently=True)
        return redirect('track-vehicle')
    return render(request, 'bookvehicle.html', {'details':v})


def EditBooking(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = RentVehicle.objects.get(id=id)
    if request.method == "POST":
        days = request.POST.get('days')
        aadhar = request.POST.get('aadhar')
        status = request.POST.get('status')
        paid_status = request.POST.get('paid_status')
        book_from = request.POST.get('book_from')
        book_to = request.POST.get('book_to')
        id_proof = request.FILES.get('id_proof')
        
        if id_proof:
            v.id_proof=id_proof
        
        v.book_day = days
        v.aadhar_number = aadhar
        v.book_from = book_from
        v.book_to = book_to
        
        if status == "Completed Rent":
            if paid_status == "UnPaid":
                msg = "Please Pay/Change paid status before Completing the status."
                return render(request, 'edit-booking.html', {'details':v, 'msg':msg})
        if status:
            v.status = status
        if paid_status:
            v.paid_status = paid_status
        v.save()
        if status == "On Rent":
            v.vehicle.status = "Not Available"
            v.vehicle.save()
        
        if status == "Pending":
            pass
        elif status == None:
            pass
        else:
            body = f'Hello {v.user.user.first_name},\nYour booked vehicle status with name {v.vehicle.name} having number {v.vehicle.vehiclenumber} has been changed to {status}.\n\n. \n\nThanks, \nVehicle Rental Support'
            subject = 'Vehicle Rental Services'
            from_email = settings.EMAIL_HOST_USER
            to_email = [v.user.user.email]
            
            send_mail(subject, body, from_email, to_email, fail_silently=True)
        return redirect('track-vehicle')
    return render(request, 'edit-booking.html', {'details':v})


 

def TrackVehicle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(user=request.user)
    if u.userType == "Admin":
        v = RentVehicle.objects.all().exclude(status="Completed Rent").order_by('-id')
    elif u.userType == "Owner":
        v = RentVehicle.objects.filter(vehicle__user=u).order_by('-id')
    else:
        v = RentVehicle.objects.filter(user=u).order_by('-id')
    if request.method == "POST":
        search = request.POST.get('search')
        
        v = RentVehicle.objects.filter(booking_id__icontains=search)
    page = request.GET.get('page', 1)

    paginator = Paginator(v, 10)
    try:
        v = paginator.page(page)
    except PageNotAnInteger:
        v = paginator.page(1)
    except EmptyPage:
        v = paginator.page(paginator.num_pages)
    return render(request, 'track.html', {'vehicle':v})


def TrackCompletedVehicle(request):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(user=request.user)
    
    v = RentVehicle.objects.filter(status="Completed Rent").order_by('-id')
    
    if request.method == "POST":
        search = request.POST.get('search')
        
        v = RentVehicle.objects.filter(status="Completed Rent", booking_id__icontains=search)
    page = request.GET.get('page', 1)

    paginator = Paginator(v, 10)
    try:
        v = paginator.page(page)
    except PageNotAnInteger:
        v = paginator.page(1)
    except EmptyPage:
        v = paginator.page(paginator.num_pages)
    return render(request, 'completed-rent.html', {'vehicle':v})


def UnpaidCompletedRent(request):
    if not request.user.is_authenticated:
        return redirect('login')
    u = UserProfile.objects.get(user=request.user)
    
    v = RentVehicle.objects.filter(paid_status="UnPaid", status="Completed Rent").order_by('-id')
    
    if request.method == "POST":
        search = request.POST.get('search')
        
        v = RentVehicle.objects.filter(paid_status="UnPaid", status="Completed Rent", booking_id__icontains=search)
    page = request.GET.get('page', 1)

    paginator = Paginator(v, 10)
    try:
        v = paginator.page(page)
    except PageNotAnInteger:
        v = paginator.page(1)
    except EmptyPage:
        v = paginator.page(paginator.num_pages)
    return render(request, 'unpaid-customer.html', {'vehicle':v})


def Track(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = RentVehicle.objects.get(id=id)
    return render(request, 'tracking-details.html', {'details':v})


def DeleteBooking(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    v = RentVehicle.objects.get(id=id)
    v.delete()
    return redirect('dashboard')