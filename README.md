# Install dependencies
The python version used when developing this prototype was 3.7.    
to install requirements execute the following commands

```
pip install -r requirements.txt
python -m spacy download fr_core_news_lg
```
# Usage
To run the prototype execute the following command in the main directory (pseudonumisation)
```
python app.py
```
Then go to [http://127.0.0.1:8050/](http://127.0.0.1:8050/)
# References
+ [Dash documentation](https://dash.plotly.com/introduction)
+ [Spacy matcher](https://spacy.io/api/matcher)
+ [analyses-trails-in-france-prenoms-hf.csv (for name pseudonymisation)](https://www.data.gouv.fr/fr/datasets/liste-de-prenoms/#community-resources)
