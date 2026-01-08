# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    City, University, Branch, College, Department, Program,
    User, Project, Group, Notification, AcademicAffiliation,
    GroupMembers, GroupSupervisors, Role, Permission, RolePermission,
    UserRoles, GroupInvitation, ApprovalRequest, NotificationLog,
    SystemSettings, ApprovalSequence
)


# ==============================================================================
# 1. إدارة المستخدمين
# ==============================================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'name', 'email', 'phone')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('إضافات مخصصة', {'fields': ('phone', 'company_name', 'name', 'gender')}),
    )


# ==============================================================================
# 2. إدارة الموقع الجغرافي
# ==============================================================================
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('bid', 'bname_ar', 'bname_en')
    search_fields = ('bname_ar', 'bname_en')


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('uid', 'uname_ar', 'uname_en', 'type')
    search_fields = ('uname_ar', 'uname_en')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('ubid', 'university', 'city', 'location')
    list_filter = ('university', 'city')
    search_fields = ('location', 'address')


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('cid', 'name_ar', 'branch')
    list_filter = ('branch',)
    search_fields = ('name_ar', 'name_en')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name', 'college')
    list_filter = ('college',)
    search_fields = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('pid', 'p_name', 'department')
    list_filter = ('department',)
    search_fields = ('p_name',)


# ==============================================================================
# 3. إدارة الأدوار والصلاحيات
# ==============================================================================
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_ID', 'type', 'role_type')
    search_fields = ('type', 'role_type')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('perm_ID', 'name')
    search_fields = ('name',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role',)


@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)


# ==============================================================================
# 4. إدارة المشاريع والمجموعات
# ==============================================================================
# ==============================================================================
# 4. إدارة المشاريع والمجموعات
# ==============================================================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # إضافة 'college' هنا لعرضها في الجدول الرئيسي للمشاريع
    list_display = ('project_id', 'title', 'get_college_name', 'type', 'state', 'start_date')
    
    # إضافة الفلترة حسب الكلية لتسهيل البحث
    list_filter = ('college', 'type', 'state', 'start_date')
    
    search_fields = ('title', 'description', 'college__name_ar')
    readonly_fields = ('project_id',)

    # تحسين شكل صفحة الإضافة (Add Project) ليكون اختيار الكلية في البداية
    fieldsets = (
        ('الارتباط الأكاديمي', {
            'fields': ('college',)
        }),
        ('معلومات المشروع الأساسية', {
            'fields': ('title', 'description', 'type', 'state')
        }),
        ('التواريخ', {
            'fields': ('start_date', 'end_date')
        }),
    )

    # دالة لعرض اسم الكلية بالعربي في الجدول الرئيسي
    def get_college_name(self, obj):
        return obj.college.name_ar if obj.college else "غير مرتبط بكلية"
    get_college_name.short_description = 'الكلية'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'group_name', 'project')
    search_fields = ('group_name',)


@admin.register(GroupMembers)
class GroupMembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('group',)
    search_fields = ('user__username', 'group__group_name')


@admin.register(GroupSupervisors)
class GroupSupervisorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('group',)
    search_fields = ('user__username', 'group__group_name')


# ==============================================================================
# 5. إدارة الدعوات والموافقات والإشعارات
# ==============================================================================
@admin.register(GroupInvitation)
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ('invitation_id', 'group', 'invited_student', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('invited_student__username', 'group__group_name')
    readonly_fields = ('created_at', 'responded_at')


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('approval_id', 'approval_type', 'status', 'approval_level', 'created_at')
    list_filter = ('approval_type', 'status', 'approval_level')
    search_fields = ('group__group_name', 'project__title')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'recipient', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('not_ID', 'user', 'state', 'date')
    list_filter = ('state', 'date')
    search_fields = ('user__username', 'message')
    readonly_fields = ('date',)


# ==============================================================================
# 6. إدارة الإعدادات والتسلسلات
# ==============================================================================
@admin.register(AcademicAffiliation)
class AcademicAffiliationAdmin(admin.ModelAdmin):
    list_display = ('affiliation_id', 'user', 'university', 'college', 'department', 'start_date')
    list_filter = ('university', 'college', 'department', 'start_date')
    search_fields = ('user__username', 'college__name_ar', 'department__name')
    
    # لترتيب وتوضيح النموذج داخل صفحة الإضافة/التعديل
    fieldsets = (
        ('معلومات المستخدم', {
            'fields': ('user',)
        }),
        ('البيانات الأكاديمية', {
            'fields': ('university', 'college', 'department')
        }),
        ('المدة الزمنية', {
            'fields': ('start_date', 'end_date')
        }),
    )


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('setting_key', 'setting_value', 'updated_at')
    search_fields = ('setting_key',)
    readonly_fields = ('updated_at',)


@admin.register(ApprovalSequence)
class ApprovalSequenceAdmin(admin.ModelAdmin):
    list_display = ('sequence_id', 'sequence_type', 'approval_levels')
    search_fields = ('sequence_type',)
