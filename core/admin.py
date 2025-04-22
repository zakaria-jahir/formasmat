from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Formation, Session, SessionDate, 
    TrainingRoom, TrainingWish, 
    CompletedTraining, Trainer, RPE
)

# Register your models here.

class SessionDateInline(admin.TabularInline):
    model = SessionDate
    extra = 1

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'formation', 'get_dates', 'get_trainers', 'status', 'iperia_opening_date', 'iperia_deadline')
    list_filter = ('status', 'formation', 'trainers')
    search_fields = ('formation__name', 'trainers__username', 'trainers__last_name')
    inlines = [SessionDateInline]
    filter_horizontal = ('trainers',)

    def get_dates(self, obj):
        return ", ".join([date.date.strftime("%d/%m/%Y") for date in obj.dates.all()])
    get_dates.short_description = "Dates"

    def get_trainers(self, obj):
        """Retourne la liste des formateurs sous forme de chaîne."""
        return ", ".join([trainer.get_full_name() for trainer in obj.trainers.all()])
    get_trainers.short_description = "Formateurs"

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_iperia', 'duration')
    search_fields = ('name', 'code_iperia')

@admin.register(TrainingRoom)
class TrainingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity')
    search_fields = ('name', 'address')

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('specialties', 'created_at')
    ordering = ('last_name', 'first_name')
    filter_horizontal = ('specialties',)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Nom complet'

@admin.register(RPE)
class RPEAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('name',)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_trainer')
    list_filter = ('is_staff', 'is_trainer', 'groups')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {'fields': ('is_trainer', 'address', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(TrainingWish)
admin.site.register(CompletedTraining)
