from ldap3 import Server, Connection, ALL
from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE

server = Server("WINDC0001", use_ssl=False, get_info=ALL)

conn = Connection(server, 'cn=admin1,cn=users,dc=mydomain,dc=com', 'Secret123', auto_bind=True)
# connection test user
# need to relate connection to login(session)
# no TLS config applied yet

conn.search('cn=users,dc=mydomain,dc=com', '(objectclass=person)')
conn.entries
# output: [CN=admin1,CN=Users,DC=mydomain,DC=com]

# create user test

conn.add('cn=user1,cn=users,dc=mydomain,dc=com', attributes={'objectClass':  ['inetOrgPerson', 'posixGroup', 'top'], 
                                                             'sn': 'user_sn', 
                                                             'gidNumber': 0
                                                             })

# modify user test
conn.modify('cn=user1,cn=users,dc=mydomain,dc=com',
         {'description': [(MODIFY_REPLACE, ['description-replaced'])],
          'sn': [(MODIFY_REPLACE, ['sn-replaced'])]
          })