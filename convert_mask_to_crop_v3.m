clf; clc; clear;
%Find all files
list = dir('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S2\MySegmentsMat\ground_truth_bb')
list = struct2cell(list);
targets = list(1,:); %Should remove the '.' and _'all'
targets = targets (3:end-8)
for i = 1:size(targets,2)
    str = targets{1,i};
    str = str(1:end-4);
    targets{1,i} = str;
    
end

% for index = 97:size(targets,2)
for index = 1: size(targets,2)  

name = targets{1,index};
status = mkdir(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S2\ImCropped\',name))
    if status == 1
    data = importdata(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S2\MySegmentsMat\ground_truth_bb\', name ,'.mat'));
    %Upload video and retrieve the relevant cdata for projection
    target = append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S2\Videos\',name,'.mp4');
    video= mmread(target,[0 1]);
    maxDur = video.totalDuration;
    Dur = min(maxDur, 45);
    video= mmread(target,[],[0 Dur]);
    analyzeframes = video.frames;
    fpi = 20;
    analyzeframes = analyzeframes(:, 1:fpi:end);    
    data = data(1:fpi:end);
    frame_tot = min(size(analyzeframes,2),size(data,2));

    
    frame_tot = min(113, frame_tot);

    for a = 1:frame_tot
        frame_n = 1 + (a-1)*fpi;

        analyzeframe = analyzeframes(a).cdata;

    %     image(analyzeframe)
        %straight multiply mask? -Garbage
        mask_frame = data{1, a};
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

        imwrite(analyzeframe(min_x:max_x,min_y:max_y,:), append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S2\ImCropped\',name, '\frame_',num2str(1 + (a-1)*fpi), '.jpg'), 'jpg');


    end
    end

end