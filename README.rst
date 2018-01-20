window_challenge
================

Installation
------------
Clone this repository locally.

Running the solution
--------------------

1. Copy the input file to the cloned directory ``window_challenge/window_challenge``
2. From inside the cloned directory containing the script (window_challenge/window_challenge), run the challenge solution with ``python window_challenge.py <input file>`` where <input file> is the name of the input file including extension (ex. 'input.txt')

Running unit tests, performance tests, etc.
-------------------------------------------

Performance testing for time is performed using the standard time lib, but the ``guppy`` package is required for the default memory testing below.

If necessary, ``pip install guppy`` to resolve import errors.

Custom performance testing
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To test performance with a custom input file, copy the file to the cloned directory ``window_challenge/window_challenge``.
2. From inside the cloned directory containing the script (window_challenge/window_challenge), run the tests with ``python test_window_challenge.py <input file>`` where <input file> is the name of the input file including extension (ex. 'input.txt')

Running the included tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

From inside the cloned directory containing the script (window_challenge/window_challenge), run the tests with ``python test_window_challenge.py``




Explanation
-----------

The solution first processes the input data into a new list of values representing increasing & decreasing ranges (hereafter, ``processed_vals`` consistent with the solution script).

    ex. input data ``188930 194123 201345 154243 154243`` yields ``[1, 2, -1, 0]``


When a < b, the next value appended is equal to the last value in the list + 1 when the last value is greater than or equal to zero, otherwise 1 is appended.

Similarly, when a > b, the next value appended is equal to the last value in the list - 1 when the last value is less than or equal to zero, otherwise -1 is appended.

When a = b, 0 is appended. ::

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

The net number of increasing and decreasing subranges in the first window of days can now be calculated as the sum of values in range [0,K-1].

    ex. for the example input data above, ``[1, 2]`` = 3

The solution also stores the maximum value of the first increasing, decreasing, or flat subrange included in the initial window of days (used for subsequent windows). ::

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

-----------

For subsequent windows of days, the net number of increasing and deceasing subranges is only affected by the *new value being included on the right side of the range* and the *value now being excluded on the left side of the range*.

The solution handles the new values using the following logic:

If the absolute value of the new value is greater than or equal to (K-1), the *entire window of days is either increasing or decreasing*.  The net is updated to reflect ``(N)(N-1)/2`` (positive or negative consistent with the sign of the new value).  The var ``left`` is also updated to K-1 with sign consistent with the increasing or decreasing range.  No further calculations need to be done for this window of days.

    ``left`` tracks the effect on ``net`` of removing the leftmost value in the subsequent window of days. The maximum possible impact of removing a value is +/- (K-1) in the case of an entirely increasing or decreasing range of size K.

If the absolute value of the new value is less than or equal to (K-1), the new value is added to the net total, and ``left`` is subtracted from the net total (and incremented positively or negatively toward zero).

If, as a consequence of the above, ``left`` is equal to zero, the value is recalculated using the ``left_subrange_len`` function and the current window of days before continuing the loop. ::

    for ix in range(1, parsed_input.n-parsed_input.k+1):
        print processed_vals[ix:(ix+parsed_input.k-1)]
        # handle new value on the right
        if abs(processed_vals[ix + parsed_input.k-2]) >= (parsed_input.k-1):
            net = copysign(parsed_input.k * (parsed_input.k-1) / 2, processed_vals[ix + parsed_input.k-2])
            print str(int(net))
            left = copysign((parsed_input.k - 1), processed_vals[ix + parsed_input.k-2])
            continue

        net += processed_vals[ix + parsed_input.k-2]
        # handle value on the left that is no longer included
        if abs(left) > (parsed_input.k-1):
            net -= (copysign((parsed_input.k-1), left))
            if processed_vals[parsed_input.k-1] <= parsed_input.k:
                left -= copysign(1, left)
        else:
            net -= left
            if processed_vals[parsed_input.k-1] <= parsed_input.k:
                left -= copysign(1, left)

        # if the left list is exhausted, recalc
        if not left:
            left = left_subrange_len(deepcopy(processed_vals[ix:(ix+parsed_input.k-1)]))

        print str(int(net))

-----------

Notes
-----
This solution needs some PEP8 cleanup.
