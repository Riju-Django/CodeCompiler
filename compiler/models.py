from django.db import models

class Question(models.Model):
    titel = models.TextField()
    descriptions = models.TextField()
    image = models.ImageField(upload_to="question_image/")
    testcase = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.titel}"
