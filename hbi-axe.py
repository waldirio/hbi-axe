#!/usr/bin/env python
"""
# File ....: hbi-axe.py
# Date ....: 05.25.2021
# Author ..: Waldirio M Pinheiro <waldirio@redhat.com> / <waldirio@gmail.com>
# Purpose .:
#   This script will collect the information from cloud.redhat.com/Inventory and
#   will put in a nice/simple view the whole information. At this moment, the
#   features available here are not available on cloud.redhat.com as well.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
"""

from os import system
import getpass
import json
import sys
from optparse import OptionParser
import requests
from time import sleep
from datetime import datetime, timedelta

systemdata = []
duplicate_list = []
diff_display_name_fqdn_list = []
last_seen_list = []
hyper_list = []

DUPLICATE_ENTRIES_LOG = "/tmp/hbi_duplicate_entries.log"
DIFFERENT_NAMES_LOG = "/tmp/hbi_different_names.log"
LAST_SEEN_LOG = "/tmp/hbi_last_seen.log"
HYPERVISOR_LIST_LOG = "/tmp/hbi_hypervisor_with_guest_list.log"

def process_info(login, password, server):
    """
    Function responsible for collect and process the main info regarding
    to the Content Hosts on cloud.redhat.com
    """

    global systemdata

    systemdata = []
    url = 'https://' + server + '/api/inventory/v1/hosts'
    result = requests.get(url, auth=(login, password)).content
    jsonresult = json.loads(result)

    page = 0
    per_page = 100
    # For debugging purposes
    # per_page = 5
    while (page == 0 or int(jsonresult['per_page']) == len(jsonresult['results'])):
    # For debugging purposes
    # while (page < 5):
        page += 1
        url = "https://cloud.redhat.com/api/inventory/v1/hosts?page=" + str(page) + "&per_page=" + str(per_page)
        print(url)
        result = requests.get(url, auth=(login, password)).content
        jsonresult = json.loads(result)
        systemdata += jsonresult['results']

    print("Loaded {} entries from your account.".format(len(systemdata)))
    input("press any key to continue")


def hypervisor_guests():
    """
    Function responsible to identify all the hypervisors "virt-who-" and then
    compare the full list against the hypervisor list. The main idea is to map
    which Content Host is running on top of which hypervisor.
    """

    global hyper_list
    hyper_list_local = []
    local_temp_list = []

    print("Please, this process can spend some time once we are checking all the hypervisors")
    for ch in systemdata:
        if 'virt-who-' in ch['display_name']:
            display_name = ch['display_name']
            satellite_id = ch['satellite_id']
            id = ch['id']
            last_seen = ch['updated']

            url = 'https://' + server + '/api/rhsm-subscriptions/v1/hosts/' + satellite_id + '/guests?limit=100&offset=0'

            result = requests.get(url, auth=(login, password)).content
            jsonresult = json.loads(result)

            num_of_guests = len(jsonresult['data'])

            if (num_of_guests != 0):
                local_temp_list.append(id)
                local_temp_list.append(display_name)
                local_temp_list.append(num_of_guests)
                local_temp_list.append(last_seen)

                hyper_list_local.append(local_temp_list)
                local_temp_list = []

    for b in hyper_list_local:
        id = b[0]
        display_name = b[1]
        num_of_guests = b[2]
        last_seen = b[3]

        url = 'https://' + server + '/api/inventory/v1/hosts/' + id + '/system_profile'

        result = requests.get(url, auth=(login, password)).content
        jsonresult = json.loads(result)

        try:
            real_number_of_sockets = jsonresult['results'][0]['system_profile']['number_of_sockets']
            if ((real_number_of_sockets % 2) != 0):
                number_of_sockets = real_number_of_sockets + 1
            else:
                number_of_sockets = real_number_of_sockets
        except KeyError:
            number_of_sockets = "no number of sockets key"

        local_temp_list.append(id)
        local_temp_list.append(display_name)
        local_temp_list.append(num_of_guests)
        local_temp_list.append(number_of_sockets)
        local_temp_list.append(last_seen)
        hyper_list.append(local_temp_list)
        local_temp_list = []

    with open(HYPERVISOR_LIST_LOG, "w") as file_obj:
        file_obj.write("id,display_name,number_of_guests,number_of_sockets,last_seen\n")

        for b in hyper_list:
            id = b[0]
            display_name = b[1]
            number_of_guests = b[2]
            number_of_sockets = b[3]
            last_seen = b[4]

            file_obj.write(str(id) + "," + str(display_name) + "," + str(number_of_guests) + "," + str(number_of_sockets) + "," + str(last_seen) + "\n")

    print("The file {} was created with the hypervisors that have at least 1 guest.".format(HYPERVISOR_LIST_LOG))
    print("Were found {} entries on your environment.".format(len(hyper_list)))
    input("press any key to see the content of the file")
    system("less " + HYPERVISOR_LIST_LOG)
    input("press any key to continue")


