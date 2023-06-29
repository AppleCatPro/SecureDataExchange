from django.db import models
from django.contrib.auth.models import AbstractUser


# Расширение модели пользователя
class CustomUser(AbstractUser):
    # Дополнительные поля
    birth_date = models.DateField(null=True, blank=True)  # Дата рождения пользователя
    gender = models.CharField(verbose_name='Гендер',
                              max_length=10,
                              choices=[('Ж', "Женский"), ('М', "Мужской")],
                              default='М')
    # photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)  # Фотография пользователя
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)  # Город пользователя
    country = models.CharField(max_length=100, null=True, blank=True)  # Страна пользователя

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class ConfidentialData(models.Model):
    # Модель для хранения конфиденциальных данных
    title = models.CharField(max_length=100)
    data = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Связь с расширенной моделью пользователя
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    # Модель для хранения сообщений между пользователями
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attached_data = models.ForeignKey(ConfidentialData, null=True, blank=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    def delete_message(self):
        self.delete()

class AuditLog(models.Model):
    # Модель для записи аудита безопасности
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"
