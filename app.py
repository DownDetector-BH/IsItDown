#!/usr/bin/env python3
"""
Is It Down? - Website Status Checker
Network connectivity testing application
"""

import os
import subprocess
import re
import urllib.parse
from flask import Flask, request, render_template, flash, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change_me_in_production'

# Security configuration
BLOCKED_KEYWORDS = [
    'rm', 'del', 'format', 'dd', 'mv', 'cp', 'chmod', 'chown',
    '&&', '||', ';', '>', '>>', '|', '$', '`'
]

def apply_filter(user_input):
    """Apply security filtering to user input"""
    # Keyword filtering for security
    filtered_input = user_input.lower()
    
    for keyword in BLOCKED_KEYWORDS:
        if keyword in filtered_input:
            raise ValueError(f"Blocked keyword detected: {keyword}")
    
    # Pattern validation
    if re.search(r'[;&|$`]', user_input):
        raise ValueError("Special characters not allowed")
        
    return user_input

def execute_curl(target):
    """Execute curl command to check target connectivity"""
    try:
        # Apply security filtering on raw input
        filtered_target = apply_filter(target)
        
        # URL decode after filtering
        decoded_target = urllib.parse.unquote(filtered_target)
        
        # Add protocol if not present
        if not decoded_target.startswith(('http://', 'https://')):
            decoded_target = f"http://{decoded_target}"
        
        # Execute curl command with minimal output
        # -s: silent mode (no progress bar)
        # -S: show errors
        # -L: follow redirects  
        # --max-time: timeout
        # --max-redirs: maximum redirects
        # -w: custom output format (only show what we need)
        # -o: output to /dev/null (don't show page content)
        # see the css file line 93 :)
        command = f'curl -s -S -L --max-time 10 --max-redirs 5 -w "Status: %{{http_code}}\\nTotal time: %{{time_total}}s\\nFinal URL: %{{url_effective}}\\n" -o /dev/null {decoded_target}'
        
        # Run the curl command
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        
        # Parse curl output to determine success
        is_successful = False
        http_code = None
        
        # Extract HTTP status code from output
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.startswith('Status:'):
                    try:
                        http_code = int(line.split(':')[1].strip())
                        # Consider 2xx and 3xx as successful
                        is_successful = 200 <= http_code < 400
                        break
                    except (ValueError, IndexError):
                        pass
        
        # If no HTTP code found but curl succeeded (return code 0), consider it successful
        if result.returncode == 0 and http_code is None:
            is_successful = True
        
        return {
            'success': True,
            'command': command,
            'output': result.stdout,
            'error': result.stderr,
            'return_code': result.returncode,
            'is_site_up': is_successful,
            'http_code': http_code
        }
        
    except ValueError as e:
        return {
            'success': False,
            'error': str(e),
            'output': '',
            'command': ''
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Command timed out after 15 seconds',
            'output': '',
            'command': ''
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Unexpected error: {str(e)}",
            'output': '',
            'command': ''
        }

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html', difficulty_mode='medium')

@app.route('/check', methods=['POST'])
def check_status():
    """Check website status endpoint"""
    target = request.form.get('target', '').strip()
    
    if not target:
        flash('Please enter a target to check!', 'error')
        return render_template('index.html')
    
    # Log the request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Checking target: {target}")
    
    # Execute curl command
    result = execute_curl(target)
    
    return render_template('result.html', 
                         target=target, 
                         result=result)



@app.route('/about')
def about():
    """About page with hints"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Development server (don't use in production!)
    app.run(host='0.0.0.0', port=5000, debug=True)