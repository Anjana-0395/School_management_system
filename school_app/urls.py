from django.urls import path
from .views import (
    LoginAPIView,
    LogoutAPIView,
    AdminDashboardAPIView,
    StaffDashboardAPIView,
    LibrarianDashboardAPIView,
    StudentCreateAPIView,
    StudentListAPIView,
    StudentUpdateAPIView,
    StudentDeleteAPIView,
    StaffCreateAPIView,
    StaffListAPIView,
    StaffUpdateAPIView,
    StaffDeleteAPIView,
    LibrarianCreateAPIView,
    LibrarianListAPIView,
    LibrarianUpdateAPIView,
    LibrarianDeleteAPIView,
    StudentLibraryListAPIView,
    LibraryHistoryCreateAPIView,
    LibraryHistoryListAPIView,
    LibraryHistoryUpdateAPIView,
    LibraryHistoryDeleteAPIView,
    StudentFeeListAPIView,
    FeeHistoryCreateAPIView,FeeHistoryListAPIView,FeeHistoryUpdateAPIView,FeeHistoryDeleteAPIView,
)

urlpatterns = [
    # Authentication
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    # Admin Dashboard Endpoints
    path('admin/dashboard/', AdminDashboardAPIView.as_view(), name='admin_dashboard'),
    path('admin/students/', StudentCreateAPIView.as_view(), name='admin_students'),
    path('admin/student_detail/', StudentListAPIView.as_view(), name='admin_student_detail'),
    path('students/edit/<int:pk>/', StudentUpdateAPIView.as_view(), name='student_edit'),  # For editing students
    path('students/delete/<int:pk>/', StudentDeleteAPIView.as_view(), name='student_delete'),  # Delete student
    path('admin/staff/', StaffCreateAPIView.as_view(), name='admin_staff'),
    path('admin/staff_detail/', StaffListAPIView.as_view(), name='admin_staff_detail'),
    path('staff/edit/<int:pk>/', StaffUpdateAPIView.as_view(), name='staff_edit'),  # For editing staff
    path('staff/delete/<int:pk>/', StaffDeleteAPIView.as_view(), name='staff_delete'), 

    path('admin/librarian/', LibrarianCreateAPIView.as_view(), name='admin_librarian'),
    path('admin/librarian_detail/', LibrarianListAPIView.as_view(), name='admin_librarian_detail'),
    path('librarian/edit/<int:pk>/', LibrarianUpdateAPIView.as_view(), name='librarian_edit'), 
    path('librarian/delete/<int:pk>/', LibrarianDeleteAPIView.as_view(), name='librarian_delete'),
 
    path('student/library_list/', StudentLibraryListAPIView.as_view(), name='student_libraryList'),
    path('student/libraryHistory_add/<int:pk>/', LibraryHistoryCreateAPIView.as_view(), name='libraryHistory_add'),
    path('student/libraryHistrory_view/', LibraryHistoryListAPIView.as_view(), name='libraryHistory_view'),
    path('libraryHistory/edit/<int:pk>/', LibraryHistoryUpdateAPIView.as_view(), name='libraryHistory_edit'),  
    path('libraryHistory/delete/<int:pk>/', LibraryHistoryDeleteAPIView.as_view(), name='libraryHistory_delete'),  

    path('student/fee_list/', StudentFeeListAPIView.as_view(), name='student_feeList'),
    path('student/feeHistory_add/<int:pk>/', FeeHistoryCreateAPIView.as_view(), name='feeHistory_add'),
    path('student/feeHistrory_view/', FeeHistoryListAPIView.as_view(), name='feeHistory_view'),
    path('feeHistory/edit/<int:pk>/', FeeHistoryUpdateAPIView.as_view(), name='feeHistory_edit'),  
    path('feeHistory/delete/<int:pk>/', FeeHistoryDeleteAPIView.as_view(), name='feeHistory_delete'),  

    # Staff Dashboard Endpoints
    path('staff/dashboard/', StaffDashboardAPIView.as_view(), name='staff_dashboard'),

    # Librarian Dashboard Endpoints
    path('librarian/dashboard/', LibrarianDashboardAPIView.as_view(), name='librarian_dashboard'),
]
