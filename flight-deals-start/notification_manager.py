import requests
import smtplib
from twilio.rest import Client


TWILIO_ACCOUNT_SID = YOUR_TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = YOUR_TWILIO_AUTH_TOKEN
USER_SHEETY_ENDPOINT = YOUR_USERS_SHEETY_ENDPOINT
MY_EMAIL = YOUR_EMAIL
MY_PASSWORD = YOUR_PASSWORD



class NotificationManager:
    def notification(self,message, stop_overs=0, via_city=""):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        if stop_overs == 0:
            message = client.messages.create(
                body=message,
                from_="+14252305384",
                to="+923218322229"
            )
            print(message.status)
        else:
            message = client.messages.create(
                body=message,
                from_="+14252305384",
                to="+923218322229"
            )
            print(message.status)

    def send_email(self, message, link):
        response = requests.get(url=USER_SHEETY_ENDPOINT)
        data = response.json()["users"]
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            for email_addr in data:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email_addr["email"],
                    msg=f"Subject:Low Price Alert!\n\n{message}\n{link}"
                )

