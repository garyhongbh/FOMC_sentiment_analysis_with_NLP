import pandas as pd
import re
df = pd.read_csv('FOMC_Draft.csv')

# Removal of unrelated paragraph
def Removal_paragraph(text):
    text = re.sub(r'Voting for the.*','',text)
    text = re.sub(r'For media inquiries.*','',text)
    text = re.sub(r'Implementation Note issued.*','',text)
    
    return text
df['text_clean'] = df['Text'].apply(lambda x: Removal_paragraph(x))


# Convert to lowercase
df['lowercase_text'] = df['text_clean'].str.lower()


#Lemmatization & POS Tagging
import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
wordnet_map = {"N":wordnet.NOUN, "V": wordnet.VERB,"J": \
               wordnet.ADJ, "R": wordnet.ADV}
def lemmatize_words(text):
    # find pos tags
    pos_text = pos_tag(text.split())
    return " ".join([lemmatizer.lemmatize(word,\
    wordnet_map.get(pos[0], wordnet.NOUN)) for word, pos in pos_text])

df['lemmatized_text'] = df['lowercase_text'].apply(lambda x: lemmatize_words(x))
df.head()


# Removal of Punction within the sentence

def remove_punctuations(text):
    punctuations = "\"#$%&'()*+-/:;<=>@[\]^_`{|}~"
    return text.translate(str.maketrans('', '', punctuations))

df['clean_text_1'] = df['lemmatized_text'].apply(lambda x: remove_punctuations(x))
df.head()


# Removal of Stopwords
from nltk.corpus import stopwords
# ", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in STOPWORDS])

df['clean_text_2'] = df['clean_text_1'].apply(lambda x: remove_stopwords(x))
df.head()

# Removal of Special characters
def remove_spl_chars(text):
    text = re.sub('[\d]', ' ', text)
    text = re.sub('\s+', ' ', text)
    return text

df['clean_text_3'] = df['clean_text_2'].apply(lambda x: remove_spl_chars(x))
df.head()

# # Removal of Frequent words
# from collections import Counter
# word_count = Counter()
# for text in df['clean_text']:
#     for word in text.split():
#         word_count[word] += 1
        
# FREQUENT_WORDS = set(word for (word, wc) in word_count.most_common(10))
# def remove_freq_words(text):
#     return " ".join([word for word in text.split() if word not in FREQUENT_WORDS])

# df['clean_text_4'] = df['clean_text_3'].apply(lambda x: remove_freq_words(x))
# df.head()


df.to_csv('FOMC_Clean.csv')
