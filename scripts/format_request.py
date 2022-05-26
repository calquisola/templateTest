import json
import re
import argparse

regex = re.compile(r'^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$')


def create_request_json(users, table_name, directory):
    req = {
      table_name: users
    }
    filename = '{0}/add_user.json'.format(directory)
    with open(filename, "w") as outfile:
        json.dump(req, outfile)

    return


def is_valid_email(email):
    if re.fullmatch(regex, email):
        return True

    return False


def parse_json(file, directory):

    f = open(file)
    data = json.load(f)
    user_emails = data["email"]
    environment = data["environment"]

    if environment == "Utility":
        table_name = "users_utility"
    else:
        table_name = "users"

    request_list = []

    emails = user_emails.split(",")

    for user_email in emails:
        obj = {
                "PutRequest": {
                  "Item": {
                      "email": {
                          "S": user_email.strip()
                      }
                    }
                  }
              }
        if is_valid_email(user_email.strip()):
            request_list.append(obj)

    create_request_json(request_list, table_name, directory)

    f.close()
    return


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('file', metavar='file', type=str,
                        help='json file from stefanbuck/github-issue-parser')

    parser.add_argument('directory', metavar='directory', type=str,
                        help='directory where output json will be saved')

    args = parser.parse_args()

    file = args.file
    # table = args.table
    directory = args.directory

    parse_json(file, directory)


if __name__ == "__main__":
    main()
