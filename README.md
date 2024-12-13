# Automatic sending of emails to subscribers, targeted by category

This project facilitates the automation of sending emails with thematic news to a list of subscribers. The code allows processing and classifying news obtained from Google alerts according to categories. In its current version, it classifies the news into two groups: "electoral" and "non-electoral". However, it is planned to make the system more flexible, so that the user can add an indefinite number of categories.

For sending and processing the emails, a Gmail account is used that automatically forwards the news to a Yandex account, from which the email is accessed via IMAP for analysis. Due to limitations in sending emails from Yandex via code, Brevo is used as the email distribution platform.

The project is designed to run on Google Colab, allowing its use by users on corporate networks with administrative restrictions and without additional installation permissions.

## Usage

1. Subscribe to Google News on [Google Alerts](https://www.google.com/alerts?source=alertsmail).
2. Create an account on Yandex and get the API KEY. Follow the guide on [Yandex app API KEY](https://yandex.com/support/id/en/authorization/app-passwords.html).
3. Create an account on Brevo and get the API KEY. Follow the guide on [Brevo API KEY](https://developers.brevo.com/docs/getting-started).
4. Go to [Google Colab](https://colab.research.google.com/) and create a new notebook.
5. Copy and paste the following code into a new entry in the created notebook:
```
import os, sys, subprocess
from google.colab import drive

project_path = '/content/drive/MyDrive/envio_de_mails/v2.0'
main_path = os.path.join(project_path, 'main.py')

if not os.path.exists(project_path):
    os.makedirs(project_path, exist_ok=True)

if not os.path.isdir('/content/drive'):
    drive.mount('/content/drive')

if not os.path.isfile(main_path):
    subprocess.run(['git', 'clone', 'https://github.com/TobiasCoding/focused-subscriber-emails-by-topic.git', project_path])

    for file_name in os.listdir(project_path):
        source = os.path.join(project_path, file_name)
        destination = os.path.join(project_path, file_name)
        if os.path.isdir(source):
            os.rename(source, destination)

    print("Installing dependencies... plase wait")
    for library in ["pytz", "sib-api-v3-sdk", "matplotlib"]:
        try:
            __import__(library)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

    print("Please, config the keys.json and build_databases.py files")
else:
    !python $main_path
```
6. Run the code: Click on the code portion and then Ctrl + Enter.
7. Modify the `keys.json` code to define your email and API KEYs obtained.
8. Configure the `build_databases.py` file located in the `databases` directory according to your preferences. And set your mail address linked with Brevo in `send_mails.py` and `send_statistics.py`.
9. Run the code: Click on the code portion and then Ctrl + Enter.

**Option Selection**: During execution, you will be able to choose options such as:
- Send electoral or non-electoral emails.
- Send to specific recipients or perform tests.

**Sending Emails**: After selecting the options, the emails will be sent automatically according to the recipients and categories configured in `build_databases.py`.

## Example of an email sent
![image](https://github.com/user-attachments/assets/ab944b07-8246-428b-9856-e6226d7d771f)

---
Developed by tobiasrimoli@duck.com
