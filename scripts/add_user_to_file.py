import json
import re
import argparse

regex = re.compile(r'^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$')


def get_emails(file):
    f = open(file)
    data = json.load(f)
    user_emails = data["email"]
    emails = user_emails.split(",")
    print(emails)
    f.close()
    return emails


def append_users(user_file, new_emails):
    f = open(user_file, "a")
    for email in new_emails:
        f.write(email.strip() + "\n")
        print(email.strip())
    #f.writelines("")
    f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('parsed_values', metavar='parsed_values', type=str,
                        help='json file from stefanbuck/github-issue-parser')
    parser.add_argument('user_file', metavar='user_file', type=str,
                        help='file name of the user list on the env')
    args = parser.parse_args()
    parsed_values_file = args.parsed_values
    user_file = args.user_file
    email_list = get_emails(parsed_values_file)
    append_users(user_file, email_list)


if __name__ == "__main__":
    main()
