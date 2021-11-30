import os
import numpy as np

#Check consistency and sizing of the all HMR output numpyp arrays.
#Check the indexing is correct.

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
        # print(subdata)
        # print(subdata[0])
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
    if printCheck:
        print('Data Target: ' + dataTarget)
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
        print('Verification of ' + str(data[0][0][0]) + ' ' + str(data[0][0][1]) +' : ' + str(verification))
    return verification

def subjectCheck(directory, structure, printCh = False):
    entries = []
    listdir = os.listdir(directory)
    print('Checking directory :' + str(directory))
    print(len(listdir))
    for a in listdir:
        check = a.split('.')
        if check[-1] == 'npy':
            target = os.path.join(directory, a)
            res = dataCheck(structure, target, printCheck= printCh)
            if res:
                entries.append(target)
    return entries

def sum(data):
    print(len(data))
    print(data.shape)
    return

# #Develop data structure to test
# hmr2struct = struct("hmr2 struct 1")
# hmr2struct.addStructs([('Tags', 3), ('Joints', (21,2)), ('Joints3d', (21, 3)), ('Poses', (24, 3, 3)), ('Shape', (10,))])
# hmr2struct.print()

# hmr2struct = struct("hmr2 struct 2")
# hmr2struct.addStructs([('Tags', 3), ('Joints', (21,2)), ('Joints3d', (21, 3)), ('PoseShape', (82,)), ('Camera', (3,)) ])
# hmr2struct.print()

hmr2gtstruct = struct("hmr2 struct 2gt")
hmr2gtstruct.addStructs([('Tags', 3), ('Joints', (21,2)), ('Joints3d', (21, 3)), ('PoseShape', (82,)), ('Camera', (3,)) , ('JointsGT', (17,2)), ('Joints3dGT', (17, 3)) ])
hmr2gtstruct.print()



#Input test data
# test = r'D:\.shortcut-targets-by-id\1LHR8VsKK7PJk9cbF-zygVbPqE_zejDMB\Cropped Images\S11\Directions 1.58860488_results.npy'
#
# dataCheck(hmr2struct, test, printCheck= True)
# data = np.load(test, allow_pickle=True)
# # sum(data[0])
# sum(data[1][0])
# sum(data[2][0])
# sum(data[3][0])
# sum(data[4][0])

# debug = r'D:\.shortcut-targets-by-id\1LHR8VsKK7PJk9cbF-zygVbPqE_zejDMB\Cropped Images\HMR Outputs\Structure 2\S5\Discussion 2.58860488_results.npy'
# de = np.load(debug, allow_pickle=True)
# print('True')

#Test folder
folders = ['S1', 'S5', 'S6', 'S7', 'S8', 'S9', 'S11']

for folder in folders:
    target = r'D:\.shortcut-targets-by-id\1LHR8VsKK7PJk9cbF-zygVbPqE_zejDMB\Cropped Images\HMR Outputs\Structure 2_gt'
    target = os.path.join(target, folder)
    print('Target: ' + target)
    b = subjectCheck(target, hmr2gtstruct, printCh= False)
    print('Entries Verified: ' + str(len(b)))