def list_duplicated_entries():
    global duplicate_list
    local_temp_list = []
    aux = []

    print("This process can spend some time ...")
    for elements in systemdata:
        display_name = elements['display_name']
        id = elements['id']

        for others in systemdata:
            others_display_name = others['display_name']
            others_id = others['id']
            last_seen = others['updated']

            if display_name == others_display_name and id != others_id:
                # Adding duplicate to the list
                local_temp_list.append(display_name)
                local_temp_list.append(others_id)
                local_temp_list.append(last_seen)

                aux.append(local_temp_list)
                local_temp_list = []

                duplicate_list.append(aux)

    duplicate_list = [list(x) for x in set(tuple(x) for x in aux)]
    duplicate_list.sort()

    with open(DUPLICATE_ENTRIES_LOG, "w") as file_obj:
        file_obj.write("fqdn,id,last_seen\n")

        for b in duplicate_list:
            fqdn = b[0]
            id = b[1]
            last_seen = b[2]

            file_obj.write(str(fqdn) + "," + str(id) + "," + last_seen + "\n")

    print("The file {} was created with the duplicate entries of your environment.".format(DUPLICATE_ENTRIES_LOG))
    print("Were found {} duplicated entries on your environment.".format(len(duplicate_list)))
    input("press any key to see the content of the file")
    system("less " + DUPLICATE_ENTRIES_LOG)
    input("press any key to continue")


def list_diff_display_name_fqdn_entries():
    global diff_display_name_fqdn_list
    local_temp_list = []
    aux = []

    print("This process can spend some time ...")
    for elements in systemdata:
        display_name = elements['display_name']
        fqdn = elements['fqdn']
        id = elements['id']
        if display_name != fqdn:
            local_temp_list.append(display_name)
            local_temp_list.append(fqdn)
            local_temp_list.append(id)
            aux.append(local_temp_list)
            local_temp_list = []

    diff_display_name_fqdn_list = [list(x) for x in set(tuple(x) for x in aux)]
    diff_display_name_fqdn_list.sort()

    with open(DIFFERENT_NAMES_LOG, "w") as file_obj:
        file_obj.write("display_name,fqdn,id\n")
        # print("fqdn,id,last_seen")

        for b in diff_display_name_fqdn_list:
            display_name = b[0]
            fqdn = b[1]
            id = b[2]

            file_obj.write(display_name + "," + str(fqdn) + "," + str(id) + "\n")

    print("The file {} was created with the duplicate entries of your environment.".format(DIFFERENT_NAMES_LOG))
    print("Were found {} entries on your environment with different `display_name` and `hostname`.".format(len(diff_display_name_fqdn_list)))
    input("press any key to see the content of the file")
    system("less " + DIFFERENT_NAMES_LOG)
    input("press any key to continue")


