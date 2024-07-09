Traceback (most recent call last):
  File "C:\Users\Lusix\Desktop\Coding\Python\LibraSync\main.py", line 62, in <module>
    load(creds)
  File "C:\Users\Lusix\Desktop\Coding\Python\LibraSync\main.py", line 41, in load
    results = service.files().list(q=f"name={DATA_FILE}").execute()
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lusix\Desktop\Coding\Python\LibraSync\.env\Lib\site-packages\googleapiclient\_helpers.py", line 130, in positional_wrapper
    return wrapped(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Lusix\Desktop\Coding\Python\LibraSync\.env\Lib\site-packages\googleapiclient\http.py", line 938, in execute
    raise HttpError(resp, content, uri=self.uri)
googleapiclient.errors.HttpError: <HttpError 400 when requesting https://www.googleapis.com/drive/v3/files?q=name%3Ddata.db&alt=json returned "Invalid Value". Details: "[{'message': 'Invalid Value', 'domain': 'global', 'reason': 'invalid', 'location': 'q', 'locationType': 'parameter'}]">