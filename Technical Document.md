**DEP: Time Delay Estimation with Data Preprocessing - Technical Document**

**Introduction**

This technical document elaborates on the functionalities of time_delay_estimation_tool_V1.py, a component of the sophisticated software suite designed for estimating time delays between astronomical light curves. This suite incorporates a broad spectrum of preprocessing techniques, time delay estimation methods, and statistical analysis features to support diverse astronomical research needs. Through an interactive graphical user interface (GUI), users can effortlessly upload light curve data, choose among various preprocessing and estimation methods, and acquire detailed results, including comprehensive statistical analyses and graphical visualizations.

**Overview of** **time_delay_estimation_tool_V1.py** **Function**

Acting as the core entry point of the application, time_delay_estimation_tool_V1.py orchestrates the GUI, manages user inputs, and seamlessly integrates different components essential for the time delay estimation process. It initiates the GUI setup, configures widgets for user interaction, and ensures functionality is bound to these widgets to respond aptly to user actions. Utilizing global variables, the script effectively manages the application's state across its different facets, guaranteeing a smooth user experience.

**Key Components**

-   **GUI Initialization**: Sets up the main window, application icon, and the layout for displaying results and plots.
-   **File Upload Handlers**: Enables users to upload lead and delayed light curve data in CSV and TXT formats, providing data input flexibility.
-   **Preprocessing and Method Selection**: Offers dropdown menus for selecting preprocessing techniques and time delay estimation methods, tailored to the specific needs of the dataset.
-   **Delay Input and Range Selection**: Presents radio buttons and entry widgets for users to either input a specific time delay or select a search range, enhancing the tool's adaptability.
-   **Result Display and Export**: Integrates functions for displaying statistical analysis, histograms, and estimation results within the GUI. It also includes options for exporting these results to CSV and PDF formats, facilitating comprehensive examination and sharing.
-   **Statistical Analysis and Visualization**: Conducts descriptive statistical analysis on light curves and generates histograms for both raw and preprocessed data, offering valuable data insights.

**Functionality**

time_delay_estimation_tool_V1.py serves as the foundation of the time delay estimation tool, integrating various components and functionalities to provide a holistic analysis platform. It meticulously processes user inputs, data, and presents results, ensuring a user-friendly interface suitable for both novice and experienced researchers in astronomy.

This tool stands out by offering a wide array of preprocessing options and estimation methodologies, accommodating different research needs and preferences. The inclusion of statistical analysis and visualization capabilities further augments the tool's analytical depth, allowing users to derive significant insights from their data.

**Concluding Overview**

time_delay_estimation_tool_V1.py epitomizes a well-coordinated application, marking a significant advancement in astronomical research. It offers an accessible yet potent platform for time delay estimation between light curves, contributing invaluable insights and methodologies to the field.

**Further Documentation**

Detailed documentation on the additional functions within the suite, such as CFfilter_function.py, rawData_function.py, data_differencing, simple_net_return, waveletDenoise, dispersionSpectraV1_Function.calculate_delay, function_dcf_EK, find_lndcf_delay, csv_saver, set_dpi_awareness, clear_frame, and various utilities, is provided to ensure users can fully leverage the suite's capabilities. Each function is meticulously designed to process light curve data efficiently, apply advanced analytical techniques, and present findings in a structured and interpretable manner, ensuring the suite remains at the forefront of astronomical analysis tools.

**Documentation for** **CFfilter_function.py**

**Purpose**: Applies the Christiano-Fitzgerald (CF) filter to preprocess light curves, separating the trend and cycle components for time-delay estimation. Essential for handling irregular sampling and observational gaps in astronomical data.

**Functionality**:

-   Processes two light curves with the CF filter to extract and standardize cycle and trend components.
-   Calculates errors for each component, enhancing the reliability of subsequent analyses.

**Documentation for** **rawData_function.py**

**Purpose**: Preprocesses light curve data by standardizing magnitudes, facilitating comparison and analysis without applying complex filtering.

**Functionality**:

-   Reads light curve DataFrames, standardizing magnitudes using MinMax scaling.
-   Calculates absolute errors for the standardized light curves, preparing data for analysis.

**Documentation for** **data_differencing**

**Purpose**: Enhances time series analysis by applying differencing to light curves, highlighting changes and reducing noise.

**Functionality**:

-   Computes the difference between consecutive magnitude measurements.
-   Normalizes data post-differencing, recalculates errors, and structures results for further analysis.

**Documentation for** **simple_net_return**

**Purpose**: Calculates the simple net return (SNR) of light curve magnitudes, quantifying relative changes and aiding in the detection of variations.

**Functionality**:

-   Computes percentage changes between consecutive magnitudes, applying MinMax scaling.
-   Recalculates errors for SNR values, preparing data for time-delay estimation.

**Documentation for** **waveletDenoise**

**Purpose**: Applies wavelet denoising to light curve data, effectively reducing noise while retaining significant signal features.

**Functionality**:

-   Utilizes the VisuShrink method for wavelet denoising, standardizing the denoised magnitudes.
-   Recalculates errors based on denoised data, offering cleaned datasets for analysis.

**Documentation for** **dispersionSpectraV1_Function.calculate_delay**

**Purpose**: Estimates the time delay between two light curves using comprehensive search techniques and computational optimizations.

**Functionality**:

-   Searches for the delay that maximizes correlation between two light curves.
-   Produces a detailed DataFrame with estimated delays, error margins, and statistical measures.

**Documentation for** **DCF Methodology** **(****function_dcf_EK****)**

**Purpose**: Utilizes the discrete correlation function (DCF) to identify temporal delays between light curves, critical for studying variable astronomical sources.

**Functionality**:

-   Standardizes input light curves for DCF calculation.
-   Iterates over a range of time lags, computing correlation to estimate delays and providing a detailed statistical analysis.

**Documentation for** **LNDCF Methodology** **(****find_lndcf_delay****)**

**Purpose**: Implements the Locally Normalized Discrete Correlation Function (LNDCF) for robust delay estimation between astronomical light curves.

**Functionality**:

-   Applies LNDCF to compute correlation over a range of time lags.
-   Generates a comprehensive summary of correlation analysis, including delay estimates and statistical summaries.

**Documentation for** **csv_saver** **Module**

**Purpose**: Offers functionalities to save analysis results into CSV files, featuring a file-saving dialog and conditional logic for data relevancy.

**Functionality**:

-   Determines the appropriate DataFrame to save based on global application state.
-   Handles potential errors gracefully, providing user feedback during the save process.

**Documentation for** **set_dpi_awareness**

**Purpose**: Enhances GUI clarity on high DPI displays by adjusting the application's DPI awareness, ensuring clear and correctly scaled visual elements.

**Functionality**:

-   Improves GUI appearance on Windows by making API calls to adjust DPI awareness, with cross-version compatibility.

**Documentation for** **clear_frame**

**Purpose**: Facilitates dynamic GUI updates by removing all child widgets from a specified frame, supporting a clean interface refresh.

**Functionality**:

-   Efficiently clears specified frames of all child widgets, allowing for dynamic content updates based on user interactions or data changes.

**Documentation for Utilities in** **utilities.py**

**Purpose**: Provides helper functions for initial GUI setup and dynamic content management, including displaying initial images and clearing frames.

**Functionality**:

-   Offers essential utilities for managing Tkinter GUI applications, ensuring efficient initial visuals and interface updates.
