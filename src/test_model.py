import pandas as pd
import numpy as np
from PIL import Image
from viyapy import viya_utils
from scoreModel import scoreModel
import os
import settings


EM_CLASSIFICATION,EM_PROBABILITY,ERROR = scoreModel(10, 10, 10)

print(EM_CLASSIFICATION)
print(EM_PROBABILITY)
print(ERROR)