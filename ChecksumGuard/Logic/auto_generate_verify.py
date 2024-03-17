import os
import hashlib
from win11toast import toast #In win11toast, value of DEFAULT_APP_ID in line 13 was changed as per my requirements 

def generatehash(path):
    checked_algorithms=['SHA512', 'MD5']
    if path:
        hash_values = []
        if os.path.isfile(path):
            for i in checked_algorithms:
                hash_value = generate_hash(path, algorithm=i)
                hash_values.append(f"Hash value ({i}): {hash_value}")
            print(hash_values)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    for i in checked_algorithms:
                        hash_value = generate_hash(file_path, algorithm=i)
                        hash_values.append(f"Hash value ({i}) for '{file_path}': {hash_value}")
            print(hash_values)
        return hash_values
def generate_hash(file_path, algorithm="", buffer_size=65536):
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        buffer = file.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(buffer_size)
    return hasher.hexdigest()

def verify_hash(generated_hash_values,verification_path, original_path):
    if generated_hash_values:
        if verification_path:
            verification_hash_values = []
            with open(verification_path, 'r') as verification_file:
                verification_hash_values = verification_file.read().splitlines()
            print(verification_hash_values)
            match = any(item in verification_hash_values for item in generated_hash_values)
            if match:
                print("File verification successful! Hash values match.")
            else:
                directory_path = os.path.dirname(original_path)
                button = [{'activationType': 'protocol', 'arguments': 'file:///{}'.format(directory_path), 'content': 'Open Folder'}]
                toast('Integrity Alert!', 'Your files are changed, consider verifying them.', buttons=button)
                print("File verification failed! Hash values do not match.")

try:
    with open("config.txt", "r") as file:
        lines=file.readlines()
        values={}
        for line in lines:
            key, value=line.strip().split(": ")
            values[key]=value
except Exception as e:
    print(e)

print(values['Original File/Folder Path'])
print(values['Hash Values Path'])
source_path=values['Original File/Folder Path']
dest_path=values['Hash Values Path']
verify_hash(generatehash(source_path),dest_path, source_path)