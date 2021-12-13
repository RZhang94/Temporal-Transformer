import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Training script')

    import pdb
    pdb.set_trace()
    
    # General Arguments
    parser.add_argument('-d', '--dataset', default='h36m', type=str, metavar='NAME', help='target dataset') # the dataset h36m
    parser.add_argument('-str', '--subjects-train', default='S1,S5,S6,S7,S8', type=str, metavar='LIST',
                        help='training subjects separated by comma')
    parser.add_argument('-ste', '--subjects-test', default='S9,S11', type=str, metavar='LIST', help='test subjects separated by comma')
    parser.add_argument('-c', '--checkpoint', default='checkpoint', type=str, metavar='PATH',
                        help='checkpoint directory')
    
    # default=1, create the checkpoint for every 1 epoch.
    parser.add_argument('--checkpoint-frequency', default=1, type=int, metavar='N',
                        help='create a checkpoint every N epochs')
    
    parser.add_argument('-r', '--resume', default='', type=str, metavar='FILENAME',
                        help='checkpoint to resume (file name)')
    
    parser.add_argument('--evaluate', default='', type=str, metavar='FILENAME', help='checkpoint to evaluate (file name)')
    parser.add_argument('--export-training-curves', action='store_true', help='save training curves as .png images')


    # Model parameters
    parser.add_argument('-s', '--stride', default=1, type=int, metavar='N', help='chunk size to use during training')
    parser.add_argument('-e', '--epochs', default=200, type=int, metavar='N', help='number of training epochs')
    parser.add_argument('-b', '--batch-size', default=512, type=int, metavar='N', help='batch size in terms of predicted frames')
    parser.add_argument('-drop', '--dropout', default=0., type=float, metavar='P', help='dropout probability')
    parser.add_argument('-lr', '--learning-rate', default=0.0001, type=float, metavar='LR', help='initial learning rate')
    parser.add_argument('-lrd', '--lr-decay', default=0.99, type=float, metavar='LR', help='learning rate decay per epoch')

    parser.add_argument('-no-da', '--no-data-augmentation', dest='data_augmentation', action='store_false',
                        help='disable train-time flipping')
    
    parser.add_argument('-frame', '--number-of-frames', default=9, metavar='N',
                        help='how many frames used as input')
    

    # Experimental
    # leave it as blank, use later if need to render the result.

    args = parser.parse_args()


    if args.resume and args.evaluate:
      print('Invalid flags: --resume and --evaluate cannot be set at the same time')
      exit()
        
    if args.export_training_curves and args.no_eval:
      print('Invalid flags: --export-training-curves and --no-eval cannot be set at the same time')
      exit()
    return args

if __name__ == '__main__':
    args = parse_args()
    print(args)