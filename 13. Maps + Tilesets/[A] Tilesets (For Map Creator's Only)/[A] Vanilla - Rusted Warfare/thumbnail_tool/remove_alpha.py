#!/usr/bin/python

import Image
from PIL import ImageFont
from PIL import ImageDraw 

import os
import subprocess
import sys
import re
import time


mapImage  = Image.open(sys.argv[1])

mapImage = mapImage.convert("RGB")

mapImage.save(sys.argv[1])


