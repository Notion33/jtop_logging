#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
import argparse
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple jtop logger')
    # Standard file to store the logs
    parser.add_argument('--file', action="store", dest="file", default="log.csv")
    args = parser.parse_args()

    print("jtop log visualizer")
    print("Loding file on {file}".format(file=args.file))

    list_key = []
    list_index = []
    target_index_name = ["GPU", "RAM", "CPU1", "CPU2", "CPU3", "CPU4", "CPU5", "CPU6", "CPU7", "CPU8"]

    try:
        with open(args.file, 'r') as csvfile:
            # reader = csv.DictReader(csvfile)
            reader = csv.reader(csvfile)
            list_reader = list(reader)
            values = np.zeros((10,(reader.line_num-1)))

            list_key = list_reader[0]
            try :
                for index_name in target_index_name:
                    list_index.append(list_key.index(index_name))
                    board_model = 'Xavier AGX'
            except:
                board_model = 'Xavier NX'

            for idx_values, list_status in enumerate(list_reader[1:]):
                for idx_keys in range(len(list_index)):
                    values[idx_keys][idx_values] = list_status[list_index[idx_keys]]

            ## Draw the graphs
            fig = plt.figure(figsize=((len(list_index)/2)*5,10))
            fig_ax = []
            average_cpu_usage = 0
            for idx in range(len(list_index)):
                fig_ax.append(fig.add_subplot(2,int(len(list_index)/2),idx+1))
                fig_ax[idx].plot(values[idx])
                plot_title = target_index_name[idx] +" usage / Mean : "
                mean_value = round(np.mean(values[idx]),2)
                if idx == 1:
                    plot_title += "{:.2f}".format(mean_value/1024) + "MB"
                else:
                    plot_title += "{:.2f}".format(mean_value) + "%"
                if idx > 1:
                    average_cpu_usage += mean_value
                fig_ax[idx].set_title(plot_title)

            fig.suptitle("Average CPU usage is : " + "{:.2f}".format(average_cpu_usage/(len(list_index)-2))+"%", fontsize=16)
            plt.show()
            fig.savefig('./result.png')
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")

# EOF