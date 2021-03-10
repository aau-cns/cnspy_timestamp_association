#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Requirements:
# sudo pip install numpy pandas
########################################################################################################################
import numpy as np


class TimestampAssociation:
    def __init__(self):
        pass

    @staticmethod
    def get_closest(array, values):
        # from: https://stackoverflow.com/a/46184652
        # by: https://stackoverflow.com/users/1536499/anthonybell
        # make sure array is a numpy array
        array = np.array(array)
        values = np.array(values)
        # get insert positions
        idxs = np.searchsorted(array, values, side="left")

        # find indexes where previous index is closer
        prev_idx_is_less = ((idxs == len(array)) | (np.fabs(values - array[np.maximum(idxs - 1, 0)]) < np.fabs(
            values - array[np.minimum(idxs, len(array) - 1)])))
        idxs[prev_idx_is_less] -= 1

        return array[idxs], idxs

    @staticmethod
    def associate_timestamps(t_est, t_gt, offset=0.0, max_difference=0.02):
        # returns idx_est, idx_gt, t_est_matched, t_gt_matched
        swapped = False
        if len(t_est) > len(t_gt):
            t_vec1 = t_est + offset
            t_vec2 = t_gt
            swapped = True
        else:
            t_vec1 = t_gt
            t_vec2 = t_est + offset

        closest_t_vec1, idx1 = TimestampAssociation.get_closest(t_vec1.transpose().ravel(), t_vec2.transpose().ravel())
        idx2 = np.arange(0, len(idx1), dtype=np.int32)
        diff = np.abs(closest_t_vec1 - np.array(t_vec2.ravel()))
        mask_greater = np.where(diff >= max_difference)[0]
        idx_1 = np.delete(idx1, mask_greater, axis=0)
        idx_2 = np.delete(idx2, mask_greater, axis=0)
        vec_1_matched = t_vec1[idx_1]
        vec_2_matched = t_vec2[idx_2]

        # returns idx_est, idx_gt, t_est_matched, t_gt_matched
        if not swapped:
            return idx_2, idx_1, vec_2_matched, vec_1_matched
        else:
            return idx_1, idx_2, vec_1_matched, vec_2_matched


########################################################################################################################
#################################################### T E S T ###########################################################
########################################################################################################################
import unittest
import time
import csv
from csv2dataframe.TimestampCSV2DataFrame import TimestampCSV2DataFrame


class TimestampAssociation_Test(unittest.TestCase):
    start_time = None

    def tuple_list_2_csv(self, d, fn):
        with open(fn, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['idx1', 'idx2'])
            for row in d:
                writer.writerow(row)

    def load_data(self):
        df_t_est = TimestampCSV2DataFrame(
            fn='./sample_data/t_est.csv')
        df_t_gt = TimestampCSV2DataFrame(
            fn='./sample_data/t_gt.csv')

        return df_t_est, df_t_gt

    def start(self):
        self.start_time = time.time()

    def stop(self):
        print("Process time: " + str((time.time() - self.start_time)))

    def test_load_from_CSV(self):
        df_t_est, df_t_gt = self.load_data()
        self.assertTrue(len(df_t_est.get_t_vec()) > 0)
        self.assertTrue(len(df_t_gt.get_t_vec()) > 0)

    def test_associate_1(self):
        df_t_est, df_t_gt = self.load_data()

        t_est = df_t_est.get_t_vec()
        t_gt = df_t_gt.get_t_vec()

        self.start()
        idx_est, idx_gt, t_est_matched, t_gt_matched = TimestampAssociation.associate_timestamps(
            t_est,
            t_gt)

        matches2 = zip(idx_est, idx_gt)
        self.stop()
        # takes: 0.5sec
        self.tuple_list_2_csv(d=matches2, fn='./results/matches.txt')


if __name__ == "__main__":
    unittest.main()
