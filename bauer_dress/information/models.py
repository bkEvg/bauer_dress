from django.db import models
from ckeditor.fields import RichTextField

class OftenQuestion(models.Model):
	question = RichTextField(blank=False, null=True, verbose_name='Вопрос')
	response = RichTextField(blank=False, null=True, verbose_name='ответ')
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

class Delivery(models.Model):
	title = models.CharField(max_length=200, blank=False, verbose_name='Заголовок')
	content = RichTextField(blank=False, verbose_name='Контент')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "доставка"
		verbose_name_plural = "доставка"

class Help(models.Model):
	title = models.CharField(max_length=200, blank=False, verbose_name='Заголовок')
	content = RichTextField(blank=False, verbose_name='Контент')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "помощь"
		verbose_name_plural = "помощь"

class Privacy(models.Model):
	content = RichTextField(blank=False, verbose_name='Контент')

	def __str__(self):
		return self.content[:100]
	

	class Meta:
		verbose_name = "приватность"
		verbose_name_plural = "приватность"

class About(models.Model):
	title = models.CharField(max_length=200, blank=False, verbose_name='Заголовок')
	content = RichTextField(blank=False, verbose_name='Контент')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "о нас"
		verbose_name_plural = "о нас"



