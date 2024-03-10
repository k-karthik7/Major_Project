import os
import hashlib
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

def verify_hash(generated_hash_values,verification_path):
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
                print("File verification failed! Hash values do not match.")

source_path=r"C:\Users\DELL\Desktop\arunkumar.txt"
dest_path=r"C:\Users\DELL\Desktop\hash.txt"
verify_hash(generatehash(source_path),dest_path)