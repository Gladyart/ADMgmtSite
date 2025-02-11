from ldap3 import Server, Connection, ALL
from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE


userID = 'Admin'

userAttributes = ['accountExpires', 'badPwdCount', 'cn','description', 'displayName', 'distinguishedName', 'GivenName', 'HomeDirectory', 'HomeDrive', 'lastLogon', 'lockoutTime', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName', 'sn', 'userAccountControl']

server = Server("192.168.0.17", use_ssl=False, get_info=ALL)

OUPath = 'OU=users,OU=MyDomain,dc=mydomain,dc=com'

conn = Connection(server, f'cn={userID},{OUPath}', 'Secret123', auto_bind=True)

class DCConnection():

    server = Server("192.168.0.17", use_ssl=False, get_info=ALL)
    
    OUPath = 'OU=users,OU=MyDomain,dc=mydomain,dc=com'

    conn = Connection(server, f'cn={userID},{OUPath}', 'Secret123', auto_bind=True)


    

    # connection test user
    # no TLS config applied yet

    def connectADServer(userID, server=server, OUPath=OUPath):
        conn = Connection(server, f'cn={userID},{OUPath}', 'Secret123', auto_bind=True)

        return conn
    
    #conn.search('cn=users,dc=mydomain,dc=com', '(objectclass=person)')
    # output: [CN=gladyart,CN=Users,DC=mydomain,DC=com]
    
    
    searchParameters = f'(&(objectclass=person)(cn={userID}))'
    # specify attr, will use on user page
    # output is sorted alfabetically by key
    ## for later:
    # searchParameters = f'(&(objectclass=person)(cn=*{searched}*))'
    # searchParameters = f'(&(givenName={firstName}*)(mail=*@example.org))'

    conn.search(OUPath, searchParameters, attributes=userAttributes)
    # other attr: Enabled, PasswordExpired, MemberOf, 
        
    entry = conn.entries[0]

    #isLocked = entry.lockoutTime.raw_values[0].decode('utf-8') # any output != 0 is locked

    def searchADPerson(self):
        searchParameters = f'(&(objectclass=person)(cn={self}))'
        conn.search(OUPath, searchParameters, attributes=userAttributes)
        entry = conn.entries[0]
        
        return entry

class ADUser(DCConnection):

    def __init__(self, id, *args):
        
        entry = ADSearch.searchADPerson(id)
        self.accountExpires = entry.accountExpires
        self.description = entry.description
        self.displayName = entry.displayName
        self.distinguishedName = entry.distinguishedName            
        self.lastLogon = entry.lastLogon
        if entry.lockoutTime == None:
            ADUser.unlockUser(self)
            self.lockoutTime = ""
            self.lockoutTimeRaw = 0
        else:
            self.lockoutTime = entry.lockoutTime
            self.lockoutTimeRaw = int(entry.lockoutTime.raw_values[0].decode('utf-8'))
        if entry.mail == None:
            self.mail = ""
        else:
            self.mail = entry.mail
        if entry.manager == None:
            self.manager = ""
        else:
            self.manager = ADSearch.searchManager(entry.manager)
        self.pwdLastSet = entry.pwdLastSet
        self.pwdLastSetRaw = int(entry.pwdLastSet.raw_values[0].decode('utf-8'))
        self.sAMAccountName = entry.sAMAccountName
        self.userAccountControl = entry.userAccountControl


    def unlockUser(self):
        conn.modify(f'{self.distinguishedName}',
                    {'lockoutTime': [(MODIFY_REPLACE, [0])]})

    # 512=Enabled, 514=Disabled, 66048=Enable/PassNoExpire, 66050=Disable/PassNoExpire    
    def enableUser(self):
        if self.userAccountControl == 514:
            conn.modify(f'{self.distinguishedName}',
                        {'userAccountControl': [(MODIFY_REPLACE, [512])]})
        elif self.userAccountControl == 66050:
            conn.modify(f'{self.distinguishedName}',
                        {'userAccountControl': [(MODIFY_REPLACE, [66048])]})

    def disableUser(self):
        if self.userAccountControl == 512:
            conn.modify(f'{self.distinguishedName}',
                        {'userAccountControl': [(MODIFY_REPLACE, [514])]})
        elif self.userAccountControl == 66048:
            conn.modify(f'{self.distinguishedName}',
                        {'userAccountControl': [(MODIFY_REPLACE, [66050])]})
    

class ADSearch(DCConnection):
    
    def searchManager(DN):
        searchParameters = f'(&(objectclass=person)(distinguishedName={DN}))'
        conn.search(OUPath, searchParameters, attributes=userAttributes)
        entry = conn.entries[0]
        
        return entry
    
    def searchADPerson(id):
        searchParameters = f'(&(objectclass=person)(cn={id}))'
        conn.search('OU=users,OU=MyDomain,dc=mydomain,dc=com', searchParameters, attributes=userAttributes)
        entry = conn.entries[0]
        
        return entry

# import AD users to SQL db via LDAP 
'''
import sqlite3 


con = sqlite3.connect("db.sqlite3") 

cur = con.cursor() 

AUTH_LDAP_USER_SEARCH = "ou=MyDomain,dc=mydomain,dc=com" 

searchParameters = '(objectclass=person)' 

conn.search(AUTH_LDAP_USER_SEARCH, searchParameters, attributes=['accountExpires', 'description', 'displayName','lastLogon', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName']) 
listOfUsers = conn.entries 

# manual db import 

# this method didn't work well before, also found out that passing fstrin is not very secure here so need to rebuild into list like import parameters instead
for user in listOfUsers: 

    cur.execute(f"INSERT INTO main_user VALUES ({user.accountExpires}, {user.description}, {user.displayName}, {user.lastLogon}, {user.mail}, {user.manager}, {user.pwdLastSet}, {user.sAMAccountName})") 
    con.commit()    

#====
#DJ ldap conversion to basic ldap below

# server = Server("WINDC0001", use_ssl=False, get_info=ALL)

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
'''