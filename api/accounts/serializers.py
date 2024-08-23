from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField
from .models import (
    Employee, EntityType, BaseEntity, Notification, Document,
    Department, Role, Branch,
    )

class EntityTypeSerializer(ModelSerializer):
    class Meta:
        model = EntityType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'updated_by']

    def update(self, instance, validated_data):
        # Set the updated_by field to the current user
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user

        return super().update(instance, validated_data)


class BaseEntitySerializer(ModelSerializer):
    class Meta:
        model = BaseEntity
        fields = ['id', 'full_name', 'username', 'email', 'entity_type', 'address',
                  'phone_number', 'branch', 'is_active', 'is_staff', 'date_of_birth',
                  'last_login', 'created_at', 'updated_at', 'tax_identifier_number',
                  'first_name', 'last_name', 'password']
        read_only_fields = ['id', 'last_login', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class EmployeeSerializer(BaseEntitySerializer):
    class Meta(BaseEntitySerializer.Meta):
        model = Employee
        fields = BaseEntitySerializer.Meta.fields + ['position', 'role', 'salary', 'department']
        extra_kwargs = BaseEntitySerializer.Meta.extra_kwargs


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']



class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

