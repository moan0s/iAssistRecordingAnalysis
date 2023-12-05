#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:15:49 2023

@author: moanos
"""

import numpy as np

filename = "/home/moanos/Nextcloud/Masterarbeit/recordings/depth.npz"

a = np.load(filename, allow_pickle=True)
a["depths"]

