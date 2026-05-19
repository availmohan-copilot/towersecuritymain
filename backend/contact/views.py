import json
import urllib.request
import urllib.parse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        name    = data.get('name', '')
        email   = data.get('email', '')
        phone   = data.get('phone', '')
        subject = data.get('subject', '')
        message = data.get('message', '')

        # SendGrid HTTP API
        payload = json.dumps({
            "personalizations": [{
                "to": [{"email": "thetowersecurity@gmail.com"}]
            }],
            "from": {"email": "towersecuritycompany@gmail.com"},
            "subject": f"Contact: {subject}",
            "content": [{
                "type": "text/plain",
                "value": f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            }]
        }).encode('utf-8')

        api_key = settings.SENDGRID_API_KEY
        print(f"API KEY CHECK: {api_key[:10] if api_key else 'NONE'}")  # debug

        req = urllib.request.Request(
            'https://api.sendgrid.com/v3/mail/send',
            data=payload,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )

        try:
            urllib.request.urlopen(req)
            return JsonResponse({'status': 'success'})
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"SENDGRID ERROR: {e.code} - {error_body}")
            return JsonResponse({'status': 'error', 'message': error_body}, status=400)
        except Exception as e:
            print(f"GENERAL ERROR: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error'}, status=400)