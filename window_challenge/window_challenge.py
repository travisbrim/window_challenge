import collections
from copy import deepcopy
from math import copysign
import sys

def input_parser(input_file):

    if not isinstance(input_file, file):
        raise ValueError('input_file is required to be a File')

    InputData = collections.namedtuple('InputData', ['n', 'k' ,'vals'])

    body = input_file.readlines()
    params = body[0].rstrip('\n').split(' ')
    data = body[1].rstrip('\n').split(' ')

    return InputData(int(params[0]), int(params[1]), data)

def subrange_processor(vals):

    if len(vals) < 1:
        raise ValueError('Input list cannot be empty')

    output = []

    for ix in range(1, len(vals)):
        if (int(vals[ix]) > int(vals[ix-1])):
            if output and output[-1] > 0:
                output.append(output[-1] + 1)
            else:
                output.append(1)
        elif (int(vals[ix]) < int(vals[ix-1])):
            if output and output[-1] < 0:
                output.append(output[-1] - 1)
            else:
                output.append(-1)
        else:
            output.append(0)

    return output


def left_subrange_len(vals):
    output = vals.pop(0)

    if output == 0:
        return output

    for val in vals:
        if (abs(val) > abs(output)):
            output += copysign(1, abs(val))
        else:
            break

    return output

def main(filename, testing=False):
    with open(filename, 'r') as f:
        parsed_input = input_parser(f)

    if parsed_input.n < 1:
        raise ValueError('Dataset length is required to be greater than 1')

    if parsed_input.k < 1:
        raise ValueError('Window size is required to be greater than 1')

    if parsed_input.k > parsed_input.n:
        raise ValueError('Window size K cannot exceed N')

    if parsed_input.n > 200000:
        print('---- Warning: Input size exceeds tested conditions ----')

    processed_vals = subrange_processor(parsed_input.vals)
    # calculate initial net of increasing, decreasing subranges
    initial_range = processed_vals[0:(parsed_input.k-1)]
    net = sum(initial_range)
    left = left_subrange_len(deepcopy(initial_range)) # TODO: deepcopy?

    print str(net)

    for ix in range(1, parsed_input.n-parsed_input.k+1):
        window = processed_vals[ix:(ix+parsed_input.k-1)]
        next_val = processed_vals[ix + parsed_input.k-2]
        # handle new value on the right
        if abs(next_val) >= (parsed_input.k-1):
            net = copysign(parsed_input.k * (parsed_input.k-1) / 2, next_val)
            # note: copysign results in a float, hence the need for int(net)
            print str(int(net))
            # if the entire range in increasing or decreasing, the impact
            # of removing the leftmost val can never be greater than
            # +/- (K-1)
            left = copysign((parsed_input.k - 1), processed_vals[ix + parsed_input.k-2])
            continue

        # if abs(next_val) < (parsed_input.k-1)

        # add impact of the new val on the right
        net += next_val

        # handle value on the left that is no longer included
        net -= left
        # increment left toward 0
        left -= copysign(1, left)

        # if the left list is exhausted, recalculate based on this window
        if not left:
            left = left_subrange_len(deepcopy(window)) # TODO: deepcopy?

        # note: copysign results in a float, hence the need for int(net)
        print str(int(net))

if __name__ == '__main__':
    main(sys.argv[1])
