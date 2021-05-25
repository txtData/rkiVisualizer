This script stores RKI's primary covid data (the case and death numbers that you see in the news every day) in Elasticsearch.
With the help of Kibana, the data can then interactively be explored.

![Screenshot](screenshot.png)

To run the script, first create a new Python environment with:
* conda install pandas
* conda install elasticseach
                         
Then follow these steps:
* Download RKI's latest covid data from here: https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0
* Place the downloaded file 'RKI_COVID19.csv' in the same folder as 'rki_indexer.py'
* Start Elasticsearch and Kibana, then run the script.
* You can start creating a Kibana dashboard here: http://localhost:5601/app/kibana#/home
