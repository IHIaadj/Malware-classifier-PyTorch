from . import ExtractFeatures

ObtainPermissionList()
# Get the list of files 
arr = os.listdir("./dataset/malwares")
datasetFile = open("datasetFile.txt", "a")

for f in arr : 
    permissionVector = Extract("dataset/malwares/"+f)
    permissionVector[len(permissionVector)-1] = 1
    datasetFile.write(str(permissionVector[0]))
    for i in range(1,len(permissionVector)):
        datasetFile.write(',' + str(permissionVector[i]) )
    datasetFile.write('\n')

datasetFile.close()