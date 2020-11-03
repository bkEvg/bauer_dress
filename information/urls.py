from django.urls import path
from . import views


app_name = 'info'
urlpatterns = [
    path('privacy/', views.privacy, name='privacy'),
    path('help/', views.help_page, name='help'),
    path('rules/', views.rules, name='rules'),
    path('about/', views.about, name='about'),
    path('delivery/', views.delivery, name='delivery'),
    path('FAQ/', views.QuestionListView.as_view(), name='faq'),
    path('FAQ/create/', views.QuestionCreateView.as_view(), name='faq-create'),
    path('FAQ/update/<int:pk>/', views.QuestionUpdateView.as_view(), name='faq-update'),
    path('FAQ/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='faq-delete'),
    path('admin/response/<question_id>/', views.answerQuestion, name='response'),
]
