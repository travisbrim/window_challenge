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

When a < b, the next value appended is equal to the last value in the list + 1 when the last value is greater than or equal to zero, otherwise 1 is appended.  Similarly, when a > b, the next value appended is equal to the last value in the list - 1 when the last value is less than or equal to zero, otherwise -1 is appended.  When a = b, 0 is appended.

    TODO: insert code here

The net number of increasing and decreasing subranges in the first window of days can now be calculated as the sum of values in range [0,K-1].

    ex. for the example input data above, ``[1, 2]`` = 3

-----------

For subsequent windows of days, the net number of increasing and deceasing subranges is only affected by the *new value being included on the right side of the range* and the *value now being excluded on the left side of the range*.

For this problem, you are given N days of average home sale price data, and a fixed window size K . For each window of K days, from left to right, find the number of increasing subranges within the window minus the number of decreasing subranges within the window.

A window of days is defined as a contiguous range of days. Thus, there are exactly N-K+1 windows where this metric needs to be computed. An increasing subrange is defined as a contiguous range of indices [a,b], a < b , where each element is larger than the previous element. A decreasing subrange is similarly defined, except each element is smaller than the previous element.

### Constraints

    1 ≤ N ≤ 200,000 days
    1 ≤ K ≤ N days

## Input Format

Your solution should accept an input file (input.txt) with the following contents:

 Line 1: Two integers, N and K.
 Line 2: N positive integers of average home sale price, each less than 1,000,000.

Your solution will only be tested with valid input, according to the above constraints.

## Output Format

Your solution should output one integer for each window’s result, with each integer on a separate line, to an output file or to the console.

### Sample Input

5 3

188930 194123 201345 154243 154243

### Sample Output

3

0

-1

### Explanation

For the first window of [188930, 194123, 201345], there are 3 increasing subranges ([188930, 194123, 201345], [188930, 194123], and [194123, 201345]) and 0 decreasing, so the answer is 3. For the second window of [194123, 201345, 154243], there is 1 increasing subrange and 1 decreasing, so the answer is 0. For the third window of [201345, 154243, 154243], there is 1 decreasing subrange and 0 increasing, so the answer is -1.
Performance

Your solution should run in less than 10 seconds and use less than 50MB of memory with a valid input of any size (within the given constraints).
