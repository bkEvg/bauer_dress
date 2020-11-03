from django.shortcuts import render, get_object_or_404, redirect
from .models import OftenQuestion, Question
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib import messages




def privacy(request):
	return render(request, 'information/privacy.html')

def help_page(request):
	return render(request, 'information/help_page.html')

def rules(request):
	return render(request, 'information/rules.html')

def about(request):
	return render(request, 'information/about.html')

def delivery(request):
	return render(request, 'information/delivery.html')



class QuestionListView(generic.ListView):
	model = OftenQuestion
	template_name = 'information/faq.html'
	context_object_name = 'questions'

	def get_queryset(self):
		return OftenQuestion.objects.filter(response__isnull=False).order_by('-updated')


#
class QuestionCreateView(SuccessMessageMixin, generic.CreateView):
	model = Question
	fields = ['email', 'name', 'question']
	success_url = '/'
	success_message = "Ваш вопрос отправлен администрации магазина!"


class QuestionUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, 
																	generic.UpdateView):
	model = OftenQuestion
	fields = ['name', 'question', 'response']
	template_name = 'information/question_form_update.html'
	success_url = '/info/FAQ'
	success_message = "Вопрос отредактирован!"


	def test_func(self):
		if self.request.user.is_staff:
			return True
		else:
			return False



class QuestionDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, 
																	generic.DeleteView):
	model = OftenQuestion
	success_url = '/info/FAQ'
	success_message = "Вопрос удален!"


	def test_func(self):
		if self.request.user.is_staff:
			return True
		else:
			return False

@staff_member_required
def answerQuestion(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	url = request.META['HTTP_REFERER']
	if question.response:
		subject = 'Ответ на вопрос'
		body = 'Здравствуйте {0},\n\nВы недавно оставляли вопрос на сайте Bauer Dress, ваш вопрос:"{1}" \n\nОтвечаем:\n"{2}" \n\nС уважением команда интернет-магазина Bauer Dress'.format(question.name, question.question, question.response)
		mail_sent = send_mail(subject, body, settings.EMAIL_HOST_USER, [question.email])
		question.delete()
		messages.success(request, message='Ответ был отправлен и поэтому удален!')
		return redirect(url)
	else:
		messages.error(request, message='Ответь на вопрос!')
		return redirect(url)
