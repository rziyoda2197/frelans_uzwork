from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from accounts.models import User


@login_required
def inbox_view(request):
    """Show list of conversations."""
    # Get unique users the current user has chatted with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    user_ids = set(list(sent_to) + list(received_from))
    chat_users = User.objects.filter(id__in=user_ids)

    # Get unread count per user
    conversations = []
    for user in chat_users:
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=user) |
            Q(sender=user, receiver=request.user)
        ).order_by('-created_at').first()
        unread_count = Message.objects.filter(
            sender=user, receiver=request.user, is_read=False
        ).count()
        conversations.append({
            'user': user,
            'last_message': last_msg,
            'unread_count': unread_count,
        })
    # Sort by last message time
    conversations.sort(key=lambda c: c['last_message'].created_at if c['last_message'] else '', reverse=True)

    return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
def chat_view(request, username):
    """Chat with a specific user."""
    other_user = get_object_or_404(User, username=username)
    messages_qs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    # Mark received messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('chat', username=username)

    return render(request, 'messaging/chat.html', {
        'other_user': other_user,
        'messages': messages_qs,
    })


@login_required
def get_new_messages(request, username):
    """AJAX endpoint for fetching new messages."""
    other_user = get_object_or_404(User, username=username)
    last_id = request.GET.get('last_id', 0)
    new_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user),
        id__gt=last_id
    ).order_by('created_at')

    # Mark as read
    Message.objects.filter(
        sender=other_user, receiver=request.user,
        is_read=False, id__gt=last_id
    ).update(is_read=True)

    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'content': msg.content,
            'is_mine': msg.sender == request.user,
            'time': msg.created_at.strftime('%H:%M'),
        })
    return JsonResponse({'messages': messages_data})


@login_required
def send_message_ajax(request, username):
    """AJAX endpoint for sending messages."""
    if request.method == 'POST':
        other_user = get_object_or_404(User, username=username)
        content = request.POST.get('content', '').strip()
        if content:
            msg = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return JsonResponse({
                'status': 'ok',
                'message': {
                    'id': msg.id,
                    'sender': msg.sender.username,
                    'sender_name': msg.sender.get_full_name() or msg.sender.username,
                    'content': msg.content,
                    'is_mine': True,
                    'time': msg.created_at.strftime('%H:%M'),
                }
            })
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def unread_count(request):
    """Get unread message count for notification badge."""
    count = Message.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'count': count})
