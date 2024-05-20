from django.test import TestCase

# Create your tests here.
from ldap3 import Server, Connection, ALL
import json

class DCConnection():

    server = Server("WINDC0001.mshome.net", use_ssl=False, get_info=ALL)

    conn = Connection(server, 'cn=admin1,cn=users,dc=mydomain,dc=com', 'Secret123', auto_bind=True)
    # connection test user
    # need to relate connection to login(session)
    # no TLS config applied yet
    
    conn.search('cn=users,dc=mydomain,dc=com', '(objectclass=person)')
    # output: [CN=admin1,CN=Users,DC=mydomain,DC=com]

    # specify attr, will use on user page
    # output is sorted alfabetically by key
    conn.search('cn=users,dc=mydomain,dc=com', '(&(objectclass=person)(cn=admin1))', attributes=['accountExpires', 'description', 'displayName','lastLogon', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName'])
    
    entry = conn.entries[0].entry_to_json()
    
    # json converts class to dictionary
    entry_dict = json.loads(entry)
