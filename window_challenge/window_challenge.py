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


def left_subrange(vals):
    output = [vals.pop(0)]

    if output[0] == 0:
        return output

    for val in vals:
        if (abs(val) > abs(output[-1])):
            output.append(val)
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
    net = sum(processed_vals[0:(parsed_input.k-1)])
    left = left_subrange(deepcopy(processed_vals[0:(parsed_input.k-1)]))
    print processed_vals[0:(parsed_input.k-1)]
    print str(net)

    count = 1

    for ix in range(1, parsed_input.n-parsed_input.k+1):
        count += 1
        print processed_vals[ix:(ix+parsed_input.k-1)]
        # handle new value on the right
        if abs(processed_vals[ix + parsed_input.k-2]) > parsed_input.k:
            print str(int(net))
            continue

        if abs(processed_vals[ix + parsed_input.k-2]) > (parsed_input.k-1):
            print 'adding: ' + str((copysign((parsed_input.k-1), processed_vals[ix + parsed_input.k-2])))
            net += (copysign((parsed_input.k-1), processed_vals[ix + parsed_input.k-2]))
        else:
            print 'adding: ' + str(processed_vals[ix + parsed_input.k-2])
            net += processed_vals[ix + parsed_input.k-2]
        # handle value on the left that is no longer included
        if abs(left[-1]) > (parsed_input.k-1):
            print 'subtracting: ' + str((copysign((parsed_input.k-1), left[-1])))
            net -= (copysign((parsed_input.k-1), left[-1]))
            if processed_vals[parsed_input.k-1] <= parsed_input.k:
                left.pop(-1)
        else:
            print 'subtracting: ' + str(left[-1])
            net -= left[-1]
            if processed_vals[parsed_input.k-1] <= parsed_input.k:
                left.pop(-1)

        # if the left list is exhausted, recalc
        if not left:
            left = left_subrange(deepcopy(processed_vals[ix:(ix+parsed_input.k-1)]))

        print str(int(net))

    print count

if __name__ == '__main__':
    main(sys.argv[1])
