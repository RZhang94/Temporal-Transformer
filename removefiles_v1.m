%Utility to quicly filter out a bunch of images from
%convert_mask_to_rop_v3.m

clc; clear;
%Find all files
folder = 'S7' ;%SET TARGET FOLDER HERE
directory = append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\',folder,'\ImCropped')
list = dir(directory);
list = struct2cell(list);
targets = list(1,:); %Should remove the '.' and _'all'
targets = targets (3:end);

%Filtered ImCropped
directorytarget = append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\',folder,'\ImCroppedFilt')

% targets = {'Test'}; %overwrite


for a = 1:size(targets,2)
   subdir = append(directory, '\', targets{1,a});
   
   sublist = dir(subdir);
   sublist = struct2cell(sublist);
   subtargets = sublist(1,:);
   subtargets = subtargets(3:end);
   
   mkdir(append(directorytarget, '\', targets{1,a}))
   
   for b = 1:size(subtargets,2)
       string = split(subtargets{1,b}, '_');
       string = string{2,1};
       string2 = split(string, '.');
       string2 = string2{1,1};

       if mod(str2double(string2)-1,20) == 0
           source = append(subdir, '\', subtargets{1,b});
           dest = append(directorytarget, '\', targets{1,a}, '\', subtargets{1,b});
           status = copyfile(source, dest);
       end
           
       
   end
           

end
