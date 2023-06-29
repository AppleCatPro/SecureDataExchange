from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, ConfidentialData, Message, AuditLog
from .forms import ConfidentialDataForm, MessageForm, CustomUserCreationForm, CustomUserChangeForm


def home(request):
    return render(request, 'home.html')


# @login_required
# def profile_view(request):
#     user = request.user
#     return render(request, 'profile.html', {'user': user})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        # 'confidential_data': decrypted_data
        'form': form,
        'user': request.user
    }
    return render(request, 'profile.html', context)


def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_detail.html', {'user': user})


def confidential_data_detail(request, data_id):
    data = get_object_or_404(ConfidentialData, id=data_id)
    return render(request, 'confidential_data_detail.html', {'data': data})


# def message_detail(request, message_id):
#     message = get_object_or_404(Message, id=message_id)
#     return render(request, 'message_detail.html', {'message': message})

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Проверка статуса сообщения и обновление на "прочитано", если нужно
    if not message.is_read:
        message.is_read = True
        message.save()
    if request.method == 'POST':
        # Проверяем, была ли нажата кнопка удаления
        if 'delete' in request.POST:
            message.delete_message()
            messages.success(request, 'Сообщение успешно удалено.')
            return redirect('message_list')
    context = {
        'message': message
    }
    return render(request, 'message_detail.html', context)


def user_create(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Перенаправление на список пользователей
    else:
        form = CustomUserForm()
    return render(request, 'user_create.html', {'form': form})


@login_required
def dashboard(request):
    # Получить конфиденциальные данные текущего пользователя
    user1 = request.user
    data = ConfidentialData.objects.filter(user=user1)
    user = CustomUser.objects.get(username=user1.username)

    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Доступ к dashboard')
    log_entry.save()

    # Дешифруем и отображаем данные только для текущего пользователя
    # user_key = user.encryption_key
    # print(user_key)
    # f = Fernet(user_key)
    # decrypted_data = [f.decrypt(d.data.encode()).decode() for d in data]

    context = {
        # 'confidential_data': decrypted_data
        'confidential_data': data,
        'user': user
    }
    return render(request, 'dashboard.html', context)


def confidential_data_create(request):
    if request.method == 'POST':
        form = ConfidentialDataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return redirect('dashboard')  # Перенаправление на список конфиденциальных данных

    # if request.method == 'POST':
    #     form = ConfidentialDataForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('data_list')  # Перенаправление на список конфиденциальных данных
    else:
        form = ConfidentialDataForm()
    return render(request, 'confidential_data_create.html', {'form': form})


def message_create(request):
    user = request.user
    data_list = ConfidentialData.objects.filter(user=request.user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')  # Перенаправление на список сообщений
    else:
        form = MessageForm()
    return render(request, 'message_create.html', {'form': form, 'data_list': data_list, 'user': user})


# def message_list(request):
#     # messages = Message.objects.all()
#     messages = Message.objects.filter(sender=request.user)
#     return render(request, 'message_list.html', {'messages': messages})


def message_list(request):
    # Retrieve only sent messages
    sent_messages = Message.objects.filter(sender=request.user)

    # Retrieve incoming messages
    incoming_messages = Message.objects.filter(recipient=request.user)

    return render(request, 'message_list.html',
                  {'sent_messages': sent_messages, 'incoming_messages': incoming_messages})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Перенаправление в личный кабинет
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')  # Перенаправление на домашнюю страницу
    return render(request, 'delete_profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile_edit.html', {'form': form})


def edit_data(request, data_id):
    # Получаем объект данных по его идентификатору
    user = request.user
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Проверяем, является ли текущий пользователь владельцем данных
    if data.user != request.user:
        # Если пользователь не является владельцем данных, перенаправляем его на страницу с ошибкой доступа или другую необходимую страницу
        return redirect('access_denied')

    if request.method == 'POST':
        # Если запрос является POST-запросом, обрабатываем форму данных
        form = ConfidentialDataForm(request.POST, instance=data)
        if form.is_valid():
            # Если форма данных действительна, сохраняем обновленные данные
            form.save()
            # Перенаправляем пользователя на страницу с подтверждением обновления данных
            return redirect('data_updated')
    else:
        # Если запрос не является POST-запросом, создаем форму данных с исходными значениями
        form = ConfidentialDataForm(instance=data)

    # Журналирование доступа к панели управления
    # log_entry = AuditLog(user=user, action='Доступ к редактируемым данным', ip_address=request.META['REMOTE_ADDR'],
    #                      success=True)
    # log_entry.save()
    # Отображаем шаблон edit_data.html с формой данных
    return render(request, 'edit_data.html', {'form': form})


@login_required
def delete_data(request, data_id):
    # Получаем объект данных по его идентификатору
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Убеждаемся, что текущий пользователь является владельцем данных
    if data.user == request.user:
        # Проверяем, является ли запрос POST-запросом
        if request.method == 'POST':
            # Если запрос POST, удаляем данные
            data.delete()
            # Перенаправляем пользователя на страницу dashboard или на другую страницу по вашему выбору
            return redirect('dashboard')

        # Отображаем шаблон delete_data.html для подтверждения удаления
        return render(request, 'delete_data.html', {'data': data})

    # Если текущий пользователь не является владельцем данных, отображаем ошибку или перенаправляем на другую страницу
    return redirect('access_denied')


@login_required
def view_data(request, data_id):
    # Получаем объект данных по его идентификатору
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Убеждаемся, что текущий пользователь является владельцем данных
    if data.user == request.user:
        # Отображаем шаблон view_data.html с данными
        return render(request, 'view_data.html', {'data': data})

    # Если текущий пользователь не является владельцем данных, отображаем ошибку или перенаправляем на другую страницу
    return redirect('access_denied')


def data_updated(request):
    # user = request.user
    # Журналирование доступа к панели управления
    # log_entry = AuditLog(user=user, action='Данные обновлены', ip_address=request.META['REMOTE_ADDR'],
    #                      success=True)
    # log_entry.save()
    return render(request, 'data_updated.html')


def access_denied(request):
    # user = request.user
    # # Журналирование доступа к панели управления
    # log_entry = AuditLog(user=user, action='Доступ запрещен', ip_address=request.META['REMOTE_ADDR'],
    #                      success=True)
    # log_entry.save()
    return render(request, 'access_denied.html')
