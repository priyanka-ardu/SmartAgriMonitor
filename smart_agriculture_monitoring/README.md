# SmartAgriMonitor
This project reimagines the Smart Agriculture Monitoring system as a file-upload-based data science pipeline, where users download CSV/Excel datasets from public portals (Kaggle, UCI, Data.gov, SoilGrids REST API) and upload them via a web-based dashboard to monitor and analyze agricultural data, providing functionalities for uploading datasets, performing exploratory data analysis (EDA), clustering, forecasting, and more.

## Features

- **Data Upload**: Upload CSV/Excel files or download datasets directly from Kaggle.
- **Exploratory Data Analysis (EDA)**: Visualize data distributions, box plots, correlation heatmaps, etc.
- **Clustering**: Visualize clustering results.
- **Forecasting**: Predict future agricultural trends using ARIMA or LSTM models.
- **Interactive Dashboard**: A web-based interface built using Streamlit for interactive data visualization and navigation.

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Data Visualization**: [Plotly](https://plotly.com/)
- **Data Science**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [Scikit-learn](https://scikit-learn.org/)
- **Modeling**: [ARIMA](https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html), [LSTM](https://www.tensorflow.org/)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/smart-agriculture-monitoring.git
    cd smart-agriculture-monitoring
    ```

2. **Set up the virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **(Optional)** If you are using Kaggle datasets, you'll need to authenticate with the [Kaggle API](https://www.kaggle.com/docs/api).

    - Place your `kaggle.json` file (which contains your Kaggle API credentials) in the `~/.kaggle/` directory (on Linux/Mac) or `C:\Users\<YourUsername>\.kaggle\` (on Windows).

5. **Run the app**:

    ```bash
    streamlit run app.py
    ```

    This will open the app in your browser at `http://localhost:8501`.

## Usage

1. **Page 1: Upload Data**: Upload your CSV/Excel dataset or download a sample dataset from Kaggle.
   - You can choose a sample from Kaggle to download directly into the app or upload your own dataset.
   
2. **Page 2: Exploratory Data Analysis (EDA)**: View data statistics, distribution plots, and perform basic cleaning.

3. **Page 3: Clustering**: Apply clustering algorithms (e.g., K-means) to group data based on certain features. Visualize the clustering results in an interactive scatter plot.

4. **Page 4: Classification**: Apply classification algorithms (e.g., logistic regression, random forest) to predict agricultural outcomes.

5. **Page 5: Forecasting**: Apply time series forecasting models (e.g., ARIMA or LSTM) to predict future trends in agricultural data.

6. **Page 6: Dashboard**: View an overview of the dataset, including visualizations for EDA, clustering, and forecasting results.

## Project Structure

The project is organized as follows:

smart-agriculture-monitoring/ 
├── app.py # Main Streamlit app file 
├── pages/ # Individual page files 
│ ├── 1_upload_data.py # Data upload page 
│ ├── 2_eda.py # EDA page 
│ ├── 3_clustering.py # Clustering page 
│ ├── 4_classification.py # Classification page 
│ └── 5_forecasting.py # Forecasting page 
├── src/ # Source code for utility functions 
│ ├── utils/ 
│ │ ├── data_loader.py # Data loading utility 
│ │ └── preprocessing.py # Data preprocessing utility 
├── requirements.txt # Python dependencies 
└── README.md # Project documentation