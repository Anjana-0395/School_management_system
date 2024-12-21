from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from .models import Student, LibraryHistory, FeeHistory,Staff, User,Librarian
from .serializers import StudentSerializer, LibraryHistorySerializer, FeeHistorySerializer,StaffSerializer,LibrarianSerializer,UserSerializer
from .permissions import IsAdminUser, IsStaffUser, IsLibrarianUser,IsAdminOrStaff,IsAdminOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
# admin dashboard api
class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated & IsAdminUser]

    def get(self, request):
        students = Student.objects.count()
        staff = Staff.objects.count()
        librarian = Librarian.objects.count()
        context = {
            'total_students': students,
            'total_staff': staff,
            'total_librarian': librarian,
        }
        return render(request,'admin/admin_dashboard.html',context)


# staff dashboard api
class StaffDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated & IsStaffUser]

    def get(self, request):
        staff = Staff.objects.all()
        return render(request,'staff/staff_dashboard.html')


# librarian dashboard api
class LibrarianDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated & IsLibrarianUser]

    def get(self, request):
        librarian = Librarian.objects.all()
        return render(request,'librarian/librarian_dashboard.html')




class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Render the login template for GET requests
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Received data: Username={username}, Password={password}")

        if not username or not password:
            # Render login template with error
            return render(request, 'login.html', {'error': 'Username and password are required'})

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            print("Authentication failed: Invalid credentials.")

            return render(request, 'login.html', {'error': 'Invalid username or password'})
        print(f"Authenticated user: {user.username}, Role: {getattr(user, 'role', 'N/A')}")

        # Log the user in
        login(request, user)

        # Redirect based on user role
        if user.is_superuser or user.role == 'admin':
            return redirect('admin_dashboard')  # Adjust to your admin dashboard URL name
        elif user.role == 'staff':
            return redirect('staff_dashboard')  # Adjust to your staff dashboard URL name
        elif user.role == 'librarian':
            return redirect('librarian_dashboard')  # Adjust to your librarian dashboard URL name
        else:
            return render(request, 'login.html', {'error': 'Unauthorized access'})
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log the user out
        logout(request)

        # Render the login.html template
        return render(request, 'login.html', {'message': 'You have been logged out successfully.'})


