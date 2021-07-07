from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from Admin.models import UserProfile, OTP
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def Home(request):
    return render(request, 'index.html')


def About(request):
    return render(request, 'about.html')

def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        body = f'Hello {name},\nOur team will get back to you within 48 hours. \nThanks\nVehicle Rental Team'
        subject = 'Vehicle Rental Services'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        
        send_mail(subject, body, from_email, to_email, fail_silently=True)

        body = f'Hello Admin,\nSome one with name {name} having email {email} is trying to contact you\nMessage: {message}'
        subject = 'Vehicle Rental Services'
        from_email = settings.EMAIL_HOST_USER
        to_email = ["rkbhol1101@gmail.com"]
        
        send_mail(subject, body, from_email, to_email, fail_silently=True)
    return render(request, 'contact.html')


def Signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'auth-register.html',{'msg':msg})
        
        if len(contact)!=10:
            msg = 'Phone Number Should be equal to 10 digit'
            return render(request,'auth-register.html',{'msg':msg})

        try:
            user=User.objects.create_user(username=username,email=email,password=pass1,first_name=first_name,last_name=last_name)
        except:
            msg='Usename already exist.'
            return render(request,'auth-register.html',{'msg':msg})
        UserProfile.objects.create(user=user,profilePicture=profile_pic,contact_No=contact, address=address, dob=dob)
        return redirect('login')
    return render(request, 'auth-register.html')


def OwnerSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'owner-signup.html',{'msg':msg})
        
        if len(contact)!=10:
            msg = 'Phone Number Should be equal to 10 digit'
            return render(request,'owner-signup.html',{'msg':msg})

        try:
            user=User.objects.create_user(username=username,email=email,password=pass1,first_name=first_name,last_name=last_name)
        except:
            msg='Usename already exist.'
            return render(request,'owner-signup.html',{'msg':msg})
        UserProfile.objects.create(user=user,profilePicture=profile_pic,contact_No=contact, address=address, dob=dob, userType="Owner")
        return redirect('login')
    return render(request, 'owner-signup.html')



def AdminSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('pic')
        
        if pass1!=pass2:
            msg='Password should be same.'
            return render(request,'admin-signup.html',{'msg':msg})
        
        if len(contact)!=10:
            msg = 'Phone Number Should be equal to 10 digit'
            return render(request,'admin-signup.html',{'msg':msg})

        try:
            user=User.objects.create_user(username=username,email=email,password=pass1,first_name=first_name,last_name=last_name)
        except:
            msg='Usename already exist.'
            return render(request,'admin-signup.html',{'msg':msg})
        UserProfile.objects.create(user=user,profilePicture=profile_pic,contact_No=contact, address=address, dob=dob, userType="Admin")
        return redirect('login')
    return render(request, 'admin-signup.html')


def Login(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
        
    msg=''
    if request.method=='POST':
        uname=request.POST['username']
        pwd=request.POST['password']
        data=authenticate(username=uname,password=pwd)
        if data !=None:
            login(request,data)
            return redirect('profile')
        msg='Incorrect Username or Password'
    return render(request, 'auth-login.html', {'msg':msg})


def Logout(request):
    logout(request)
    return render(request,'index.html')    


def SendEmailForForgotPassword(request):
    if request.method == "POST":
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except:
            msg='Invalid Username.'
            return render(request, 'ForgotPassEmail.html', {'msg':msg})
        
        otp = OTP.objects.create(user=user)
        
        body = f'Forgot Password?? This is your OTP to get your password reset {otp.otp}'
        subject = 'Forgot Password for Vehicle Project Services Account'
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]
        
        send_mail(subject, body, from_email, to_email, fail_silently=True)
        return redirect('forgot-password')
    return render(request, 'ForgotPassEmail.html')


def ForgotPassword(request):
    msg =''
    if request.method == "POST":
        username = request.POST.get('username')
        user_otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1!=password2:
            msg='Password should be same.'
            return render(request,'auth-forgot-password.html', {'msg':msg})
        try:
            user = User.objects.get(username=username)
        except:
            msg='Invalid Username.'
            return render(request, 'auth-forgot-password.html', {'msg':msg})
        
        otp = OTP.objects.filter(user=user).order_by('-created_at').first()
        if str(otp.otp) == user_otp:
            user.set_password(password1)
            user.save()
            return redirect('login')
        msg = 'Please Enter Correct OTP'
    return render(request, 'auth-forgot-password.html', {'msg':msg})