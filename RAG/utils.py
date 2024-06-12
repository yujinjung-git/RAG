import os
import warnings

def initialize_environment():
    # OpenMP 경고 무시 설정
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    warnings.filterwarnings("ignore")