# Student Views
class StudentCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    template_name = 'admin/admin_studentAdd.html'

    def get(self, request, *args, **kwargs):
        # To render the list of students and the form
        students = self.get_queryset()
        return render(request, self.template_name, {'students': students})
    
    def post(self, request, *args, **kwargs):
        # Prepare data for the serializer
        print("POST Data:", request.POST)
        data = {
            "full_name": request.POST.get("full_name"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "email": request.POST.get("email"),
            "phone_number": request.POST.get("phone_number"),
            "address": request.POST.get("address"),
            "class_name": request.POST.get("class_name"),
            "division": request.POST.get("division"),
        }
        
        # Validate and save using the serializer
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # messages.success(request, "Student added successfully!")
            return HttpResponse("""<script>alert('Added successfully.');window.location.href = '/school_app/admin/dashboard/';</script>""")
        else:
        # Add serializer errors to the template context
            print("-----------",serializer.errors)
            return render(request, self.template_name, {
                'errors': serializer.errors,
                'data': data,
            })
        
# List View for Students
class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        students = self.get_queryset()
        if request.user.role == 'admin':
            dashboard_url = reverse('admin_dashboard')
            template_name = 'admin/admin_studentView.html'

        elif request.user.role == 'staff':
            dashboard_url = reverse('staff_dashboard')
            template_name = 'staff/staff_studentView.html'           

        else:
            dashboard_url = reverse('librarian_dashboard')  # Fallback in case of unknown roles
            template_name = 'staff/staff_studentView.html'           
        return render(request, template_name, {'students': students,'dashboard_url':dashboard_url})  

# For updating a student's details
class StudentUpdateAPIView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        student = self.get_object()  # Retrieve the student by the primary key (pk)
        return render(request, 'admin/admin_studentEdit.html', {'student': student})

    def post(self, request, *args, **kwargs):
        student = self.get_object()
        
        data = {
            "full_name": request.POST.get("full_name"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "email": request.POST.get("email"),
            "phone_number": request.POST.get("phone_number"),
            "address": request.POST.get("address"),
            "class_name": request.POST.get("class_name"),
            "division": request.POST.get("division"),
        }
        
        serializer = self.get_serializer(instance=student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # messages.success(request, "Student update successfully!")
            return HttpResponse("""<script>alert('Updated successfully.');window.location.href = '/school_app/admin/student_detail/';</script>""")

            # return redirect('admin_student_detail')
        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_studentEdit.html', {
                'student': student,
                'errors': serializer.errors,
                'data': data,
            })
        
class StudentDeleteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        # Get the student object or return 404
        student = get_object_or_404(Student, pk=pk)

        # Delete the student
        student.delete()
        # messages.success(request, "Student deleted successfully!")
        # Redirect to the student list page or return a success response
        return redirect('admin_student_detail')

# Staff views----------------------

class StaffCreateAPIView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    template_name = 'admin/admin_staffAdd.html'

    def get(self, request, *args, **kwargs):
        # Render the form to add a staff member
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Collect the POST data from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = "staff"  # Explicitly setting role to staff

        # Step 1: Create the User instance (with the role of 'staff')
        user = User(
            username=username,
            email=email,
            role=role,
            password=make_password(password)  # Hash the password
        )
        user.save()  # Save the User instance

        # Step 2: Create the Staff profile and link it to the User
        staff_name = request.POST.get("staff_name")
        department = request.POST.get("department")
        joining_date = request.POST.get("joining_date")

        staff = Staff(
            user=user,  # Link to the User instance
            staff_name=staff_name,
            department=department,
            joining_date=joining_date
        )
        staff.save()  # Save the Staff instance

        # Redirect or show success message
        return HttpResponse("""<script>alert('Staff added successfully.');window.location.href = '/school_app/admin/dashboard/';</script>""")

class StaffListAPIView(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        staff = self.get_queryset()
        return render(request, 'admin/admin_staffView.html', {'staff': staff})

class StaffUpdateAPIView(generics.UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        staff = self.get_object()  # Retrieve the staff by the primary key (pk)
        return render(request, 'admin/admin_staffEdit.html', {'staff': staff})

    def post(self, request, *args, **kwargs):
        staff = self.get_object()
        
        
        data = {
            "staff_name": request.POST.get("staff_name"),
            "department": request.POST.get("department"),
            "joining_date": request.POST.get("joining_date"),
        }
        
        serializer = self.get_serializer(instance=staff, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return HttpResponse("""<script>alert('Staff Updated successfully.');window.location.href = '/school_app/admin/staff_detail/';</script>""")

        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_staffEdit.html', {
                'staff': staff,
                'errors': serializer.errors,
                'data': data,
            })

class StaffDeleteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        # Get the staff object or return 404
        staff = get_object_or_404(Staff, pk=pk)

        # Delete the student
        staff.delete()
        # Redirect to the staff list page or return a success response
        return redirect('admin_staff_detail')
# Librarian views-------------

class LibrarianCreateAPIView(APIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    template_name = 'admin/admin_librarianAdd.html'

    def get(self, request, *args, **kwargs):
        # Render the form to add a staff member
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Collect the POST data from the form
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = "librarian"  # Explicitly setting role to staff

        # Step 1: Create the User instance (with the role of 'staff')
        user = User(
            username=username,
            email=email,
            role=role,
            password=make_password(password)  # Hash the password
        )
        user.save()  # Save the User instance

        # Step 2: Create the librarian profile and link it to the User
        librarian_name = request.POST.get("librarian_name")
        joining_date = request.POST.get("joining_date")
        library_section = request.POST.get("library_section")

        librarian = Librarian(
            user=user,  # Link to the User instance
            librarian_name=librarian_name,
            joining_date=joining_date,
            library_section=library_section
        )
        librarian.save()  # Save the Staff instance

        # Redirect or show success message
        return HttpResponse("""<script>alert('Librarian added successfully.');window.location.href = '/school_app/admin/dashboard/';</script>""")

class LibrarianListAPIView(generics.ListAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list
        librarian = self.get_queryset()
        return render(request, 'admin/admin_LibrarianView.html', {'librarian': librarian})

class LibrarianUpdateAPIView(generics.UpdateAPIView):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        librarian = self.get_object()  # Retrieve the librarian by the primary key (pk)
        return render(request, 'admin/admin_librarianEdit.html', {'librarian': librarian})

    def post(self, request, *args, **kwargs):
        librarian = self.get_object()
        
        
        data = {
            "librarian_name": request.POST.get("librarian_name"),
            "joining_date": request.POST.get("joining_date"),
            "library_section": request.POST.get("library_section"),
        }
        
        serializer = self.get_serializer(instance=librarian, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return HttpResponse("""<script>alert('Librarian Updated successfully.');window.location.href = '/school_app/admin/librarian_detail/';</script>""")

        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_staffEdit.html', {
                'librarian': librarian,
                'errors': serializer.errors,
                'data': data,
            })

class LibrarianDeleteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        # Get the student object or return 404
        librarian = get_object_or_404(Librarian, pk=pk)

        # Delete the student
        librarian.delete()
        # Redirect to the librarian list page or return a success response
        return redirect('admin_librarian_detail')


# FeeHistory Views
class StudentFeeListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        students = self.get_queryset()
        # Determine the appropriate dashboard URL based on the user's role
        if request.user.role == 'admin':
            dashboard_url = reverse('admin_dashboard')
        elif request.user.role == 'staff':
            dashboard_url = reverse('staff_dashboard')
        else:
            dashboard_url = reverse('default_dashboard')  # Fallback in case of unknown roles

        return render(request, 'admin/student_feeList.html', {'students': students,'dashboard_url':dashboard_url}) 
class FeeHistoryCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['pk']) # Retrieve the student by the primary key (pk)
        return render(request, 'admin/admin_feeAdd.html', {'student': student})

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['pk'])
        
        # Collect FeeHistory data from POST request
        data = {
            "student": student.id,  # Associate with Student
            "fee_type": request.POST.get("fee_type"),
            "amount": request.POST.get("amount"),
            "payment_date": request.POST.get("payment_date"),
            "remarks": request.POST.get("remarks"),
        }
        serializer = FeeHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("""<script>alert('Fee details added.');window.location.href = '/school_app/student/fee_list/';</script>""")
        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_feeAdd.html', {
                'student': student,
                'errors': serializer.errors,
                'data': data,
            }) 
