# -*- coding:utf8 -*-

import argparse
# from icecream import ic as print


def print_args(args, save_path=None):
    print(f"{'=' * 20} Options {'=' * 20}")

    args_str = []
    for arg in vars(args):
        formated_str = arg.rjust(15) + " : " + str(getattr(args, arg))
        print(formated_str)
        args_str.append(formated_str)
    
    if save_path is not None and save_path.endswith('.txt'):
        fp = open(save_path, 'w')
        for line in args_str:
            fp.write(line + '\n')
        fp.close()
    
    print(f"{'=' * 20} Options {'=' * 20}")


def parse_normal():
    """
    Example:
        python argument_parser.py --dataset=sunrgbd --num_point=10000
    """
    parser = argparse.ArgumentParser()
    # parser.add_argument('data_root', type=str, help='path of data root') # this is a required positional argument
    parser.add_argument('--name', help='name of this experiment') # no default value, will set to None
    
    # no default value, will set to None
    parser.add_argument('--num_memory', type=int, help='number of memory')

    # will set to str type if not explicitly specify the data type
    parser.add_argument('--dataset', default='sunrgbd', help='Dataset: sunrgbd or scannet [default: sunrgbd]')
    parser.add_argument('--num_point', type=int, default=20000, help='Point Number [default: 20000]')

    # we can run the script with python argument_parse.py --gpu 0 1 2 3
    parser.add_argument('--gpu', type=int, nargs='+', default=(0, 1), help='specify gpu devices')
    args = parser.parse_args()
    print(args)
    
    for k, v in vars(args).items():
        print(k, v, type(v))

    print_args(args)


def parse_action():
    """
    命令行中只要出现--viz,--compute_median_size等参数则为true,否则为false, 只为bool类型
    Example:
        python argument_parser.py --viz
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--viz', action='store_true', help='Run data visualization.')
    parser.add_argument('--compute_median_size', action='store_true', help='Compute median 3D bounding box sizes for each class.')
    parser.add_argument('--gen_v1_data', action='store_true', help='Generate V1 dataset.')
    parser.add_argument('--gen_v2_data', action='store_true', help='Generate V2 dataset.')
    args = parser.parse_args()

    print(args)
    print(type(args.viz))


def modify_commandline_options(parser):
    # net structure and parameters
    parser.add_argument('--net_recon', type=str, default='resnet50', choices=['resnet18', 'resnet34', 'resnet50'], 
                        help='network structure')
    parser.add_argument('--init_path', type=str, default='checkpoints/init_model/resnet50-0676ba61.pth')
    parser.add_argument('--bfm_folder', type=str, default='BFM')
    parser.add_argument('--bfm_model', type=str, default='BFM_model_front.mat', help='bfm model')
    parser.add_argument('--pin_mem', action='store_true',
                        help='Pin CPU memory in DataLoader for more efficient (sometimes) transfer to GPU.')
    return parser


def parse_commandline_options():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = modify_commandline_options(parser)
    opt, unknown = parser.parse_known_args()  # parse again with new defaults
    
    print(unknown, type(unknown))

    message = ''
    message += '----------------- Options ---------------\n'
    for k, v in sorted(vars(opt).items()):
        comment = ''
        default = parser.get_default(k)
        if v != default:
            comment = '\t[default: %s]' % str(default)
        message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
    message += '----------------- End -------------------'
    print(message)


def get_args():
    parser = argparse.ArgumentParser('VideoMAE pre-training script', add_help=False) # add_help=False means no help str
    parser.add_argument('--batch_size', default=64, type=int)
    parser.add_argument('--epochs', default=800, type=int)
    return parser.parse_args()


if __name__=='__main__':
    parse_commandline_options()
    exit(0)

    parse_normal()

    # get_args()

    # parse_action()

    # parse_commandline_options()
