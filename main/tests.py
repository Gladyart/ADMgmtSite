from django.test import TestCase


# Create your tests here.
from ldap3 import Server, Connection, ALL


class DCConnection():

    server = Server("WINDC0001", use_ssl=False, get_info=ALL)

    conn = Connection(server, 'cn=admin1,cn=users,dc=mydomain,dc=com', 'Secret123', auto_bind=True)
    # connection test user
    # need to relate connection to login(session)
    # no TLS config applied yet
    
    #conn.search('cn=users,dc=mydomain,dc=com', '(objectclass=person)')
    # output: [CN=admin1,CN=Users,DC=mydomain,DC=com]
    
    userID = 'admin1'
    OUPath = 'cn=users,dc=mydomain,dc=com'
    searchParameters = f'(&(objectclass=person)(cn={userID}))'
    # specify attr, will use on user page
    # output is sorted alfabetically by key
    ## for later:
    # searchParameters = f'(&(objectclass=person)(cn=*{searched}*))'
    # searchParameters = f'(&(givenName={firstName}*)(mail=*@example.org))'

    conn.search(OUPath, searchParameters, 
                attributes=['accountExpires', 'description', 'displayName','lastLogon', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName'])
        
    entry = conn.entries[0]



    
