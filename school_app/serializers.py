from rest_framework import serializers
from datetime import date,datetime,timezone
from .models import User, Student, Staff, LibraryHistory, FeeHistory, Librarian
from rest_framework.exceptions import  ValidationError
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.get('role', 'staff')  # Default to 'staff' if no role is provided
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.role = role
        user.save()
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value
    def validate_email(self, value):
        # Exclude the current student from the uniqueness check
        student_id = self.instance.id if self.instance else None
        if Student.objects.filter(email=value).exclude(id=student_id).exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value
    def validate_dob(self, value):
        today = date.today()
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = '__all__'

class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'

    def validate_borrow_date(self, value):
        """Ensure borrow_date is not in the future."""
        if value > date.today():
            raise serializers.ValidationError("Borrow date cannot be in the future.")
        return value

    def validate(self, data):
        """Validate return_date relative to borrow_date."""
        borrow_date = data.get('borrow_date')
        return_date = data.get('return_date')

        # Call model's clean method to validate return_date
        instance = LibraryHistory(**data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data

        
class FeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeHistory
        fields = '__all__'
        def validate_amount(self, value):
            if value <= 0:
                raise serializers.ValidationError("The amount must be greater than 0.")
            return value

        def validate_payment_date(self, value):
            # Ensure that payment date is not in the future
            if value > timezone.now().date():
                raise serializers.ValidationError("Payment date cannot be in the future.")
            return value