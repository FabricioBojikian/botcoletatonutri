from datetime import datetime

def log_error(message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")