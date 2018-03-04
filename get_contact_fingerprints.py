#!/usr/bin/env python
"""
Take a set of residue-frequency files generated by `get-resfreqs.py`,
group them into a single table file by matching residue pair ids, and
plot them as a clustered heat-map.
"""

from __future__ import division
import sys
import argparse
import numpy as np


def parse_frequencyfiles(freq_files, freq_cutoff):
    columns = len(freq_files)
    ret = {}
    for fidx, freq_file in enumerate(freq_files):
        for line in freq_file:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue

            tokens = line.split("\t")
            res1 = tokens[0]
            res2 = tokens[1]
            freq = float(tokens[3])

            if not (res1, res2) in ret:
                ret[(res1, res2)] = np.zeros(columns)

            ret[(res1, res2)][fidx] = freq

    # Remove entries where no frequency exceeds 0.6
    ret = {key: val for key, val in ret.items() if np.amax(val) > freq_cutoff}
    return ret


def write_frequencytable(freq_table, col_labels, out_file):
    out_file.write("\t".join([] + col_labels) + "\n")
    for (res1, res2) in freq_table:
        freq_strings = [str(freq) for freq in freq_table[(res1, res2)]]
        out_file.write("\t".join([res1, res2] + freq_strings) + "\n")


def plot_frequencies(freq_table, col_labels, out_file, cluster_columns):
    import pandas as pd
    import matplotlib
    import os
    if "DISPLAY" not in os.environ:
        matplotlib.use('agg')
    import seaborn as sns; 
    sns.set(color_codes=True)
    # sns.set(font_scale=0.5)
    
    freq_matrix = np.array([freq_table[(r1, r2)] for (r1, r2) in freq_table])
    row_labels = [r1 + " - " + r2 for (r1, r2) in freq_table]
    pdframe = pd.DataFrame(freq_matrix, index=row_labels, columns=col_labels, col_cluster=cluster_columns)
    fingerprints = sns.clustermap(pdframe,
                                  figsize=(pdframe.shape[1], pdframe.shape[0]),
                                  annot=True,
                                  cmap='Blues')

    if out_file is not None:
        fingerprints.savefig(out_file)
        print("Wrote fingerprint heatmap to "+out_file)
    else:
        import pylab as plt
        plt.show()


def main():
    # Parse command line arguments
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            # Prints full program help when error occurs
            self.print_help(sys.stderr)
            sys.stderr.write('\nError: %s\n' % message)
            sys.exit(2)

    parser = MyParser(description=__doc__,
                      formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--input_frequencies',
                        type=argparse.FileType('r'),
                        required=True,
                        nargs='+',
                        help="Paths to one or more residue frequency files")
    parser.add_argument('--column_headers',
                        type=str,
                        required=False,
                        nargs='+',
                        help="Header column labels. If nothing is specified, the input_frequencies filenames are used")
    parser.add_argument('--table_output',
                        type=argparse.FileType('w'),
                        required=False,
                        default=None,
                        help="If specified, the tab-separated frequency table will be written to this file")
    parser.add_argument('--plot_output',
                        type=str,
                        required=False,
                        default=None,
                        help="If specified, the heatmap will be written to this file (supports svg and png formats)")
    parser.add_argument('--frequency_cutoff',
                        type=float,
                        required=False,
                        default=0.6,
                        help="Only interactions occurring at least this frequently will be plotted")
    parser.add_argument('--cluster_columns',
                        type=bool,
                        required=False,
                        default=False,
                        help="Perform hierarchical clustering on the columns")


    args = parser.parse_args()

    freq_table = parse_frequencyfiles(args.input_frequencies, args.frequency_cutoff)

    # Determine column headers and exit on error
    column_headers = [f.name for f in args.input_frequencies] if args.column_headers is None else args.column_headers
    if len(column_headers) != len(args.input_frequencies):
        parser.print_help(sys.stderr)
        sys.stderr.write("\nError: --column_header arguments must match length of --input_frequencies\n")
        sys.exit(2)

    if args.table_output is not None:
        write_frequencytable(freq_table, column_headers, args.table_output)

    plot_frequencies(freq_table, column_headers, args.plot_output, args.cluster_columns)


if __name__ == '__main__':
    main()
