# CS331 Sentiment Analysis Assignment 3
# This file contains the processing functions
import pandas as pd
import os 

from classifier import BayesClassifier, accuracy

def load_data(train_file: str, test_file: str):
    """
    Loads the data from the text files
    Returns the data as a dataframe
    """
    
    # read in the data from the text files
    train_data = pd.read_csv(train_file, sep='\t', header=None, names=['text', 'label'])
    test_data = pd.read_csv(test_file, sep='\t', header=None, names=['text', 'label'])

    return train_data, test_data


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses all data stored in a pandas dataframe, loaded using the load_data functions
    """
    
    # remove all punctuation, symbols, and numbers from the text, including apostrophes, 
    data['preprocessed_text'] = data['text'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
    
    # convert all words to lowercase
    data['preprocessed_text'] = data['preprocessed_text'].str.lower()
    
    # split the text into a list of words
    data['tokens'] = data['preprocessed_text'].str.split()
    
    return data


def build_vocab(preprocessed_data: pd.DataFrame) -> list:
    """
    Builds the vocab from the preprocessed text
    preprocessed_text: output from process_text
    Returns unique text tokens
    """
    
    # initialize the vocab
    vocab = set()
    
    # loop through each text and add the tokens to the vocab
    for text in preprocessed_data['tokens']:
        for token in text:
            vocab.add(token)
    
    # sort the vocab
    vocab = list(vocab)
    vocab.sort()
    
    return vocab


def vectorize_text(data: pd.DataFrame, vocab: list) -> pd.DataFrame:
    """
    Converts the text into vectors
    text: preprocess_text from process_text
    label: 0 or 1
    vocab: vocab from build_vocab
    Returns the vectorized text and the labels
    """

    # create columb in dataframe labeled 'vectorized_text'
    data_vectorized = []
    for i, row in data.iterrows():
        vectorized_text = []
        tokens = set(row['tokens'])
        for token in vocab:
            if token in tokens:
                vectorized_text.append(1)
            else:
                vectorized_text.append(0)
        
        if len(vectorized_text) != len(vocab):
            raise ValueError("Length of vectorized text does not match length of vocab")
        
        data_vectorized.append(vectorized_text)
        
    data['vectorized_text'] = data_vectorized
    
    return data


def save_preprocessed_data(data: pd.DataFrame, vocab: list, file_name: str):
    """
    Saves the preprocessed data to a text file
    data: output from preprocess_data
    file_name: name of file to save to
    """
    
    # save the data to a text file
    with open(file_name, 'wt') as f:
        for token in vocab:
            f.write(f'{token},')
        f.write('classlabel\n')
        for i, text in data.iterrows():
            for token in text['vectorized_text']:
                f.write(f'{token},')
            f.write(f'{text["label"]}\n')


def load_preprocessed_data(file_name: str):
    """
    Loads the preprocessed data from a text file
    file_name: name of file to load from
    Returns the text vectors, labels, and vocab
    """
    
    # read in the data from the text file
    with open(file_name, 'r') as f:
        # read first line into list
        vocab = f.readline().split(',')[:-1]
        
        # iterate through the rest of the file
        data = []
        labels = []
        for line in f:
            line = line.split(',')
            data.append([int(x) for x in line[:-1]])
            labels.append(int(line[-1]))
            
    return data, labels, vocab


def main():
    
    # if the preprocessed data does not exist, create it
    if not (os.path.isfile('./train_preprocessed.txt') and os.path.isfile('./test_preprocessed.txt')):
        print("Preprocessed data does not exist. Creating...")
        # Take in text files and outputs sentiment scores
        train_data, test_data = load_data('./trainingSet.txt', './testSet.txt')
        
        # preprocess the training data
        train_data = preprocess_data(train_data)
        vocab = build_vocab(train_data)
        train_data = vectorize_text(train_data, vocab)
        
        # preprocess the test data
        test_data = preprocess_data(test_data)
        test_data = vectorize_text(test_data, vocab)
        
        # save the preprocessed data
        save_preprocessed_data(train_data, vocab, 'train_preprocessed.txt')
        save_preprocessed_data(test_data, vocab, 'test_preprocessed.txt')

    # load the preprocessed data
    print("Loading preprocessed data...")
    train_data, train_labels, vocab = load_preprocessed_data('train_preprocessed.txt')
    test_data, test_labels, _ = load_preprocessed_data('test_preprocessed.txt')

    # sentiment analysis
    print("Initializing Naive Bayes Classifier...")
    classifier = BayesClassifier(train_file='trainingSet.txt', test_file='testSet.txt')
    
    # fit model
    print("Fitting model...")
    classifier.train(train_data, train_labels, test_data, test_labels, vocab)
    
    # predict labels
    print("Predicting on training and test data...")
    train_predictions = classifier.classify_text(train_data, vocab)
    test_predictions = classifier.classify_text(test_data, vocab)
    
    # calculate accuracy
    train_accuracy = accuracy(train_predictions, train_labels)
    test_accuracy = accuracy(test_predictions, test_labels)
    
    # print accuracy
    print("Training Accuracy: ", train_accuracy)
    print("Test Accuracy: ", test_accuracy)
    
    return 1


if __name__ == "__main__":
    main()