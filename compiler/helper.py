import os
import json
import requests
import concurrent.futures
import base64, re

API_KEY = '20f53137c4msha170c6335a05594p1fa7cejsn248140d97f6f'
API_URL = 'https://judge0-ce.p.rapidapi.com/submissions/'

headers = {
    'Content-Type': 'application/json',
    'X-RapidAPI-Key': API_KEY,
}

def submit_code(source_code, language_id, input):
    data = {
        'source_code': base64.b64encode(source_code.encode()).decode('utf-8'),
        'language_id': language_id,
        'stdin': base64.b64encode(input.encode()).decode('utf-8'),
        'base64_encoded': True
    }
    response = requests.post(API_URL, json=data, headers=headers)
    response_data = response.json()
    try:
        token = response_data['token']
    except KeyError:
        token = None
    return token

def decode_base64_in_string(input_str):
    # Regex to find base64 encoded strings
    base64_pattern = re.compile(r"'([A-Za-z0-9+/=]+)'")
    
    def decode_match(match):
        base64_str = match.group(1)
        try:
            decoded_bytes = base64.b64decode(base64_str)
            decoded_str = decoded_bytes.decode('utf-8')
            return f"'{decoded_str}'"
        except Exception as e:
            # If there's an error in decoding, return the original string
            return match.group(0)
    
    # Substitute all base64 encoded parts with their decoded counterparts
    decoded_str = base64_pattern.sub(decode_match, input_str)
    
    return decoded_str

def get_submission_result(token):
    GET_URL = f"https://judge0-ce.p.rapidapi.com/submissions/{token}/?base64_encoded=true"
    response = requests.get(GET_URL, headers=headers)
    result = response.json()
    if result.get("stdout"):
        result["stdout"] = base64.b64decode(result["stdout"]).decode('utf-8')
    if result.get("stderr"):
        result["stderr"] = base64.b64decode(result["stderr"]).decode('utf-8')
    if result.get("compile_output"):
        result["compile_output"] = decode_base64_in_string(result["compile_output"])
    return result

def process_testcase(test_case, language_id, source_code):
    try:
        token = submit_code(source_code, language_id, test_case["input"])
        result = get_submission_result(token)
        return result
    except Exception as e:
        return {"error": str(e)}

def code_compiler(source_code, language_id, test_cases):
    results = []
    for test in test_cases:
        result = process_testcase(test, language_id, source_code)
        results.append(result)
    status_ = []
    error_ = None
    outputs = []
    times = []
    memory_list = []

    for result in results:
        if result.get("status"):
            status_.append(result["status"].get("description"))
        if result.get("compile_output") and error_ != result["compile_output"]:
            error_ = result["compile_output"]
        if result.get("stdout"):
            outputs.append(result["stdout"])
        if result.get("time"):
            times.append(result["time"])
        if result.get("memory"):
            memory_list.append(result["memory"])

    if len(test_cases) == status_.count("Accepted"):
        full_code_status = "Accepted"
    else:
        full_code_status = status_[-1] if status_ else "Error"

    response = {
        "status_list": status_,
        "full_code_status": full_code_status,
        "error_": error_,
        "memory": memory_list,
        "time": times,
        "outputs": outputs
    }
    print(response)
    return response

def get_language():
    headers = {
        'X-RapidAPI-Key': API_KEY,
    }
    
    def get_supported_languages():
        if os.path.exists('languages.txt'):
            with open('languages.txt', 'r') as file:
                data = file.read()
                if data:
                    return json.loads(data)
        
        response = requests.get("https://judge0-ce.p.rapidapi.com/languages", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            with open('languages.txt', 'w') as file:
                file.write(json.dumps(data))
            return data
        else:
            return "API call failed"
    
    return get_supported_languages()
