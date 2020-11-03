from django.contrib import admin, messages
from .models import OftenQuestion, Question
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings



def response(obj):
	return format_html('<a href="{}">Отправить ответ</a>'.format(
        reverse('info:response', args=[obj.id])))


def send_responses(modeladmin, request, queryset):
	for obj in queryset:
		if obj.response:
			subject = 'Ответ на вопрос'
			body = 'Здравствуйте {0},\n\nВы недавно оставляли вопрос на сайте Bauer Dress, ваш вопрос:"{1}" \n\nОтвечаем:\n"{2}" \n\nС уважением команда интернет-магазина Bauer Dress'.format(obj.name, obj.question, obj.response)
			send_mail(subject, body, settings.EMAIL_HOST_USER, [obj.email])
			obj.delete()
		else:
			continue
	messages.success(request, message='Все ответы отправлены')
send_responses.short_description = 'Отправить ответы'


class OftenQuestionAdmin(admin.ModelAdmin):
	list_display = ['question']
admin.site.register(OftenQuestion, OftenQuestionAdmin)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ['email', 'name', 'question', response]
	actions = [send_responses]
admin.site.register(Question, QuestionAdmin)