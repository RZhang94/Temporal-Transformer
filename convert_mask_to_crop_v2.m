% clf; clc; clear;
% %Load in the 2d masks, name should default to data
% name = 'Discussion 1.55011271'
% data = importdata(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S1\MySegmentsMat\ground_truth_bb\', name ,'.mat'));
% %Upload video and retrieve the relevant cdata for projection
% video= mmread(append('C:\Users\JoyceRay\PycharmProjects\ECE-3\PoseFormer-main\data\S1\Videos\',name,'.mp4'))
% analyzeframes = video.frames;

for a = 1:10
    frame_n = a*100;
    
    singleframe = data(1,frame_n); %Isolate frame
    
    analyzeframe = analyzeframes(frame_n).cdata;
    
    subplot(2,5,a)
    hold on
%     image(analyzeframe)
    %straight multiply mask? -Garbage
    mask_frame = data{1, frame_n};
%     image(bsxfun(@times, analyzeframe, cast(mask_frame, 'like', analyzeframe)))
    
    %Find the corners
    max_x = 0; max_y = 0;
    min_x = 9999; min_y = 9999;
    [size_x, size_y] = size(mask_frame);
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
    
%     plot(min_y, min_x, 'd')
%     plot(max_y, max_x, 'd')
    image(analyzeframe(min_x:max_x,min_y:max_y,:))
    title( 'Frame :', frame_n)

end