from django.db import models
from accounts.models import Course  

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')  # Lien avec le cours
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    total_questions = models.IntegerField(default=0)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)  # Score de passage en %
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz: {self.title} ({self.course.title})"


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')  # Lien avec le quiz
    question_text = models.TextField()
    question_type = models.TextField()
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)  # Points pour cette question
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question_text} (Quiz: {self.quiz.title})"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  # Lien avec la question
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # Vrai si c'est la bonne réponse

    def __str__(self):
        return f"Choice: {self.choice_text} (Question: {self.question.question_text})"
