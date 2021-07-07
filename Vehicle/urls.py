from django.contrib import admin
from django.urls import path
from Admin.views import (
    Search,
    Profile, 
    ChoiceUser,
    ChangePassword, 
    AllUsers, 
    AllOwner, 
    AllPublic, 
    EditProfile,
    UserDetails,
    DeleteUser,
    EditSingleUser,
    Dashboard,
    AddVehicleType,
    AddVehicle,
    EditVehicle,
    DeleteVehicle,
    TotalVehicle,
    TrackVehicle,
    Track,
    AvailableVehicle,
    BookVehicle,
    EditBooking,
    DeleteBooking,
    TrackCompletedVehicle,
    UnpaidCompletedRent
)
from Public.views import Login, Logout, Signup, Home, Contact ,About, OwnerSignup, AdminSignup, SendEmailForForgotPassword, ForgotPassword
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name=''),
    path('choice-user/',ChoiceUser,name='choice-user'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('register/', Signup, name='register'),
    path('ownersignup/', OwnerSignup, name='ownersignup'),
    path('adminsignup/', AdminSignup, name='adminsignup'),

    path('users/', AllUsers, name='users'),
    path('all-owner/', AllOwner, name='all-owner'),
    path('all-public/', AllPublic, name='all-public'),
    
    path('profile/', Profile, name='profile'),
    path('dashboard/', Dashboard, name='dashboard'),
    path('user-details/<int:id>/', UserDetails, name='user-details'),
    path('edit-single-user/<int:id>/', EditSingleUser, name='edit-single-user'),
    path('delete-user/<int:id>/', DeleteUser, name='delete-user'),

    path('edit-profile/', EditProfile, name='edit-profile'),
    path('email-forgotpassword/', SendEmailForForgotPassword, name='email-forgotpassword'),
    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('change-password/', ChangePassword, name='change-password'),


    path('add-vehilce-type/', AddVehicleType, name='add-vehilce-type'),
    path('add-vehicle/', AddVehicle ,name="add-vehicle"),
    path('delete-vehicle/<int:id>/', DeleteVehicle, name='delete-vehicle'),
    path('total-vehicle/', TotalVehicle, name='total-vehicle'),

    path('edit-vehicle/<int:id>/', EditVehicle, name='edit-vehicle'),

    path('available-vehicle/', AvailableVehicle, name='available-vehicle'),
    
    path('book-vehicle/<int:id>/', BookVehicle, name='book-vehicle'),
    path('edit-booking/<int:id>/', EditBooking, name="edit-booking"),
    path('delete-booking/<int:id>/', DeleteBooking, name='delete-booking'),
    path('completed-rent/', TrackCompletedVehicle, name='completed-rent'),
    path('unpaid-completed-rent/', UnpaidCompletedRent, name='unpaid-completed-rent'),
    path('track-vehicle/', TrackVehicle, name='track-vehicle'),
    path('track/<int:id>/', Track, name='track'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
