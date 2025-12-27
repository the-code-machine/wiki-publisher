import json
from pyexpat.errors import messages
import re
from django.http import JsonResponse
from django.shortcuts import redirect, render
import requests
from django.views.decorators.csrf import csrf_exempt
def home(request):
    return render(request, 'publisher/home.html')

def get_started(request):
    # If the user submits the form (POST request)
    if request.method == "POST":
        # 1. Get data from the form
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        # 2. Check credentials (HARDCODED FOR DEMO)
        if username_input == 'sk123' and password_input == 'root@123':
            # Success: specific user found, go to dashboard
            return redirect('dashboard')
        else:
            # Failure: Add an error message
            messages.error(request, "Invalid Bot Username or Password.")
        
    return render(request, 'publisher/get_started.html')



# --- New Dashboard Views ---
def dashboard_home(request):
    return render(request, 'publisher/dashboard/home.html')

def upload_files(request):
    # You would add logic here later to handle form submissions
    return render(request, 'publisher/dashboard/upload_files.html')

@csrf_exempt
def fetch_repo(request):
    """
    Proxy view: Frontend calls this -> Django calls GitIngest API -> Returns parsed files.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            repo_url = data.get('repo_url')
            
            # 1. Call GitIngest API
            api_url = "https://gitingest.com/api/ingest"
            payload = {
                "input_text": repo_url,
                "token": "",
                "max_file_size": "50",
                "pattern_type": "exclude",
                "pattern": ""
            }
            
            response = requests.post(api_url, json=payload)
            response_data = response.json()
            
            raw_content = response_data.get('content', '')
            
            # 2. Parse the raw text content into separate files
            # GitIngest separates files with: ================================================\nFILE: path/to/file\n================================================
            files = []
            
            # Regex to split content by the file separator
            # Captures the filename and the content following it
            pattern = r"={48}\nFILE: (.+?)\n={48}\n(.*?)(?=\n={48}\nFILE:|\Z)"
            matches = re.findall(pattern, raw_content, re.DOTALL)
            
            for filename, content in matches:
                # Filter: Only show JS and CSS files
                if filename.endswith('.js') or filename.endswith('.css'):
                    files.append({
                        'name': filename,
                        'content': content.strip(),
                        'lint_status': 'Passed' if 'error' not in content.lower() else 'Warning' # Simple mock logic
                    })

            return JsonResponse({'files': files, 'tree': response_data.get('tree')})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Placeholder views for other pages so links don't break
# publisher/views.py
def mapping_config(request):
    # Renders the Mapping Configuration page
    return render(request, 'publisher/dashboard/mapping_config.html')

# publisher/views.py
def publish(request):
    return render(request, 'publisher/dashboard/publish.html')

# publisher/views.py
def publish_log(request):
    return render(request, 'publisher/dashboard/publish_log.html')

# publisher/views.py
def settings(request):
    return render(request, 'publisher/dashboard/settings.html')




