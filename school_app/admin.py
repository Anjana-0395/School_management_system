from django.contrib import admin
from .models import User, Student, Staff, LibraryHistory, FeeHistory,Librarian

# Customize the User admin interface
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'class_name', 'division', 'created_at')
    list_filter = ('class_name', 'division')
    search_fields = ('full_name', 'email', 'class_name', 'division')
    ordering = ('full_name',)

class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_name', 'department', 'joining_date')
    list_filter = ('department', 'joining_date')
    search_fields = ('user__username', 'user__email', 'department')
    ordering = ('user__username',)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('user', 'librarian_name', 'library_section', 'joining_date')
    list_filter = ('library_section', 'joining_date')
    search_fields = ('user__username', 'user__email', 'library_section')
    ordering = ('user__username',)


class LibraryHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'book_name', 'borrow_date', 'return_date', 'status')
    list_filter = ('status', 'borrow_date', 'return_date')
    search_fields = ('student__full_name', 'book_name', 'status')
    ordering = ('borrow_date',)

class FeeHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'payment_date', 'remarks')
    list_filter = ('fee_type', 'payment_date')
    search_fields = ('student__full_name', 'fee_type', 'amount')
    ordering = ('payment_date',)

# Register models with their respective admin interfaces
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(LibraryHistory, LibraryHistoryAdmin)
admin.site.register(FeeHistory, FeeHistoryAdmin)
admin.site.register(Librarian,LibrarianAdmin)
