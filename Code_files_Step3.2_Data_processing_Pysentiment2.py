from textblob import TextBlob
import pandas as pd
import pysentiment2 as ps


# Read data from the CSV file---pd.read_csv(path)
df = pd.read_csv('FOMC_Clean.csv')
# The text column name for reading data from the CSV file is "clean_text_3"
text_list = df['clean_text_3'].tolist()

lm = ps.LM()

def fin_sentiment(sentence):
    tokens = lm.tokenize(sentence)
    score = lm.get_score(tokens)
    return score

# Calculate the sentiment scores and the number of sentences for each text
def get_sentence_sentiment_scores(text_list):
    sentence_sentiment_scores = []
    sentence_counts = []
    sentence_length = []

    for text in text_list:
        # Split the text into sentences
        text_with_periods = text.replace('.', '. ')
        # Get all sentences in one FOMC statement
        sentences = TextBlob(text_with_periods).sentences
        # Count number of sentences in one FOMC statement
        sentence_counts.append(len(sentences))

        # Calculate sentiment scores for each sentence and add them to the list
        for sentence in sentences:
            sentiment_score = fin_sentiment(str(sentence))
            sentence_length.append(len(sentence))

            # Locate poliarty score from dictionary, then calculate sentiment
            # using length of sentiment as weight
            sentiment_score = len(sentence)*(list(sentiment_score.values())[2])
            sentence_sentiment_scores.append(sentiment_score)
            
    return sentence_sentiment_scores, sentence_counts, sentence_length

# Get the sentiment scores for each sentence and the count of sentences for each text
sentence_scores, sentence_counts, sentence_length = get_sentence_sentiment_scores(text_list)

avg_sentiment_scores = []
start_index = 0

for count in sentence_counts:
    end_index = start_index + count
    sumLength = sum(sentence_length[start_index:end_index + 1])

    # Calculate weighted average score for the speech of each FOMC statement
    avg_score = sum(sentence_scores[start_index:end_index]) / sumLength
    avg_sentiment_scores.append(avg_score)
    start_index = end_index

avg_sentiment_scores

result_df = pd.DataFrame({'Text': range(1, len(avg_sentiment_scores) + 1),
                          'Average_Sentiment_Score': avg_sentiment_scores})
result_df.to_csv('Sentiment_Scores.csv', index=False)