def list_servers_last_seen():
    today = datetime.now()
    num_of_days = input("Enter the number of days ago: ")
    new_date = today - timedelta(days=int(num_of_days))

    global last_seen_list
    local_temp_list = []
    aux = []

    print("This process can spend some time ...")
    for elements in systemdata:
        display_name = elements['display_name']
        id = elements['id']
        last_seen = elements['updated'][:19]

        new_last_seen = datetime.strptime(last_seen, '%Y-%m-%dT%H:%M:%S')

        if new_last_seen < new_date:
            local_temp_list.append(display_name)
            local_temp_list.append(id)
            local_temp_list.append(new_last_seen)
            aux.append(local_temp_list)
            local_temp_list = []

    list_servers_last_seen = [list(x) for x in set(tuple(x) for x in aux)]
    list_servers_last_seen.sort()

    with open(LAST_SEEN_LOG, "w") as file_obj:
        file_obj.write("display_name,id,last_seen\n")

        for b in list_servers_last_seen:
            display_name = b[0]
            id = b[1]
            last_seen = b[2]

            file_obj.write(str(display_name) + "," + str(id) + "," + str(last_seen) + "\n")

    print("The file {} was created with the old entries of your environment.".format(LAST_SEEN_LOG))
    print("Were found {} old entries on your environment.".format(len(list_servers_last_seen)))
    input("press any key to see the content of the file")
    system("less " + LAST_SEEN_LOG)
    input("press any key to continue")


def main_menu():
    SLEEP_TIME = 1
    status = ""

    while True:
        if (len(systemdata) == 0):
            status = "Not loaded yet"
        else:
            status = "Ready to go"

        system("clear")
        print("############################################################")
        print("### Red Hat/SysMgmt/CEE")
        print("")
        print("User ....:", login)
        print("Status ..: {}".format(status))
        print("")
        print("1. Load the data from cloud.redhat.com")
        print("2. List Duplicate Entries on HBI")
        print("3. List Servers with different `display_name` and `Hostname`")
        print("4. List Server with Last_Seen > X days")
        print("5. List all the Hypervisors with at least 1 guest")
        print("")
        print("")
        print("0. Exit")
        print("############################################################")
        print("Please, type the # related to your request: ", end="")
        opc = input()

        if (opc == "1"):
            process_info(login, password, server)
        elif (opc == "2"):
            list_duplicated_entries()
        elif (opc == "3"):
            list_diff_display_name_fqdn_entries()
        elif (opc == "4"):
            list_servers_last_seen()
        elif (opc == "5"):
            hypervisor_guests()
        elif (opc == "0"):
            print("Closing the application")
            sys.exit()
        else:
            print("please, type a valid option")
            sleep(SLEEP_TIME)


if __name__ == "__main__":

    default_server = "cloud.redhat.com"
    default_login = ""
    default_password = ""

    parser = OptionParser()
    parser.add_option("-l", "--login", dest="login", help="Login user", metavar="LOGIN", default=default_login)
    parser.add_option("-p", "--password", dest="password", help="Password for specified user. Will prompt if omitted", metavar="PASSWORD", default=default_password)
    parser.add_option("-s", "--server", dest="server", help="FQDN of server - omit https://", metavar="SERVER", default=default_server)
    (options, args) = parser.parse_args()

    if not(options.login and options.server):
        print("Must specify at least login.  See usage:")
        parser.print_help()
        print("\nExample usage: ./hbi-axe.py -l username")
        sys.exit(1)
    else:
        login = options.login
        password = options.password
        server = options.server

    if not(options.login and options.server):
        print("Must specify at least login.  See usage:")
        parser.print_help()
        print("\nExample usage: ./hbi-axe.py -l admin")
        sys.exit(1)
    else:
        FILEINPUTMODE = False

    login = options.login
    password = options.password
    server = options.server

    if not (FILEINPUTMODE or password):
        password = getpass.getpass("%s's password:" % login)

    # Testing the credentials
    url = 'https://' + server + '/api/inventory/v1/hosts'
    result = requests.get(url, auth=(login, password))
    if result.ok:
        pass
    else:
        print("wrong credentials, please try again.")
        sys.exit()

    main_menu()

    # TODO
    # print("3. Delete Duplicate Entries")
    # print("5. Delete Entries where the 3 type of name differ")
    # print("7. Delete Server with Last_Seen > X days")
    # print("8. Generate a report with all the available fields")
