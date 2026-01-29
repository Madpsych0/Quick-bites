from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

def scanner_view(request):
    """
    QR code scanner interface for canteen staff
    Optimized for smartphone screens
    """
    return render(request, 'scanner/scanner.html')

@csrf_exempt
def scan_ticket(request):
    """
    Handle QR code scanning and ticket redemption
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            
            # Make request to main app's redeem endpoint
            response = requests.post(
                'http://localhost:8000/api/redeem-ticket/',
                json={'qr_data': qr_data},
                headers={'Content-Type': 'application/json'}
            )
            
            return JsonResponse(response.json())
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error processing scan'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