class FeeHistoryListAPIView(generics.ListCreateAPIView):
    queryset = FeeHistory.objects.all()
    serializer_class = FeeHistorySerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        fee_history = self.get_queryset()
        # Determine the appropriate dashboard URL based on the user's role
        if request.user.role == 'admin':
            dashboard_url = reverse('admin_dashboard')
        elif request.user.role == 'staff':
            dashboard_url = reverse('staff_dashboard')
        else:
            dashboard_url = reverse('default_dashboard')  # Fallback in case of unknown roles

        return render(request, 'admin/admin_feeView.html', {'fee_history': fee_history,'dashboard_url':dashboard_url}) 
class FeeHistoryUpdateAPIView(generics.UpdateAPIView):
    queryset = FeeHistory.objects.all()
    serializer_class = FeeHistorySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        fee_history = self.get_object()  
        return render(request, 'admin/admin_feeEdit.html', {'fee_history': fee_history})

    def post(self, request, *args, **kwargs):
        fee_history = self.get_object()
        
        data = {
            "fee_type": request.POST.get("fee_type"),
            "amount": request.POST.get("amount"),
            "payment_date": request.POST.get("payment_date"),
            "remarks": request.POST.get("remarks"),
        }
        print("==========",data)
        serializer = self.get_serializer(instance=fee_history, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # messages.success(request, "library_history update successfully!")
            return HttpResponse("""<script>alert('Fee history updated successfully.');window.location.href = '/school_app/student/feeHistrory_view/';</script>""")

        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_feeEdit.html', {
                'fee_history': fee_history,
                'errors': serializer.errors,
                'data': data,
            })
class FeeHistoryDeleteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        # Get the student object or return 404
        fee_history = get_object_or_404(FeeHistory, pk=pk)
        fee_history.delete()
        return redirect('feeHistory_view')

# LibraryHistory Views
class StudentLibraryListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        students = self.get_queryset()
        return render(request, 'admin/student_libraryList.html', {'students': students})  
class LibraryHistoryCreateAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = LibraryHistorySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['pk']) # Retrieve the student by the primary key (pk)
        return render(request, 'admin/admin_libraryAdd.html', {'student': student})

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, pk=self.kwargs['pk'])
        
        # Collect LibraryHistory data from POST request
        data = {
            "student": student.id,  # Associate with Student
            "book_name": request.POST.get("book_name"),
            "borrow_date": request.POST.get("borrow_date"),
            "return_date": request.POST.get("return_date"),
            "status": request.POST.get("status"),
        }
        print("POST Data:", request.POST)
        print("Data being sent to serializer:", data)
        serializer = LibraryHistorySerializer(data=data)
        if serializer.is_valid():
            try:
                print("========",serializer.is_valid())
                serializer.save()
                return HttpResponse("""<script>alert('Library details added.');window.location.href = '/school_app/student/library_list/';</script>""")
            except ValidationError as e:
                # If model validation fails, catch the error and pass it to the template
                print("ValidationError:", e)
                return render(request, 'admin/admin_libraryAdd.html', {
                    'student': student,
                    'errors': e.message_dict,  # Pass the model validation errors
                    'data': data,
                }) 
        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_libraryAdd.html', {
                'student': student,
                'errors': serializer.errors,
                'data': data,
            })        
class LibraryHistoryListAPIView(generics.ListCreateAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer

    def get(self, request, *args, **kwargs):
        # Call the API view to get the list of students
        library_history = self.get_queryset()
        students = self.get_queryset()
        if request.user.role == 'admin':
            dashboard_url = reverse('admin_dashboard')
            template_name = 'admin/admin_libraryView.html'
        elif request.user.role == 'staff':
            dashboard_url = reverse('staff_dashboard')
            template_name = 'staff/staff_libraryView.html'

        else:
            dashboard_url = reverse('librarian_dashboard')  # Fallback in case of unknown roles
            template_name = 'staff/staff_libraryView.html'
        return render(request, template_name, {'library_history': library_history,'dashboard_url':dashboard_url})  
class LibraryHistoryUpdateAPIView(generics.UpdateAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        library_history = self.get_object()  
        return render(request, 'admin/admin_libraryEdit.html', {'library_history': library_history})

    def post(self, request, *args, **kwargs):
        library_history = self.get_object()
        
        data = {
            "book_name": request.POST.get("book_name"),
            "borrow_date": request.POST.get("borrow_date"),
            "return_date": request.POST.get("return_date"),
            "status": request.POST.get("status"),
        }
        print("==========",data)
        serializer = self.get_serializer(instance=library_history, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # messages.success(request, "library_history update successfully!")
            return HttpResponse("""<script>alert('Library history updated successfully.');window.location.href = '/school_app/student/libraryHistrory_view/';</script>""")

        else:
            # Add serializer errors to the template context
            print("Errors:", serializer.errors)
            return render(request, 'admin/admin_libraryEdit.html', {
                'library_history': library_history,
                'errors': serializer.errors,
                'data': data,
            })
class LibraryHistoryDeleteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        # Get the student object or return 404
        library_history = get_object_or_404(LibraryHistory, pk=pk)
        library_history.delete()
        return redirect('libraryHistory_view')