import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        name    = data.get('name', '')
        email   = data.get('email', '')
        phone   = data.get('phone', '')
        subject = data.get('subject', '')
        message = data.get('message', '')

        send_mail(
            subject=f"Contact: {subject}",
            message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
            from_email='thetowersecurity@gmail.com',
            recipient_list=['availmohan@gmail.com'],
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)