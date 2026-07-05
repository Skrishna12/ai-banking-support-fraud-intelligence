import streamlit as st
import sys

st.write("Python executable:")
st.write(sys.executable)

import torch
st.write("Torch version:")
st.write(torch.__version__)