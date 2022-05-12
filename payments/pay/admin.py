from django.contrib import admin
from pay.models import Year, Term, Gender, Profile, IndividualPayment, Level, Classroom, FeesForTerm, GroceriesForTerm, ClearanceForStudent, ClusterLevel
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class ClearanceForStudentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'term', 'cleared')
    list_filter = ['profile']
    search_fields = ['profile', ]


class FeesForTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'amount', 'clusterlevel')
    search_fields = ['profile', ]


class GroceriesForTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'clusterlevel', 'amount')
    search_fields = ['profile']


class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'slug')
    prepopulated_fields = {'slug': ('title', 'level'), }


class YearAdmin(admin.ModelAdmin):
    list_display = ('title', 'status',)


class GenderAdmin(admin.ModelAdmin):
    list_display = ('title',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name','clusterlevel' , 'slug',)

class ClusterLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender', 'age', 'level', 'classroom',)
    search_fields = ['user__username', 'first_name', 'last_name', ]


class IndividualPaymentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'created_on', 'cashier', 'actual_amount_paid', 'amount_paid')
    search_fields = ['profile']


class TermAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'total_days', 'status', 'slug',)
    prepopulated_fields = {'slug': ('title', 'year', 'total_days'), }


admin.site.register(ClearanceForStudent, ClearanceForStudentAdmin)
admin.site.register(GroceriesForTerm, GroceriesForTermAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(ClusterLevel, ClusterLevelAdmin)
admin.site.register(IndividualPayment, IndividualPaymentAdmin)
admin.site.register(FeesForTerm, FeesForTermAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Year, YearAdmin)
