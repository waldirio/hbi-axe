# hbi-axe
This app will help you to retrieve some information from cloud.redhat.com that are not available at this moment via customer portal.

It's possible to
- List Duplicate Entries on HBI/Insights Inventory
- List Servers with different `display_name` and `Hostname`
- List Server with Last_Seen > X days
- List all the Hypervisors with at least 1 guest

Those information will be very useful during the troubleshooting process.

Let's start.

## ## Start Attention Point
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
## ## End Attention Point

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

User ....: user-account-here
Status ..: Not loaded yet

1. Load the data from cloud.redhat.com
2. List Duplicate Entries on HBI
3. List Servers with different `display_name` and `Hostname`
4. List Server with Last_Seen > X days
5. List all the Hypervisors with at least 1 guest


0. Exit
############################################################
Please, type the # related to your request:
```

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
fqdn,id,last_seen
(none),48a68387-8d8e-401d-b746-54d633544e8e,2021-05-26T00:37:20.301323+00:00
(none),63b3c52d-479b-4019-9113-c30fba205bbe,2021-05-20T00:33:54.164677+00:00
(none),8711d9e9-1cc1-43ba-b5da-faf1a88e67ee,2021-05-26T00:39:42.655086+00:00
ansible,0d57e738-8f2c-4c0d-aa38-4214084d162d,2021-05-26T00:11:31.769515+00:00
ansible,28bf2ab5-ce48-4291-9123-d0d3b7bfa9d4,2021-05-26T00:13:27.359815+00:00
ansible,38c3670f-c56e-473b-a5ef-ea52aac83aab,2021-05-26T00:42:29.167919+00:00
ansible-bastion,3f5a0952-2db9-4549-b69a-d2f433abd137,2021-05-24T00:31:41.294139+00:00
ansible-bastion,aee52062-da4a-498e-83f2-8283e09cb09b,2021-05-26T00:09:40.373904+00:00
ansible-bastion,e590b5c1-1b2b-42ac-91d4-1908a70dc705,2021-05-26T00:10:48.986680+00:00
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
display_name,fqdn,id
00bb66d7-0142-40fb-a52c-f690358998e8,None,00bb66d7-0142-40fb-a52c-f690358998e8
02269b27-52b1-4a33-88f3-fcf1e13ea200,None,02269b27-52b1-4a33-88f3-fcf1e13ea200
1f6941ff-4b60-4741-aaf7-49f69fd3d194,vm25-187.gsslab.pnq2.redhat.com,1f6941ff-4b60-4741-aaf7-49f69fd3d194
8530eefa-e5d4-425c-af2b-dd860bb93bd5,vm00-39.gsslab.pek2.redhat.com,8530eefa-e5d4-425c-af2b-dd860bb93bd5
8cc90245-ecdf-4e3b-995b-165579826c29,srv-mrg-67,8cc90245-ecdf-4e3b-995b-165579826c29
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
display_name,id,last_seen
(none),63b3c52d-479b-4019-9113-c30fba205bbe,2021-05-20 00:33:54
020e9808f91dc65275038f429a1a3d521f4c1b67.example.com,9eb45929-8b33-4a61-8a33-41af52af03ed,2021-05-22 11:47:47
02e4319a-04d8-4906-8572-f131a8294423,02e4319a-04d8-4906-8572-f131a8294423,2021-05-21 00:07:53
10bb781b-d9c9-4866-86a4-068cc2bc23cc,10bb781b-d9c9-4866-86a4-068cc2bc23cc,2021-05-19 00:07:45
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
```


I really hope this helps you.

If you need anything else of if you are facing issues trying to use it, please let me know.

waldirio@redhat.com / waldirio@gmail.com
