import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import multiprocessing
import concurrent.futures
import nltk
import os
import concurrent.futures
import pandas as pd
import logging
from syllapy import _syllables
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict
print(nltk.data.path)
nltk.download('punkt')
nltk.download('cmudict')
from nltk.corpus import cmudict
cmudict.ensure_loaded()


def read_stopwords_files(StopWords, encoding='latin-1'):
    stopwords = []
    for filename in os.listdir(StopWords):
        file_path = os.path.join(StopWords, filename)
        with open(file_path, 'r', encoding=encoding) as file:
            stopwords.extend(file.read().splitlines())
    return set(stopwords)

stopwords_folder = 'StopWords'  # Folder containing stopwords files
project_directory = os.getcwd()  # Current project directory
stopwords_directory = os.path.join(project_directory, stopwords_folder)
stopwords = read_stopwords_files(stopwords_directory)
# print(stopwords)

positive_words_file = "/Users/jasmeet/PycharmProjects/pythonProject2/MasterDictionary/positive-words.txt"  # Replace with the path to your positive words file
negative_words_file = "/Users/jasmeet/PycharmProjects/pythonProject2/MasterDictionary/negative-words.txt"  # Replace with the path to your negative words file

with open(positive_words_file, 'r') as f:
    positive_words = set(f.read().splitlines())

with open(negative_words_file, 'r', encoding='latin-1') as f:
    negative_words = set(f.read().splitlines())

def clean_text(text, stopwords):
    words = word_tokenize(text)
    cleaned_words = [word.lower() for word in words if word.lower() not in stopwords]
    return cleaned_words

def sentiment_scores(text, positive_words, negative_words):
    positive_score = sum(1 for word in text if word in positive_words)
    negative_score = sum(1 for word in text if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(text) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score

def count_syllables(word):
    return _syllables(word)



def average_sentence_length(text):
    sentences = sent_tokenize(text)
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    total_sentences = len(sentences)
    return total_words / total_sentences

def percentage_complex_words(text):
    words = word_tokenize(text)
    complex_words = [word for word in words if count_syllables(word) > 2]
    return (len(complex_words) / len(words)) * 100
def fog_index(average_sentence_length, percentage_complex_words):
    return 0.4 * (average_sentence_length + percentage_complex_words)

def average_words_per_sentence(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    return len(words) / len(sentences)

def count_complex_words(text):
    words = word_tokenize(text)
    return sum(1 for word in words if count_syllables(word) > 2)

def count_total_words(text):
    words = word_tokenize(text)
    return len(words)

def syllable_count_per_word(text):
    words = word_tokenize(text)
    syllable_count = sum(count_syllables(word) for word in words)
    total_words = len(words)
    return syllable_count / total_words

def count_personal_pronouns(text):
    personal_pronouns = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    words = word_tokenize(text)
    return sum(1 for word in words if word.lower() in personal_pronouns)

def average_word_length(text):
    words = word_tokenize(text)
    total_characters = sum(len(word) for word in words)
    total_words = len(words)
    return total_characters / total_words


output_data = []

logging.basicConfig(level=logging.INFO)
def process_file(file_name):
    global negative_score
    logging.info(f"Processing file: {file_name}")
    try:
        with open(file_name, 'r') as file:
            text = file.read()
        cleaned_text = clean_text(text, stopwords)
        positive_score, negative_score, polarity_score, subjectivity_score = sentiment_scores(cleaned_text, positive_words, negative_words)
        avg_sentence_length = average_sentence_length(text)
        pct_complex_words = percentage_complex_words(text)
        fog = fog_index(avg_sentence_length, pct_complex_words)
        avg_words_per_sentence = average_words_per_sentence(text)
        complex_word_count = count_complex_words(text)
        total_word_count = count_total_words(text)
        syllables_per_word = syllable_count_per_word(text)
        personal_pronouns = count_personal_pronouns(text)
        avg_word_length = average_word_length(text)
        # print(f"Cleaned Text for {file_name}: {' '.join(cleaned_text)}")

        file_data = {
            'File Name': file_name,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'Average Sentence Length': avg_sentence_length,
            'Percentage of Complex Words': pct_complex_words,
            'Fog Index': fog,
            'Average Number of Words Per Sentence': avg_words_per_sentence,
            'Complex Word Count': complex_word_count,
            'Total Word Count': total_word_count,
            'Syllable Count Per Word': syllables_per_word,
            'Personal Pronouns Count': personal_pronouns,
            'Average Word Length': avg_word_length
        }

        # Append the dictionary to the list
        output_data.append(file_data)

        logging.info(f"File processed successfully: {file_name}")
        print(f"Processed file: {file_name}")
        print(f"Positive Score: {positive_score}")
        print(f"Negative Score: {negative_score}")
        print(f"Polarity Score: {polarity_score}")
        print(f"Subjectivity Score: {subjectivity_score}")
        print(f"Average Sentence Length: {avg_sentence_length}")
        print(f"Percentage of Complex Words: {pct_complex_words}")
        print(f"Fog Index: {fog}")
        print(f"Average Number of Words Per Sentence: {avg_words_per_sentence}")
        print(f"Complex Word Count: {complex_word_count}")
        print(f"Total Word Count: {total_word_count}")
        print(f"Syllable Count Per Word: {syllables_per_word}")
        print(f"Personal Pronouns Count: {personal_pronouns}")
        print(f"Average Word Length: {avg_word_length}")
        print('done')
    except Exception as e:
        logging.error(f"Error processing file {file_name}: {str(e)}")

        # print(f"For File {file_name}:")
        print("Error:", e)

        # print("Cleaned Text(before joining):", cleaned_text)



if __name__ == "__main__":
    # num_cpus = multiprocessing.cpu_count()
    file_names = sorted([filename for filename in os.listdir() if filename.startswith('blackassign') and filename.endswith('.txt')])

    # num_workers = 8


    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    #     executor.map(process_file, file_names)
    for file_name in file_names:
        process_file(file_name)

    df = pd.DataFrame(output_data)

    # Save the DataFrame to an Excel file
    df.to_excel('output.xlsx', index=False)


