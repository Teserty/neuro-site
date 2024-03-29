from django.db import models


class Dialog(models.Model):
    user_text = models.TextField(blank=True, default="")
    result = models.TextField(blank=True, default="")
    is_good_result = models.BooleanField(default=False)


class NewDialog(models.Model):
    user_text = models.TextField(blank=True, default="")
    our_text = models.TextField(blank=True, default="")
    result = models.TextField(blank=True, default="")
    is_good_result = models.BooleanField(default=False)
    stage = models.IntegerField(default=0)

#apt-cash depends bash - зависимости
#apt-cash rdepends bash - обрптные зависимости
#apt-get remove bash
# purge - удалит вместе с конфигами
#apt-get upgrade