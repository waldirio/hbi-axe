## hbi-axe
This app will help you to retrieve some information from cloud.redhat.com that are not available at this moment via customer portal.

# Table of Contents
1. [Available Features](#available_feature)
2. [Running without virtual environment](#running_without_venv)
3. [Running with virtual environment](#running_with_venv)
4. [Some Outputs](#some_outputs)
5. [Contact Here](#contact_here)


## available_feature

It's possible to
- List Duplicate Entries on HBI/Insights Inventory
- List Servers with different `display_name` and `Hostname`
- List Server with Last_Seen > X days
- List all the Hypervisors with at least 1 guest
- Remove entries on cloud.redhat.com

Those information will be very useful during the troubleshooting process.

[back to top](#hbi-axe)
## running_without_venv

If you have python 3 and two additional packages on your system, `python3-urllib3` and `python3-requests`, virtual environment is not required, instead you can just download the script and use it. Simple like that! :-)

```
# python <tab> <tab>
python                python2.7             python2.7-pasteurize  python3.6             python3-chardetect    
python2               python2.7-futurize    python3               python3.6m            
```
Here we can see we have python 2 and python 3, and when checking the version
```
# python3 --version
Python 3.6.8
```
and here we can see the packages
```
# rpm -qa | grep -E '(python3-urllib3|python3-requests)'
python3-urllib3-1.25.11-1.el7pc.noarch
python3-requests-2.24.0-1.el7pc.noarch
```
Note. On this way, you are good to go.

That said, let's proceed
```
# wget https://raw.githubusercontent.com/waldirio/hbi-axe/master/hbi-axe.py
# python3 hbi-axe.py
```
then you should be able to see something as below
```
# python3 hbi-axe.py 
Must specify at least login.  See usage:
Usage: hbi-axe.py [options]

Options:
  -h, --help            show this help message and exit
  -l LOGIN, --login=LOGIN
                        Login user
  -p PASSWORD, --password=PASSWORD
                        Password for specified user. Will prompt if omitted
  -s SERVER, --server=SERVER
                        FQDN of server - omit https://

Example usage: ./hbi-axe.py -l username
```

If you face any kind of issue on the procedure above, please proceed with the steps below in order to create a virtual environment and execute it.

[back to top](#hbi-axe)
## running_with_venv

First, let's create the virtual environment using python 3.6
```
# python3.6 -m venv ~/.virtualenv/hbi-axe
```
Now let's clone the project and access the directory
```
# git clone https://github.com/waldirio/hbi-axe.git
# cd hbi-axe/
```
At this moment, let's activate the virtual environment
```
# source ~/.virtualenv/hbi-axe/bin/activate
(hbi-axe) [root@wallsat69 hbi-axe]#
```
This step will be necessary just once, we will upgrade the pip
```
(hbi-axe) [root@wallsat69 hbi-axe]# pip install --upgrade pip
```
and install some requirements. Don't worry, this will be real quick and will not change your environment, everything will be installed under the virtual environment `hbi-axe`
```
(hbi-axe) [root@wallsat69 hbi-axe]# pip install -r requirement 
```
Great. Now, we are ready to go! As you can see below, you can pass the username and password.
```
(hbi-axe) [root@wallsat69 hbi-axe]# ./hbi-axe.py 
Must specify at least login.  See usage:
Usage: hbi-axe.py [options]

Options:
  -h, --help            show this help message and exit
  -l LOGIN, --login=LOGIN
                        Login user
  -p PASSWORD, --password=PASSWORD
                        Password for specified user. Will prompt if omitted
  -s SERVER, --server=SERVER
                        FQDN of server - omit https://

Example usage: ./hbi-axe.py -l username
(hbi-axe) [root@wallsat69 hbi-axe]#
```
Once you pass only the username, the password will be requested and here we are!
```
(hbi-axe) [root@wallsat69 hbi-axe]# ./hbi-axe.py -l user-account-here
user-account-here's password:



############################################################
### Red Hat/SysMgmt/CEE

User ....: rhn-support-wpinheir
Status ..: Not loaded yet

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request:
```

[back to top](#hbi-axe)
## some_outputs

The initial step will be select 1 to load the information. At this moment, the app will connect to cloud.redhat.com using your credential and will collect the whole data about the servers from Inventory.


`List Duplicate Entries on HBI` will present the duplicated entries or servers with the same `display_name`
```
############################################################
### Red Hat/SysMgmt/CEE

User ....: user-account-here
Status ..: Ready to go

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request: 2
This process can spend some time ...
The file /tmp/hbi_duplicate_entries.log was created with the duplicate entries of your environment.
Were found 1317 duplicated entries on your environment.
press any key to see the content of the file
```

Below an example
```
id,display_name,last_seen
033519f3-2e29-4574-bad3-2cb9ea2714fd,561f7d69fec4a3b6eb3d0f5cb1967d92f35db8ba.example.com,2021-05-12T02:54:54.041303+00:00
37b83eec-e15a-4620-943c-87ce2314f06a,561f7d69fec4a3b6eb3d0f5cb1967d92f35db8ba.example.com,2021-05-20T02:55:13.343192+00:00
57614925-e980-4fe7-8288-b38819daa278,746916acb8efbd3f6b402326565c22ca46f7384d.example.com,2021-06-03T02:56:59.457510+00:00
a2efc986-2012-4910-a620-7eaa89a1c0ac,746916acb8efbd3f6b402326565c22ca46f7384d.example.com,2021-06-07T02:57:00.555070+00:00
678be3ac-dfa2-45f2-af76-fe8c17a23a1c,Fresh,2021-06-07T00:28:42.089450+00:00
fdd11be4-2465-415e-8a75-f03e37017d18,Fresh,2021-06-03T00:10:23.462133+00:00
...
```


`List Servers with different 'display_name' and 'Hostname'` will present the entries that are presenting divergence in the `Hostname` and `Display_Name`
```
############################################################
### Red Hat/SysMgmt/CEE

User ....: user-account-here
Status ..: Ready to go

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request: 3
This process can spend some time ...
The file /tmp/hbi_different_names.log was created with the duplicate entries of your environment.
Were found 836 entries on your environment with different `display_name` and `hostname`.
press any key to see the content of the file
```
Below an example
```
id,display_name,fqdn,last_seen
006328f8-b3c3-4809-92b7-ecead62c9c15,dhcp16-225-6.fs.lab.eng.bos.redhat.com,smayhew-rhel8.fs.lab.eng.bos.redhat.com,2021-06-05T00:36:16.833456+00:00
00bb66d7-0142-40fb-a52c-f690358998e8,00bb66d7-0142-40fb-a52c-f690358998e8,None,2021-06-07T00:28:44.293885+00:00
014b7c22-f05a-4c73-91bd-910a46ea2932,starSRV,starSRV.eng.pek2.redhat.com,2021-06-07T17:47:15.811742+00:00
02269b27-52b1-4a33-88f3-fcf1e13ea200,02269b27-52b1-4a33-88f3-fcf1e13ea200,None,2021-06-07T00:26:19.060785+00:00
023a2c78-ceac-47d0-9395-171e030ab686,dhcp-1-181-206.sd.lab.cee.rdu2.redhat.com,rhdstest.testidmlaab.com,2021-06-07T00:33:51.587852+00:00
026ed2e2-2ca1-4161-bbef-c13eed26235a,026ed2e2-2ca1-4161-bbef-c13eed26235a,None,2021-06-07T00:41:52.092614+00:00
02a1576b-2b9e-4889-81a4-635285c1b18e,02a1576b-2b9e-4889-81a4-635285c1b18e,None,2021-06-07T00:40:48.314607+00:00
02a45e42-fd8c-4ca4-b496-7c1057812481,stux79,stuxn82,2021-06-03T00:08:24.881861+00:00
...
```

`List Server with Last_Seen > X days` will present all the servers that `last_seen` or `last update` is greater than `X` days
```
############################################################
### Red Hat/SysMgmt/CEE

User ....: user-account-here
Status ..: Ready to go

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request: 4
Enter the number of days ago: 2
This process can spend some time ...
The file /tmp/hbi_last_seen.log was created with the old entries of your environment.
Were found 2206 old entries on your environment.
press any key to see the content of the file
```
Below an example
```
id,display_name,last_seen
e1365f3b-7821-4bae-a317-356d6a8ee7fb,rhel8.void,2021-06-06 12:53:59
650b36df-ebb3-4b5a-a77c-a5e539108f6d,loadbalancer.openincite.net,2021-06-06 00:40:57
1d435c45-0b0d-44a9-8e0e-858b04c65653,realm,2021-06-06 00:40:30
0a5c8bca-b901-4a1e-8219-1c0dcd6dc9cb,crcqe-jenkins-slave-rhel79-48,2021-06-06 00:39:33
32bce224-d6fb-4610-94f4-c3a20b38549d,lappy.redhat.lab.home,2021-06-06 00:39:33
158ce088-f409-4f46-a06e-2414ca40f348,node1.openshift.local,2021-06-06 00:37:22
6fd2ddb7-b45b-42a3-936e-9c8168492d73,rhel7.madebug.net,2021-06-06 00:37:21
...
```

`List all the Hypervisors with at least 1 guest` will present all the hypervisors that are presenting `host-guest mapping` and has at least 1 guest on top of it.
```
############################################################
### Red Hat/SysMgmt/CEE

User ....: user-account-here
Status ..: Ready to go

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request: 5
Please, this process can spend some time once we are checking all the hypervisors
The file /tmp/hbi_hypervisor_with_guest_list.log was created with the hypervisors that have at least 1 guest.
Were found 20 entries on your environment.
press any key to see the content of the file
```
Below an example
```
id,display_name,number_of_guests,number_of_sockets,last_seen
77747c3f-9a2a-4cd2-923b-52db2d905050,virt-who-nuc1.local.lan-1,5,2,2021-05-25T22:54:04.047140+00:00
4dae819f-7aec-4772-8b7f-d41c9c35e4a9,virt-who-bdt-tnf-esx-node04-1,1,2,2021-05-25T19:36:21.675017+00:00
711a0749-a09c-49b4-8aa7-1760a212b2d0,virt-who-esxi4.lab.eng.rdu2.redhat.com-1,1,4,2021-05-25T19:22:56.047952+00:00
64d4f02f-98ec-4a60-b8af-2fa1393be37a,virt-who-satotest.gsslab.brq2.redhat.com,100,2,2021-05-17T08:41:27.467423+00:00
de59402d-94da-4cfb-ad49-5cfe2bdf676a,virt-who-titan.cluster.local-1,7,2,2021-04-21T12:55:29.371771+00:00
6a33b34a-3ec0-4517-bcfd-9768a5bc436a,virt-who-fred.usersys.redhat.com-1,1,2,2021-04-20T23:57:31.767382+00:00
...
```

`Remove entries` on cloud.redhat.com will remove some entries based on a local file that will be specified by the customer
```
############################################################
### Red Hat/SysMgmt/CEE

User ....: rhn-support-wpinheir
Status ..: Ready to go

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest
9. Remove entries on cloud.redhat.com

0. Exit
############################################################
Please, type the # related to your request: 9
## This section will allow you to remove some entries on cloud.redhat.com
In order to proceed, you can inform the file which contain the entries that you would like to remove.
Note, you can use the files generated by the previous entries, edit to keep the entries that you would
like to remove. If you would like to remove all the entries from the file, just keep the file as is.
press any key to continue

Would you like to proceed now? (Y/N): y
Please, type the file path: /tmp/hbi_server_to_be_removed
Are you sure that you would like to proceed? (Y/N): y

The file /tmp/hbi_deleted_entries.csv was created with the deleted entries of your environment.
Were deleted 4 entries from your environment.
press any key to see the content of the file
```
Here is the content of `/tmp/hbi_server_to_be_removed`
```
$ cat /tmp/hbi_server_to_be_removed 
id,display_name,fqdn,last_seen
cfe80122-9e32-46bb-9b57-821d5a34fe85,srv01.example.com,03 Jun 2021 19:24 UTC
b4038a36-8987-456d-819c-0d2b5bd72759,srv02.example.com,03 Jun 2021 19:24 UTC
```

And below an example of the output
```
$ cat /tmp/hbi_deleted_entries.csv
uuid,Removed,status_code
cfe80122-9e32-46bb-9b57-821d5a34fe85,False,404
b4038a36-8987-456d-819c-0d2b5bd72759,True,202
```
Note. Above we can see some servers that weren't removed `404` because they are not present anymore and also we can see `202`, on this case the entry was removed successfuly.



[back to top](#hbi-axe)
## contact_here

I really hope this helps you.

If you need anything else of if you are facing issues trying to use it, please let me know.

waldirio@redhat.com / waldirio@gmail.com

[back to top](#hbi-axe)