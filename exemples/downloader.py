#!python
import os
from argparse import ArgumentParser
from datetime import datetime
from email.mime.base import MIMEBase
from logging import DEBUG
from os import makedirs
from os.path import isdir, join
from traceback import format_exc

from gmail import GMail, Message

from lbpscrapper.scrapper import LBP

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("user")
    parser.add_argument("passw")
    parser.add_argument("download_dir")
    parser.add_argument("gmail_user")
    parser.add_argument("gmail_password")
    parser.add_argument("mail_receiver")
    args = parser.parse_args()

    log_folder = "logs"
    if not isdir(log_folder):
        makedirs(log_folder)
    log_file = join(log_folder, datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.txt"))
    log_file = os.path.abspath(log_file)

    try:
        with LBP(args.user, args.passw, headless=False, download_dir=args.download_dir, log_file=log_file,
                 log_level_console=DEBUG) as s:
            s.login()
            accounts = s.parse_accounts()
            s.go_to_e_releves()
            releves = s.ereleves
            for r in releves:
                s.download_releve_if_not_downloaded(r, accounts)
        raise ValueError("toto")
    except Exception as e:
        # Send error by mail
        tb = format_exc()
        main_content = "Le contenu de l'erreur est ci-joint\n%s %s\n%s" % (e.__class__.__name__, str(e), tb)
        gmail = GMail(args.gmail_user, args.gmail_password)
        msg = Message(subject="Error on LBP parser", to=args.mail_receiver,
                      text=main_content,
                      attachments=[MIMEBase('application', 'unknown'), log_file])
        gmail.send(msg)
        gmail.close()
