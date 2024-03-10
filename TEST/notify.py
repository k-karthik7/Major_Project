from win11toast import toast #In win11toast, value of DEFAULT_APP_ID in line 13 was changed as per my requirements 

button = [
    {'activationType': 'protocol', 'arguments': 'file:///C:/Windows/Media', 'content': 'Open Folder'}
]

toast('Integrity Alert!', 'Your files are changed, consider verifying them.', buttons=button)