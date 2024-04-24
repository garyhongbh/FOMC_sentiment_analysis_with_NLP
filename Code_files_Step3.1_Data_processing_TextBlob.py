from textblob import TextBlob
import pandas as pd

# Read data from the CSV file
df = pd.read_csv('FOMC_Clean.csv')
# The text column name for reading data from the CSV file is "clean_text_3"
text_list = df['clean_text_3'].tolist()

# Calculate the sentiment scores and the number of sentences for each text
def get_sentence_sentiment_scores(text_list):
    sentence_sentiment_scores = []
    sentence_counts = []
    for text in text_list:
        # Split the text into sentences
        text_with_periods = text.replace('.', '. ')
        print(text_with_periods)
        sentences = TextBlob(text_with_periods).sentences
        print(sentences)
        sentence_counts.append(len(sentences))
        # Calculate sentiment scores for each sentence and add them to the list
        for sentence in sentences:
            sentiment_score = sentence.sentiment.polarity
            sentence_sentiment_scores.append(sentiment_score)
    return sentence_sentiment_scores, sentence_counts

# Get the sentiment scores for each sentence and the count of sentences for each text
sentence_scores, sentence_counts = get_sentence_sentiment_scores(text_list)

avg_sentiment_scores = []
start_index = 0
for count in sentence_counts:
    end_index = start_index + count
    avg_score = sum(sentence_scores[start_index:end_index]) / count
    avg_sentiment_scores.append(avg_score)
    start_index = end_index

result_df = pd.DataFrame({'Text': range(1, len(avg_sentiment_scores) + 1),
                          'Average_Sentiment_Score': avg_sentiment_scores})
result_df.to_csv('Sentiment_Scores_TextBlob.csv', index=False)
