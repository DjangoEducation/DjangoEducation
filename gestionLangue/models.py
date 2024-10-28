from django.db import models
from accounts.models import CustomUser

class InputTranslator(models.Model):
    # User who created the input
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="input_translations")
    
    # Fields to save input text and audio
    input_text = models.TextField(blank=True, null=True)  # Save input text as plain text
    input_voice = models.FileField(upload_to="gestionLangue/input_voice/", blank=True, null=True)  # Path for audio files
    
    # Optional metadata or other fields as needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input ID: {self.id}, User ID: {self.user.id}"

class OutputTranslator(models.Model):
    # Link to the original input for which this is an output
    input_translator = models.ForeignKey(InputTranslator, on_delete=models.CASCADE, related_name="output_translations")
    
    # Fields to store translated text and audio outputs
    output_text = models.TextField(blank=True, null=True)  # Save translated text as plain text
    output_voice = models.FileField(upload_to="gestionLangue/output_voice/", blank=True, null=True)  # Path for translated audio

    # Optional metadata or other fields as needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Output ID: {self.id}, Input ID: {self.input_translator.id}"
