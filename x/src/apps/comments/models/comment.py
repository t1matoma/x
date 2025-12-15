from django.db import models
from django.conf import settings



class Comment(models.Model):
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='comments',
	)
	post = models.ForeignKey(
		'posts.Post',
		on_delete=models.CASCADE,
		related_name='comments',
		null=True,  # Making it nullable for now, remove after migration
		blank=True
	)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.content
