from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="username", max_length=50)
    password = models.CharField(verbose_name="password", max_length=50)
    create_time = models.DateTimeField(verbose_name="create_time", auto_now_add=True)


class Problem(models.Model):
    title = models.CharField(verbose_name="title", max_length=50)
    problem_id = models.IntegerField(verbose_name="problem_id")
    text = models.TextField(verbose_name="text")


class Category(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)

    def __str__(self):
        return self.name


class FavoriteProblem(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="title", max_length=50)
    link = models.CharField(verbose_name="link", max_length=50)
    description = models.CharField(verbose_name="description", max_length=50)
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="create_time", auto_now_add=True)


class ProblemSet(models.Model):
    index = models.IntegerField(verbose_name="pNumber")
    title = models.CharField(verbose_name="name", max_length=50)
    content = models.TextField(verbose_name="content")
    url = models.CharField(verbose_name="url", max_length=50)


class CodeforcesContestInfo(models.Model):
    contest_id = models.IntegerField(verbose_name="contest_id")
    name = models.CharField(verbose_name="name", max_length=50)
    start_time = models.CharField(verbose_name="start_time", max_length=50)
    length = models.CharField(verbose_name="length", max_length=50)
    url = models.CharField(verbose_name="url", max_length=50)


class AtcoderContestInfo(models.Model):
    contest_id = models.CharField(verbose_name="contest_id", max_length=50)
    name = models.CharField(verbose_name="name", max_length=50)
    start_time = models.CharField(verbose_name="start_time", max_length=50)
    url = models.CharField(verbose_name="url", max_length=50)
