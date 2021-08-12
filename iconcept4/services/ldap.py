from ldap3 import Server, Connection, ALL



# Check user authentication in the LDAP and return his information
def get_LDAP_user(username, password,LdapConnectionUrl,LdapAuthenticationDomain,LdapUserDn):
    LDAP_URL = ''+LdapConnectionUrl+''
    username=username
    print('username:',username)
    try:
        server = Server(LDAP_URL, get_info=ALL)
        connection = Connection(server,
                                'uid={username},DC=wemabank,DC=local'.format(
                                    username=username),
                                password, auto_bind=True)

        connection.search(''+LdapUserDn+'', '({attr}={login})'.format(
            attr='uid', login=username), attributes=['cn'])

        if len(connection.response) == 0:
            return None

        return connection.response[0]
    except:
        return None