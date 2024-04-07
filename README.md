
# DEP-Time-Delay-Estimation-with-Data-Preprocessing
DEP: Time Delay Estimation with Data Preprocessing

DEP is a comprehensive software tool designed to facilitate the estimation of time delays between multiple images of a lensed quasar. Tailored for astronomers and astrophysicists, DEP integrates advanced data preprocessing techniques with a user-friendly graphical interface, enhancing the accuracy and accessibility of time-delay cosmography.

## Features

* Intuitive GUI: Simplifies the analysis process, making advanced computational methods accessible to users without programming expertise.
* Advanced Preprocessing: Includes a suite of data preprocessing techniques to optimize time-delay estimation.
* Multiple Estimation Methods: Supports various time-delay estimation algorithms, providing flexibility in analysis approaches.
* Descriptive Statistics: Offers insightful statistical analysis and visualization of light curves.

## Installation

Ensure you have Python 3.8 or newer installed on your system. DEP can be installed using the following steps:

First, clone the repository to your local machine:

bash
    git clone https://github.com/luisleonanaya/DEP-Time-Delay-Estimation-with-Data-Preprocessing
    cd DEP-Time-Delay-Estimation-with-Data-Preprocessing

Then, you can run the main script directly with Python:

bash

    python time_delay_estimation_tool_V1.py

## Requirements 

DEP relies on standard Python packages:
* numpy
* scipy
* matplotlib
* pandas
* Pillow
* scikit-learn
* scikit-image
* statsmodels
* reportlab

## Usage

Start DEP by navigating to the DEP directory and executing the main script:

bash

    python time_delay_estimation_tool_V1.py

Follow the on-screen instructions to upload light curves, select preprocessing techniques, and perform time-delay estimation.

## Releases
Download the appropriate executable for your OS from the releases page:

    Windows: [DEP-v1.0-windows.zip](https://github.com/luisleonanaya/DEP-Time-Delay-Estimation-with-Data-Preprocessing/releases/download/DEP-v1.0-windows/DEP_estimation_tool_V1_windows.zip)
    macOS: td_estimation_tool_macOS-v1.0.zip
    Linux: DEP_estimation_tool_linux-v1.0.zip

## Documentation

For detailed information on DEP's features and functionalities, refer to the DEP User Manual. The manual provides step-by-step instructions on using DEP, from data input to result interpretation.

## Support

For questions or issues related to DEP, please contact us at lanaya@astro.unam.mx.

## Citation

If you use DEP in your research, please cite the following paper: 
Luis Leon-Anaya, Juan C Cuevas-Tello, Octavio Valenzuela, César A Puente, Carlos Soubervielle-Montalvo, Data science methodology for time-delay estimation and data preprocessing of the time-delay challenge, Monthly Notices of the Royal Astronomical Society, Volume 522, Issue 1, June 2023, Pages 1323–1341, https://doi.org/10.1093/mnras/stad817

## License

DEP is released under the GNU General Public License v3.0. See the LICENSE file for more details.
