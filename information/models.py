from django.db import models

class OftenQuestion(models.Model):
	question = models.TextField(blank=False, null=True, verbose_name='Вопрос')
	response = models.TextField(blank=False, null=True, verbose_name='ответ')
	created = models.DateTimeField(auto_now_add=True, null=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.question[:15] + '...'

	class Meta:
		verbose_name = 'часто задаваемый вопрос'
		verbose_name_plural = 'часто задаваемые вопросы'


class Question(models.Model):
	email = models.EmailField(verbose_name='Email')
	name = models.CharField(max_length=50, verbose_name='Имя')
	question = models.TextField(blank=False, null=True, verbose_name='Вопрос')
	created = models.DateTimeField(auto_now_add=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	response = models.TextField(blank=True, null=True, verbose_name='Ответ')

	def __str__(self):
		return self.question[:15]

	class Meta:
		verbose_name = 'вопрос'
		verbose_name_plural = 'вопросы'