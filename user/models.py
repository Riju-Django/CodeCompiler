from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_image/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

class UserPost(models.Model):
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.created_by.username} at {self.created_at}"

class PostComment(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.post.id}"


