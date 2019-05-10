# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 18:58
# @Author  :
# ad属性 安全权限相关
from ldap3 import Connection,Server, ALL, MODIFY_REPLACE
from ldap3.protocol.microsoft import security_descriptor_control

from apps.securitytab import ldaptypes
from apps.securitytab.uuids import string_to_bin


ldap3RESTARTABLE = Connection(server=Server('', get_info=ALL, use_ssl=False), user='\\', password='', auto_bind=True)

def test():
    try:
        # Set SD flags to only query for DACL设置SD标志仅查询DACL
        controls = security_descriptor_control(sdflags=0x04)
        ldap3RESTARTABLE.search('DC=,DC=com', '(&(objectClass=user)(SAMAccountName=sdfsd112))', attributes=['SAMAccountName', 'nTSecurityDescriptor','objectSid'], controls=controls)
        entry = ldap3RESTARTABLE.entries[0]
        usersid = entry['objectSid'].value
        print(usersid)
        secDescData = entry['nTSecurityDescriptor'].raw_values[0]  # 默认权限
        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
        everyone = create_every_ace()
        secDesc['Dacl']['Data'].append(everyone)
        data = secDesc.getData()
        dn = entry.entry_dn
        # 修改权限
        modifynt = ldap3RESTARTABLE.modify(dn, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
        print(modifynt)
        return modifynt
    except Exception as e:
        print(e)


def test1():
    try:
        # Set SD flags to only query for DACL设置SD标志仅查询DACL
        controls = security_descriptor_control(sdflags=0x04)
        ldap3RESTARTABLE.search('DC=,DC=com', '(&(objectClass=user)(SAMAccountName=sdfsd112))', attributes=['SAMAccountName', 'nTSecurityDescriptor','objectSid'], controls=controls)
        entry = ldap3RESTARTABLE.entries[0]
        usersid = entry['objectSid'].value
        print(usersid)
        secDescData = entry['nTSecurityDescriptor'].raw_values[0]  # 默认权限
        secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR(data=secDescData)
        everyone = create_every_ace()
        Data = secDesc['Dacl']['Data']
        secDesc['Dacl']['Data'].remove(everyone)
        data = secDesc.getData()
        dn = entry.entry_dn
        # 修改权限
        modifynt = ldap3RESTARTABLE.modify(dn, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
        print(modifynt)
        return modifynt
    except Exception as e:
        print(e)

def checkdacl():
    controls = security_descriptor_control(sdflags=0x04)
    ldap3RESTARTABLE.search('DC=,DC=com', '(&(objectClass=user)(SAMAccountName=sdfsd112))', attributes=['SAMAccountName', 'nTSecurityDescriptor', 'objectSid'], controls=controls)
    entry = ldap3RESTARTABLE.entries[0]
    usersid = entry['objectSid'].value
    print(usersid)
    secDescData = entry['nTSecurityDescriptor'].raw_values[0]  # 默认权限
    dn = entry.entry_dn
    every_ace = create_every_ace()
    secDesc = ldaptypes.SR_SECURITY_DESCRIPTOR()
    secDesc.fromString(secDescData)

    for ace in secDesc['Dacl'].aces:
        Sid = ace['Ace']['Sid'].formatCanonical()
        Mask = ace['Ace']['Mask']['Mask']
        if Sid == 'S-1-1-0' and Mask == 65600:
            secDesc['Dacl']['Data'].remove(ace)
    data = secDesc.getData()
    modifynt = ldap3RESTARTABLE.modify(dn, {'nTSecurityDescriptor': (MODIFY_REPLACE, [data])}, controls=controls)
    print(modifynt)

    return 1



# Create an object ACE with the specified privguid and our sid
def create_every_ace():
    nace = ldaptypes.ACE()
    nace['AceFlags'] = 0
    nace['AceLen'] = 16
    nace['AceSize'] = 20
    nace['AceType'] = 1
    nace['TypeName'] = 'ACCESS_DENIED_ACE'
    acedata = ldaptypes.ACCESS_DENIED_ACE()
    acedata['Mask'] = ldaptypes.ACCESS_MASK()
    #acedata['Mask']['Mask'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ADS_RIGHT_DS_CONTROL_ACCESS
    acedata['Mask']['Mask'] = 65600
    #acedata['ObjectType'] = b''
    #acedata['InheritedObjectType'] = b''
    acedata['Sid'] = ldaptypes.LDAP_SID()
    acedata['Sid'].fromCanonical('S-1-1-0')
    assert 'S-1-1-0' == acedata['Sid'].formatCanonical()
    #acedata['Flags'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ACE_OBJECT_TYPE_PRESENT
    nace['Ace'] = acedata
    return nace


def create_object_ace_1(privguid, sid):
    nace = ldaptypes.ACE()
    nace['AceType'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ACE_TYPE
    nace['AceFlags'] = 0x00
    acedata = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE()
    acedata['Mask'] = ldaptypes.ACCESS_MASK()
    acedata['Mask']['Mask'] = 65600
    acedata['ObjectType'] = string_to_bin(privguid)
    acedata['InheritedObjectType'] = b''
    acedata['Sid'] = ldaptypes.LDAP_SID()
    acedata['Sid'].fromCanonical(sid)
    assert sid == acedata['Sid'].formatCanonical()
    acedata['Flags'] = ldaptypes.ACCESS_ALLOWED_OBJECT_ACE.ACE_OBJECT_TYPE_PRESENT
    nace['Ace'] = acedata
    return nace


