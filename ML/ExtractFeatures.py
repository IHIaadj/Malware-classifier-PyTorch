# Run all apk in test folder 
import os
import zipfile
import subprocess
import pkg_resources
from xml.etree import ElementTree as ET

PERMISSIONS_LIST = []


def ObtainPermissionList():
    resource_package = __name__
    resource_path = '/'.join(('', 'PERMISSION_LIST'))

    Xall_path = pkg_resources.resource_filename(resource_package, resource_path)
    file = open(Xall_path, "r")
    global PERMISSIONS_LIST
    for line in file : 
        line = line.split('\n')[0]
        a = line.split('.')
        PERMISSIONS_LIST.append(a[2])
       

def ExtractingManifest(name) : 
    try : 
        file_zip = zipfile.ZipFile(name)
    except : 
        print(name)
    file_zip.extract('AndroidManifest.xml', '.') 
    file_zip.close()

def GetManifestXML(): 
    resource_package = __name__
    resource_path = '/'.join(('', 'AXMLPrinter2.jar'))

    Xall_path = pkg_resources.resource_filename(resource_package, resource_path)
    result = subprocess.run(["java", "-jar",Xall_path,"AndroidManifest.xml"], stdout=subprocess.PIPE)
    os.remove("AndroidManifest.xml")

    return result.stdout.decode("utf-8", 'replace')

def permissionExtract(AndroidManifest):
    permission = []
    try : 
        root = ET.fromstring(AndroidManifest)
    except : 
        f = open("error.txt", "w+")
        f.write(AndroidManifest)
    permissions = root.findall("uses-permission")

    for perm in permissions :
        for att in perm.attrib:
            value = str(perm.attrib[att]).split('.')
            permission.append(value[len(value)-1])
    #print(permission)
    return permission

def CreatePermissionVector(permission):
    permissionVector = [0] * 396
    print("**************************************" + str((len(PERMISSIONS_LIST) + 1)) + "****************************")
    for perm in permission :
        try :
            permissionVector[PERMISSIONS_LIST.index(perm)] = 1 
        except :
            print('OK')
    return permissionVector 

def Extract(filename):
    ObtainPermissionList()
    ExtractingManifest(filename)
    return CreatePermissionVector(permissionExtract(GetManifestXML()))