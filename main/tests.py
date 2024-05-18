from django.test import TestCase

# Create your tests here.
from ldap3 import Server, Connection, ALL

class DCConnection():

    server = Server("WINDC0001.mshome.net", use_ssl=False, get_info=ALL)

    conn = Connection(server, 'cn=admin1,cn=users,dc=mydomain,dc=com', 'Secret123', auto_bind=True)
    # connection test user
    # need to relate connection to login(session)
    # no TLS config applied yet
    
    conn.search('cn=users,dc=mydomain,dc=com', '(objectclass=person)')
    
    # output: [CN=admin1,CN=Users,DC=mydomain,DC=com]
    ls = conn.entries[0]
