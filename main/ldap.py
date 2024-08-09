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


# can not install django ldap(python-ldap), some s* requires too much time
# to do: make class based on below and learn to code it yourself I guess
# can build from scratch I think with ldap3

AUTH_LDAP_BIND_DN = "cn=admin1,cn=users,dc=mydomain,dc=com"
AUTH_LDAP_BIND_PASSWORD = "Secret123"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=MyDomain,dc=mydomain,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=Groups,ou=MyDomain,dc=mydomain,dc=com", ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")
AUTH_LDAP_MIRROR_GROUPS = True

# Populate the Django user from the LDAP directory.
AUTH_LDAP_REQUIRE_GROUP = "cn=SG-Domain-ADM-ADManagement_site,ou=Groups,ou=MyDomain,dc=mydomain,dc=com"

AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
        "username": "uid",
        "password": "userPassword",
}
AUTH_LDAP_PROFILE_ATTR_MAP = {
        "home_directory": "homeDirectory"
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        #"is_active": "cn=active,ou=groups,dc=example,dc=com",
        "is_staff": "cn=SG-Domain-ADM-ADManagement_site,ou=Groups,ou=MyDomain,dc=mydomain,dc=com",
        #"is_superuser": "cn=superuser,ou=groups,dc=example,dc=com"
}
    
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_TIMEOUT = 3600
    
AUTH_LDAP_FIND_GROUP_PERMS = True
    
    # Keep ModelBackend around for per-user permissions and maybe a local
    # superuser.
AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
)