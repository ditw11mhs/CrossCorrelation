import streamlit as st
import numpy as np
import pandas as pd
import os
import sys


class Main:
    def __init__(self):
        pass

    def main(self):
        self.deploy = True

        # Page Configuration

        if self.deploy:
            favicon_path = r"/app/Data/favicon-web.ico"
        else:
            favicon_path = r"Data\favicon-web.ico"

        st.set_page_config(
            page_title='Tugas Cross Correlation Biomodelling ITS', page_icon=favicon_path, layout="wide")

        # File Loading and Padding

        data1, data2 = self.file_loader()
        self.data1_len, self.data2_len = self.length(data1, data2)
        data2_padded = self.padder(data2)

        st.title("Cross Correlation")
        st.caption("Aditya Wardianto 07311940000001 - Biomodelling ITS")
        # st.markdown("""<script async defer src="https://buttons.github.io/buttons.js"></script><a class="github-button" href="https://github.com/ditw11mhs/CrossCorrelation/" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" aria-label="Open ditw11mhs/CrossCorrelation on GitHub">Watch</a>""", unsafe_allow_html=True)
        st.components.v1.html("""
        <!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/ditw11/CrossCorrelation/subscription" data-color-scheme="no-preference: dark; light: dark; dark: dark;" data-size="large" data-show-count="true" aria-label="Watch ditw11/CrossCorrelation on GitHub">Watch</a>
        """)
        # Time Lag
        st.header("Time Lag")
        self.t_lag = st.slider(label="Time Lag", min_value=-(self.data2_len-1), max_value=self.data2_len -
                               1, value=0, help="Slider to shift Data 2 position horizontaly")
        data2_out = data2_padded[self.data2_len -
                                 self.t_lag:2*self.data2_len-self.t_lag]

        col1, col2 = st.columns(2)
        # Plotting Input
        with col1:
            st.header("Input Plot")
            chart_input = pd.DataFrame(
                {
                    "Heel Data": data1,
                    "Toe Data": data2_out
                }
            )
            st.line_chart(chart_input)

        # Correlation
        correlation = self.correlate(data1, data2_padded)

        col3, col4 = st.columns(2)
        with col3:
            # Plotting Correlation
            st.header("Correlation Plot")
            chart_output = pd.DataFrame({'Correlation': correlation})
            st.line_chart(chart_output)

        # Normalization
        norm_correlation = self.normalize(correlation)

        with col2:
            # Plotting Normalized Correlation
            st.header("Normalization")
            chart_norm = pd.DataFrame(
                {'Normalized Correlation': norm_correlation})
            st.line_chart(chart_norm)

        with col4:
            st.header('Data Table')
            st.write(pd.DataFrame({
                'Heel Data': data1,
                'Toe Data': data2_out,
                'Correlation': correlation,
                'Normalized Correlation': norm_correlation
            }
            ))

    @st.cache(allow_output_mutation=True)
    def file_loader(self):

        if self.deploy:
            path1 = r'/app/Data/Heel123.txt'
            path2 = r'/app/Data/Toe123.txt'
        else:
            path1 = r'Data\Heel123.txt'
            path2 = r'Data\Toe123.txt'

        data1 = np.loadtxt(path1)
        data2 = np.loadtxt(path2)
        # x = np.linspace(0, 1, 5000)
        # data1 = np.sin(5*np.pi*x)
        # data2 = np.sin(5*np.pi*x)

        return data1, data2

    @st.cache
    def length(self, data1, data2):
        return len(data1), len(data2)

    @st.cache
    def padder(self, data2):
        data2_padded = np.pad(
            data2, (self.data2_len, 2*self.data2_len), 'constant', constant_values=0)
        return data2_padded

    def correlate(self, data1, data2_padded):
        start = self.data2_len - self.t_lag
        end = 2*self.data2_len-self.t_lag+self.data1_len-1

        data2_1d = data2_padded[start:end]

        data2_2d = np.lib.stride_tricks.sliding_window_view(
            data2_1d, self.data1_len)
        correlation = np.dot(data2_2d, data1)
        return correlation

    def normalize(self, data):
        # return (data-np.min(data))/((np.max(data)-np.min(data)+10e-8))
        return data/self.data1_len


if __name__ == "__main__":
    mainClass = Main()
    mainClass.main()
