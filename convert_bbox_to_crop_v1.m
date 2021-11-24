clf; clc; clear;
%Find all files
list = dir('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S8\MySegmentsMat\ground_truth_bb')
list = struct2cell(list);
targets = list(1,:); %Should remove the '.' and _'all'
targets = targets (3:end-8)
for i = 1:size(targets,2)
    str = targets{1,i};
    str = str(1:end-4);
    targets{1,i} = str;
    
end

% for index = 97:size(targets,2)
for index = 40:size(targets,2)  

name = targets{1,index};
mkdir(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S8\ImCropped\',name))
data = importdata(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S8\MySegmentsMat\ground_truth_bb\', name ,'.mat'));
%Upload video and retrieve the relevant cdata for projection
video= mmread(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S8\Videos\',name,'.mp4'))
analyzeframes = video.frames;
frame_tot = min(size(analyzeframes,2),size(data,2));

fpi = 5;
images = floor(frame_tot/fpi)-1;

for a = 1:fpi:images*fpi
    frame_n = a;
    
    singleframe = data(1,frame_n); %Isolate frame
    
    analyzeframe = analyzeframes(frame_n).cdata;
    
%     image(analyzeframe)
    %straight multiply mask? -Garbage
    mask_frame = data{1, frame_n};
%     image(bsxfun(@times, analyzeframe, cast(mask_frame, 'like', analyzeframe)))
    
    %Find the corners
    max_x = 0; max_y = 0;
    min_x = 9999; min_y = 9999;
    size_x =1000;
    size_y=1000;
    for xs = 1:size_x
        for ys = 1:size_y
           if mask_frame(xs,ys) == 1
               if xs > max_x
                   max_x = xs;
               end
               if ys > max_y
                   max_y = ys;
               end
               if xs < min_x
                   min_x = xs;
               end
               if ys < min_y
                   min_y = ys;
               end
           end
        end
    end
    
    %make even boxes
    len_x = max_x - min_x;
    len_y = max_y - min_y;
    max_length = max(len_x, len_y)+50;
    
    min_x = min_x - (max_length - len_x)/2;
    max_x = max_x + (max_length - len_x)/2;
    min_y = min_y - (max_length - len_y)/2;
    max_y = max_y + (max_length - len_y)/2;
    
    %Check oversize
    if max_x > size_x
        max_x = size_x;
        min_x = size_x-max_length;
    end
    if min_x < 1
        max_x = 1+max_length;
        min_x = 1;
    end
    
    if max_y > size_y
        max_y = size_y;
        min_y = size_y-max_length;
    end
    if min_y < 1
        max_y = 1+max_length;
        min_y = 1;
    end
    
    imwrite(analyzeframe(min_x:max_x,min_y:max_y,:), append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S8\ImCropped\',name, '\frame_',num2str(a), '.jpg'), 'jpg');


end
end