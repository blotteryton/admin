from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.StackedInline):
    model = ProjectMember
    exclude = ("user",)
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMemberInline, ]
