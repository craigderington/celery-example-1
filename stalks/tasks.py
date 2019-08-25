from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
import random
import requests
from requests.auth import HTTPBasicAuth
import config

# setup our celery object
app = Celery(__name__,
             broker=config.CELERY_BROKER_URL,
             backend=config.CELERY_RESULT_BACKEND)

# setup our task logger
logger = get_task_logger(__name__)

messages = [
    "I am Locutus of Borg.  Resistence if Futile.",
    "Dude, where's my car?",
    "Send me your tired, your hungry and your poor",
    "Celery for the Win!"
]

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, get_random_users, name="Get Random Users Every Minute")
    sender.add_periodic_task(120.0, generate_ips, name="Generate IP Address for Geolocation")
    sender.add_periodic_task(300.0, get_date, name="Log Date Every 5 Minutes.")
    sender.add_periodic_task(
        crontab(), # log every minute
        get_message,
    )


@app.task
def get_random_users():
    """ Get a list of random users """
    API_METHOD = "GET"
    URL = "https://randomuser.me/api/?nat=us&results=5000"
    hdr = {"content-type": "application/json", "user-agent": "SimplePythonFoo()"}
    counter = 0

    try:
        r = requests.request(API_METHOD, URL, headers=hdr)
        if r.status_code == 200:
            resp = r.json()

            for item in resp["results"]:
                title = item["name"]["title"]
                fname = item["name"]["first"]
                lname = item["name"]["last"]
                logger.info("Discovered New User: {} {} {}".format(title, fname, lname))
                show_user.delay(title, fname, lname)
                counter += 1
        else:
            # log the http status code
            logger.info("Get Random Users API call returned HTTP status code: {}".format(str(r.status_code)))

    except requests.HTTPError as http_err:
        logger.critical(str(http_err))

    return counter


@app.task
def show_user(title, fname, lname):
    """ Show the user from the API call """
    person = "{} {} {}".format(title, fname, lname)
    logger.info("{}".format(person))
    return person


@app.task
def log(msg):
    logger.info(msg)
    return random.randint(1000, 10000)


@app.task
def get_date():
    """ Return the date as a string """
    return datetime.now().strftime("%c")


@app.task
def get_message():
    """ Get a random message for the console """
    msg = random.choice(messages)
    logger.info("{}".format(str(msg)))
    return str(msg)


@app.task
def generate_ips():
    """ Task Producer to GeoLocate IP addresses """
    # ignore first octet in rfc1918
    rfc1918 = [10, 127, 172, 192]

    try:
        for i in range(50):
            ip = get_random_ip()
            if ip.split(".")[0] not in rfc1918:
                geolocate.delay(ip)
            else:
                logger.info(
                    "Unable to Geolocate IP Address: {}".format(str(ip))
                )
    
    except ValueError as err:
        logger.info("Generate IP Addresses - Error: {}".format(str(err)))


def get_random_ip():
    """
    Create a random IP address
    :return: ipv4 address
    """
    return ".".join(str(random.randrange(1, 255)) for i in range(4))


@app.task
def geolocate(ip):
    """ Geolocate the IP address """
    API_METHOD = ["GET", "POST"]
    IPINFO_URL = "http://ip-api.com/json/" + ip
    hdr = {"content-type": "application/json", "user-agent": "SimplePythonFoo()"}

    try:
        r = requests.request(
            API_METHOD[0],
            IPINFO_URL,
            headers=hdr
        )

        if r.status_code == 200:
            resp = r.json()
            logger.info(resp)
        else:
            logger.info("Geolocate API called returned HTTP Status Code: {}".format(str(r.status_code)))

    except requests.HTTPError as http_err:
        logger.info("Geolocate API call returned HTTP Error: {}".format(str(http_err)))

    return ip


@app.task
def verify_email(email):
    """ Verify an email address using Neutrino API """
    API_METHOD = ["GET", "POST"]
    NEUTRINO_RESOURCE = "email-validate"
    params = {"email": email, "fix-typos": "True"}
    hdr = {
        "content-type": "application/json",
        "api-key": config.NEUTRINO_API_KEY,
        "user-id": config.NEUTRINO_API_USERNAME
    }
    
    try:
        r = requests.request(
            API_METHOD[1],
            config.NEUTRINO_API_URL + NEUTRINO_RESOURCE,
            headers=hdr,
            params=params
        )

        if r.status_code == 200:
            resp = r.json()
            logger.info(resp)
        else:
            logger.info("Neutrino API HTTP Status Code: {}".format(str(r.status_code)))
    
    except requests.HTTPError as http_err:
        logger.info("Neutrino API HTTP Error: {}".format(str(http_err)))

    return email
