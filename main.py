import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from textblob import TextBlob

# Header.
st.header('Sentiment Analysis')
# Analyze Text Expander.
with st.expander('Analyze Text'):
    text = st.text_input('Text here: ')
    if text:
        blob = TextBlob(text)
        st.write('Polarity: ', round(blob.sentiment.polarity, 2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity, 2))

# CSV Expander.
with st.expander('Analyze CSV'):
    uploaded_file = st.file_uploader('Choose a csv file', type='csv')

    # Analyzing polarity of large reviews in csv file.
    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity


    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'


    if uploaded_file:
        st.markdown('---')
        df = pd.read_csv(uploaded_file, )
        st.dataframe(df)
        df['score'] = df['reviews'].apply(score)
        df['analysis'] = df['score'].apply(analyze)
        st.write(df.head(5000))

        # Download Button
        st.download_button(
            label="Download data as excel",
            data=df.to_csv(index=False),
            file_name='sentiment.csv',
            mime='text/csv',
        )

analysis_counts = df['analysis'].value_counts()

# Inside your Streamlit app
with st.expander('Plot polarity'):
    fig, ax1 = plt.subplots()

    # Plotting the histogram
    plt.bar(analysis_counts.index, analysis_counts.values, color=['grey', 'green', 'red'])
    plt.xlabel('Sentiment Analysis')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis Distribution')
    st.pyplot(fig)
