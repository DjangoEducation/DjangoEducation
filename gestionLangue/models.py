from django.db import models
from accounts.models import CustomUser

class Voice(models.Model):
    AudioMp3 = models.FileField(upload_to='audio/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    AudioText = models.TextField()
    AudioLangue = models.CharField(max_length=100, default='anglais')

    def __str__(self):
        return f"Voice ID: {self.id}, User ID: {self.user.id}"  # Use 'id' for primary key and 'user.id' for user reference


class SortieVoice(models.Model):
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE)  # Crée une relation avec Voice
    AudioSortieMp3 = models.FileField(upload_to='audio/sortie/')
    AudioSortieText = models.TextField()
    AudioLangue = models.CharField(max_length=100)

    def __str__(self):
        return f"SortieVoice ID: {self.id}, Voice ID: {self.voice.id}"  # Use 'id' instead of 'voice_id'
