#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
os.environ["DISPLAY"]=":1"
from src.aa_biosynthesis_pathways_AS import main
main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
