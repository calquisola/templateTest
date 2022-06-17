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


def format_aws_json(emails):
    request_list = []
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
        request_list.append(obj)
    return request_list


def get_added_emails(file):
    emails = []
    f = open(file, 'r')
    for line in f:
        # check if the first char is +
        if line[0] == '+':
            details = line.split('+')
            if is_valid_email(details[1]):
                emails.append(details[1])
    f.close()
    return emails


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('file', metavar='file', type=str,
                        help='file with git changes')

    parser.add_argument('db_name', metavar='db_name', type=str,
                        help='dynamodb table name')

    parser.add_argument('directory', metavar='directory', type=str,
                        help='directory where output json will be saved')

    args = parser.parse_args()

    file = args.file
    table = args.db_name
    directory = args.directory

    emails = get_added_emails(file)
    aws_json_data = format_aws_json(emails)
    create_request_json(aws_json_data, table, directory)


if __name__ == "__main__":
    main()
