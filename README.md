# Articles summarization & Entities extraction
![alt text](https://www.intellippt.com/blog/wp-content/uploads/2021/04/Summary.png)
### extracting custom entities and content summarization using NLP (spacy)
## How it works : 

  >The model script takes inputs (custom keywords text file) and (excel database) populated with some articles data and process them through the algorithm and export them back to the same file with the exctracted entities and summirization
## How to run : 
  >make sure you put your custom keywords in 'data\keywords.txt' and articles content in 'data\nlp_db.xlsx'
  - $ pip install -r requirements.txt
  - $ python setup.py
  - $ python main.py
