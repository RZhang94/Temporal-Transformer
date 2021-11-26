import os
import numpy as np

class struct:
    def __init__(self, title):
        struct.name = title
        struct.names = []
        struct.structures = []

    def addStruct(self, title, size):
        #Feed me structure data
        struct.names.append(title)
        struct.structures.append(size)

    def addStructs(self, structs):
        #Feed me tuples of strcuture in order
        for struct in structs:
            self.addStruct(struct[0], struct[1])\

    def print(self):
        # Check if loaded properly
        print('Structure Name: '+ self.name + ' ; ' + str(self.names))
        print('Structure sizes: ' + str(self.structures) +'\n')

def dataCheck(struct, dataTarget, printCheck = False):
    def indCheck(indData):
        if isinstance(indData, list):
            indSize = len(indData)
        else:
            indSize = indData.shape
        return indSize

    def checksubsize(subdata, ref):
        #Verify size of all points in subdata are consistent
        verification = True
        firstSize = indCheck(subdata[0])
        #print('First size: ' + str(firstSize))
        for i in range(0, ref):
            #print(str(i) + ' ' + str(indCheck(subdata[i])))
            if indCheck(subdata[i]) != firstSize:
                verification = False
        if verification:
            return firstSize
        else:
            return False

    def sizing(data):
        #Check sizes of everything in data and return them
        sizeVar = []
        n = indCheck(data)
        # print('Data Points: ' + str(n))
        for i in range(0,n[0]):
            sizeVar.append(checksubsize(data[i], n[1]))

        return(sizeVar)

    #Feed me data and the structure

    data = np.load(dataTarget, allow_pickle=True)
    data_size = sizing(data)
    verification = True
    # print('Data size: ' + str(data_size))
    # print('Structure Size: ' + str(struct.structures))
    for i in range(0, len(struct.structures)):
        # print(str(struct.structures[i])+ ' comp ' + str(data_size[i]))
        # print(str(type(struct.structures[i]))+ ' comp ' + str(type(data_size[i])))
        if struct.structures[i] != data_size[i]:
            verification = False
    if printCheck:
        print('Data Target: ' + dataTarget)
        print('Verification of ' + str(data[0][0][0]) + ' ' + str(data[0][0][1]) +' : ' + str(verification))
    return verification

def subjectCheck(directory, structure):
    entries = []
    listdir = os.listdir(directory)
    print('Checking directory :' + str(directory))
    # print(len(listdir))
    for a in listdir:
        if a != 'desktop.ini':
            target = os.path.join(directory, a)
            res = dataCheck(structure, target)
            if res:
                entries.append(target)
    return entries


#Develop data structure to test
hmr2struct = struct("hmr2")
hmr2struct.addStructs([('Tags', 3), ('Joints', (21,2)), ('Joints3d', (21, 3)), ('Poses', (24, 3, 3)), ('Shape', (10,)) ])
hmr2struct.print()

#Input test data
# test = r'D:\.shortcut-targets-by-id\1LHR8VsKK7PJk9cbF-zygVbPqE_zejDMB\Cropped Images\HMR Outputs\S1\desktop.ini'
# dataCheck(hmr2struct, test, printCheck= True)

#Test folder
folder = r'D:\.shortcut-targets-by-id\1LHR8VsKK7PJk9cbF-zygVbPqE_zejDMB\Cropped Images\HMR Outputs\S9'
b = subjectCheck(folder, hmr2struct)
print(b)
print(len(b))


