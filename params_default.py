import logging

login_url = "https://prenotami.esteri.it/Services"
id_url = "https://prenotami.esteri.it/Services/Booking/74"
passport_url = "https://prenotami.esteri.it/Services/Booking/318"

id_check = True
passport_check = True
stop_on_success = True
check_interval_sec = 60

log_level = logging.INFO
log_format = '[%(asctime)s] %(message)s'
log_datefmt = '%m/%d/%Y %H:%M:%S'

email = "<your_username>"
password = "<your_password>"
pushbullet_token = None # optional access token for pushbullet notifications