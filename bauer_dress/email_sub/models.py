from django.db import models

class Subscription(models.Model):
	name = models.CharField('Имя', max_length=50, null=True)
	surname = models.CharField('Фамилия', max_length=50, null=True)
	email = models.EmailField(blank=False, null=False, verbose_name='Email')
	date_sub = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

	def __str__(self):
		return self.email

	class Meta:
		verbose_name='рассылка'
		verbose_name_plural='рассылки'

