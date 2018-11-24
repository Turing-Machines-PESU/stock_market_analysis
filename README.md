# stock_market_analysis

Created: 25 September 2018

<h4>A brief overview of the project is available at an alternate site. Please click on the image :</h4>
<a href="http://www.youtube.com/watch?feature=player_embedded&v=OMjrD539SFk
" target="_blank"><img src="http://img.youtube.com/vi/OMjrD539SFk/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="400" height="250" border="10" /></a>


<h4> To the run the project</h4>

```
python GUI/GUI.py
```

<b>Data Acquisition Sources:</b>
<ol>
  <li>https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs</li>
  <li>https://trendogate.com/     [Scrapped the required data] </li>
  <li>https://www.nasdaq.com/screening/company-list.aspx         [Details on companies and Symbol list]</li>
</ol>

<b>Preprocessed datasets:</b>
<ol>
  <li>[ Compressed Dataset ]( https://drive.google.com/file/d/19Srw3pxNe1S01X_Q5qj19ADAh8egwNTl/view?usp=sharing ) </li>
  <li>[ Uncompressed CSV ]( https://drive.google.com/file/d/1N-FCUykn-t9pmbdBZH9HcUhrmqflgP9a/view?usp=sharing )</li>
</ol>

<h2>Progress:</h2>
<ol>
  <li> <b>25 September 2018:</b> Created the repository. Added datasets and scripts. </li>
  <li><b>27 September 2018:</b> Literature survey on required python packages and preprocessing on the text data from the trending topics</li>
  <li><b>9 October 2018:</b> Analysis of twitter data</li>
  <li><b>13 October 2018:</b> Added working prototype of newly designed graph "TextoGram" [to branch textogram_prototype]</li>
  <li><b>14 October 2018:</b> Advanced Analysis on Xerox Inc and comparision with Google Inc. Fitted ARIMA model. Failed attempt to develop interesting insights.</li>
  <li><b>14 October 2018:</b> Preprocessed the Company data and Filtered out irrelevant data</li>
  <li><b>14 October 2018:</b> Basic Summary Statistics on Company Data</li>
  <li><b>10 November 2018:</b> Segmentation of the hashtags and basic text preprocessing.</li>
  <li><b>12 November 2018:</b> Basic work on GUI.(Testing phase as of 13 Nov)</li>
  <li><b>13 November 2018:</b> Basic Forecasting. LSTM, Linear Regression.</li>
  <li><b>15 November 2018:</b> Design GUI Screens. Finalise Pipeline.</li>
  <li><b>18 November 2018:</b> Modularization and Integration. </li>
  <li><b>20 November 2018:</b> Bug Fixing and Debugging.</li>
  <li><b>21 November 2018:</b> GUI Integration. Video Recording. Editing.</li>
  <li><b>22 November 2018:</b> First draft of the Report.</li>
  <li><b>23 November 2018:</b> Finalize report. Testing and Debugging.</li>
</ol>

<b>To install the required packages</b>
```
  pip install -r requirements.txt
```
<b> ** Please note that not all packages can be installed from the above command. If encountered with an error please manually install  the package from the list in the requirements.txt.</b>

<h4> Project Structure </h4>

Please maintain the project structure as follows [After downloading the dataset]:
        .
 ```
  ├── _config.yml
  ├── datasets
  │   ├── Companies
  │   │   ├── companylist (1).csv
  │   │   ├── companylist (2).csv
  │   │   └── companylist.csv
  │   ├── companies_stocks.csv
  │   ├── filtered_companies.csv
  │   ├── hashtags.csv
  │   ├── regions.csv
  │   ├── segmented_tags.csv
  │   ├── twitter.csv
  │   ├── words_dates_list_cw.csv
  │   └── words_dates_list_gnrl.csv
  ├── Dickey Fuller Test and Filters.ipynb
  ├── ETFs
  ├── Forecasting
  │   ├── advanced_analysis_xerox.ipynb
  │   ├── Basic_prediction_with_lstm.ipynb
  │   ├── company_preprocessed_data.csv
  │   ├── Forecasting using Auto Arima.ipynb
  │   ├── LinearRegressionModel.py
  │   ├── lstm.py
  │   ├── preprocess_data.py
  │   ├── stock_data.py
  │   └── visualize.py
  ├── GUI
  │   ├── graph_images
  │   ├── GUI.ipynb
  │   ├── GUI.py
  │   └── loading.jpg
  ├── index.md
  ├── modules
  │   ├── basic.py
  │   └── forecast.py
  ├── packages.txt
  ├── README.md
  ├── requirements.txt
  ├── scripts
  │   ├── hashtags_segmentation.py
  │   ├── mergestocks.py
  │   ├── process_companies.py
  │   ├── regions_scrape.py
  │   ├── seg_tags_preprocess.py
  │   ├── twitterscrape.py
  │   └── update_companies.py
  ├── stock_notes.txt
  ├── Stocks
  ├── Understanding_companies_stocks.py
  ├── Understanding_Dataset.ipynb
  ├── Understanding_Dataset.py
  ├── Understanding_stocks.ipynb
  ├── understanding_twitter_dataset.ipynb
  └── understanding_twitter_dataset.py
```
<h4> The folders ./ETFs and ./Stocks are not completely necessary but few modules may not work in their absence<h4>
  
  
