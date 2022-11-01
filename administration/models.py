from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class Project(models.Model):
    class Languages(models.TextChoices):
        RUSSIAN = "RUSSIAN", "Русский"
        ENGLISH = "ENGLISH", "English"

    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255, choices=Languages.choices)
    channel_link = models.URLField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.user:
            user = User(first_name=self.name, last_name=self.last_name, email=self.email, username=self.username)
            user.is_staff = True
            user.save()

            user.set_password(self.password)
            user.save()

            bloggers_group = Group.objects.get(name='bloggers')
            bloggers_group.user_set.add(user)

            self.user = user
        else:
            self.user.name = self.name
            self.user.last_name = self.last_name
            self.user.email = self.email
            self.user.username = self.username

            if not self.user.check_password(self.password):
                self.user.set_password(self.password)

            self.user.save()

        return super(ProjectMember, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
