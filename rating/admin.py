from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, Lesson, Grade

# Кастомизация управления пользователями (Учителя и Ученики)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Настройки отображения списка пользователей
    list_display = ('username', 'last_name', 'first_name', 'school_class', 'nickname', 'is_teacher', 'is_staff')
    list_filter = ('school_class', 'is_teacher', 'is_staff')
    search_fields = ('username', 'last_name', 'first_name', 'nickname')
    
    # Группировка полей в форме редактирования пользователя
    fieldsets = UserAdmin.fieldsets + (
        ('Школьные данные', {'fields': ('nickname', 'school_class', 'is_teacher')}),
    )
    # Поля для формы создания нового пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Школьные данные', {'fields': ('nickname', 'school_class', 'is_teacher', 'last_name', 'first_name')}),
    )

# Настройка предметов
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Настройка уроков
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('date', 'subject', 'topic', 'max_score')
    list_filter = ('subject', 'date')
    search_fields = ('topic',)
    date_hierarchy = 'date'  # Удобная навигация по датам (календарь сверху)

# Настройка оценок
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_subject', 'lesson', 'score', 'get_max_score')
    list_filter = ('lesson__subject', 'student__school_class', 'lesson__date')
    search_fields = ('student__last_name', 'student__nickname', 'lesson__topic')

    # Вспомогательные методы для вывода связанных данных в список
    @admin.display(ordering='lesson__subject', description='Предмет')
    def get_subject(self, obj):
        return obj.lesson.subject.name

    @admin.display(description='Макс. балл урока')
    def get_max_score(self, obj):
        return obj.lesson.max_score
