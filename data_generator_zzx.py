from itertools import zip_longest
import numpy as np
import random
import torch

def get_frame_num(frame_name):
    l = frame_name.split('_')

    m = l[1].split('.')
    n = m[0]
    frame_num = int(n)
    return frame_num


def get_j_neighbor(dataset, central_idx, one_side, j, S, video, central_frame_num):
    # subject = []
    if dataset[central_idx + j][0][0] == S:
        if dataset[central_idx - 1][0][1] == video:

            # extract the frame number
            frame_name = dataset[central_idx + j][0][2]
            frame_num = get_frame_num(frame_name)
            if frame_num == central_frame_num + 20*j:

                ##########################
                '''change here to revise the input data'''
                # make pose for an example
                subject = dataset[central_idx + j][3]
            else:
                subject = dataset[central_idx][3]
                print('the ', j,  'of frame', central_frame_num, 'not found')
        
        else:
            subject = dataset[central_idx][3]
            print('the ', j,  'of frame ', central_frame_num, 'not found')
    else:
        subject = dataset[central_idx][3]
        print('the ', j,  'of frame ', central_frame_num, 'not found')
    return subject


class Dataloader_zzx:
    def __init__(self, dataset, batch_size=512, receptive_field=9):
        # dataset = np.transpose(dataset, (1,0))    # not needed for the newly formed trainingdata
        self.tol_num_data = len(dataset)
        self.batch_size = batch_size
        self.n_batches = self.tol_num_data // self.batch_size
        self.receptive_field = receptive_field
        self.dataset = dataset
        self.one_side = receptive_field // 2      # how many frames to search in one side
    
    def generator(self):
        print("dividing data......")
        for i in range(self.n_batches):
            # local batch and labels
            indices = random.sample(range(0,self.tol_num_data), self.batch_size)
            central_images = self.dataset[indices]      # retrieve data by raws
            one_side = self.one_side

            current_batch = []
            subject = []
            # generate the data from an single frame and combine them together.
            for i, img in enumerate(central_images):

                # import pdb
                # pdb.set_trace()

                S, video, frame = img[0]        # Ex: S = 'S1', video = 'Posing 1.54138969', frame = 'frame_201.jpg'
                central_frame_num = get_frame_num(frame)
                # get the location of the central frame in the dataset.
                central_idx = indices[i]

                # repeat the central frame if can't find the neighbor frames.
                if central_idx <= self.one_side or central_idx >= self.tol_num_data - self.one_side:
                    '''change here'''
                    subject_central = img[3]
                    subject = [subject_central] * self.one_side * 2   # repeat the element for 2*one_side times.
                    print('******************', len(subject))
                    subject_np = subject[0]
                    print(len(subject), '\n', central_frame_num)
                    for frame_np in subject[1:]:
                        subject_np = np.vstack([subject_np, frame_np])
                    
                    current_batch.append(subject_np)

                    subject = [] #set subject clear
                    
                    print('get neighbors for', central_frame_num,'\n', '####################')

                    continue
                    # break
                
                # generate the sequence list: the left and right of the central frame
                else:
                    for j in [x for x in range(-self.one_side, 0)] + [x+1 for x in range(0, self.one_side)]:    # without the central frame
                        subject.append(get_j_neighbor(self.dataset, central_idx, self.one_side, j, S, video, central_frame_num))

                

                # convert the list (len(6)) to array that is (6*)   (85)*9 -> (9,85)
                # stack list elements as row in numpy.array
                subject_np = subject[0]
                print(len(subject), '\n', central_frame_num)
                for frame_np in subject[1:]:
                    subject_np = np.vstack([subject_np, frame_np])
                
                current_batch.append(subject_np)

                subject = [] #set subject clear
                
                print('get neighbors for', central_frame_num,'\n', '####################')



            # convert the list to numpy (9,85) -> (512,9,85)
            batch_np = current_batch[0]
            batch_np = np.expand_dims(batch_np, axis=0)
            for bundle in current_batch[1:]:
                bundle = np.expand_dims(bundle, axis=0)
                batch_np = np.vstack([batch_np, bundle])



            # numpy -> tensor
            training_set_batch = torch.from_numpy(batch_np)
            yield training_set_batch      # yield the result