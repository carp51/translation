from django.db import models
from django.contrib.auth import get_user_model


class dialylog(models.Model):

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    source_text = models.CharField(max_length=100)
    tranlated_text = models.CharField(max_length=100)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.source_text
        