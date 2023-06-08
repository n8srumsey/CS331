# This file implements a Naive Bayes Classifier
import matplotlib.pyplot as plt
import math
import numpy as np

def accuracy(predicted_labels: list, true_labels: list) -> float:
    """
    predicted_labels: list of 0/1s predicted by classifier
    true_labels: list of 0/1s from text file
    return the accuracy of the predictions
    """
    
    # error checking
    if len(predicted_labels) != len(true_labels):
        raise ValueError("Length of predicted labels and true labels must be the same")
    
    # calculate the accuracy
    pred = np.array(predicted_labels)
    true = np.array(true_labels)
    accuracy_score = sum(pred == true) / len(true)

    # return the accuracy
    return accuracy_score


class BayesClassifier():
    """
    Naive Bayes Classifier
    file length: file length of training file
    sections: sections for incremental training
    """
    def __init__(self, train_file, test_file):
        self.postive_word_counts = {}
        self.negative_word_counts = {}
        self.n_positive_scentences = 0
        self.n_negative_scentences = 0
        
        self.train_file = train_file
        self.test_file = test_file
        
    def train(self, train_data: list, train_labels: list, test_data: list, test_labels: list, vocab: list):
        """
        This function builds the word counts and sentence percentages used for classify_text
        train_data: vectorized text
        train_labels: vectorized labels
        vocab: vocab from build_vocab
        """
        
        # clear out previous report.txt
        open('report.txt', 'wt').close()
        
        
        # initialize word counts with Dirichlet priors
        for word in vocab:
            self.postive_word_counts[word] = 1
            self.negative_word_counts[word] = 1
        
        n_samples = len(train_data)
        n_partitions = 4
        partition_size = n_samples // n_partitions
        samples_fitted = 0
        
        samples_fitted_hist = []
        train_acc_list = []
        test_acc_list = []
        
        for i in range(n_partitions):
            partition = train_data[i * partition_size : (i + 1) * partition_size]
            labels = train_labels[i * partition_size : (i + 1) * partition_size]
            if i == n_partitions - 1:
                partition = train_data[i * partition_size : ]
                labels = train_labels[i * partition_size : ]
            p = i    
            for tokens, label in zip(partition, labels):
                samples_fitted += 1
                if label == 0:
                    self.n_negative_scentences += 1
                    for i, token in enumerate(tokens):
                        if token == 1:
                            self.negative_word_counts[vocab[i]] += 1
                elif label == 1:
                    self.n_positive_scentences += 1
                    for i, token in enumerate(tokens):
                        if token == 1:
                            self.postive_word_counts[vocab[i]] += 1
                        
            train_acc = self.evaluate(train_data, train_labels, vocab)
            test_acc = self.evaluate(test_data, test_labels, vocab)
            train_acc_list.append(train_acc)
            test_acc_list.append(test_acc)
            samples_fitted_hist.append(samples_fitted)
            
            self.report(p, n_partitions, train_acc, test_acc, samples_fitted)
        
        self.plot(samples_fitted_hist, train_acc_list, test_acc_list)
            

    def evaluate(self, data: list, labels: list, vocab: list) -> float:
        """
        data: vectorized text
        labels: vectorized labels
        vocab: vocab from build_vocab
        """
        predictions = self.classify_text(data, vocab)
        return accuracy(predictions, labels)

    def report(self, partition: int, n_partitions: int, train_acc: float, test_acc: float, samples_fitted: int):
        """
        train_acc: list of training accuracies
        test_acc: list of testing accuracies
        """
        
        with open('report.txt', 'a') as f:
            f.write(f'[Training Partition {partition+1}/{n_partitions}]\n')
            
            f.write(f'\tTraining ({self.train_file}):\n')
            f.write(f'\t\tAccuracy: {train_acc}\n')
            f.write(f'\t\t# Samples Fitted: {samples_fitted}\n')
            
            f.write(f'\tTesting ({self.test_file}):\n')
            f.write(f'\t\tAccuracy: {test_acc}\n')
            f.write('=======================================================\n')

    def plot(self, samples_fitted_list, train_acc: list, test_acc: list):
        """
        train_acc: list of training accuracies
        test_acc: list of testing accuracies
        """
        
        # Plot the training and testing accuracies vs # samples fitted on figures side by side
        # Save the figure as 'accuracy.png'
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(samples_fitted_list, train_acc)
        plt.xlabel("# Samples Fitted")
        plt.ylabel("Accuracy")
        plt.title("Training Accuracy")
        
        plt.subplot(1, 2, 2)
        plt.plot(samples_fitted_list, test_acc)
        plt.xlabel("# Samples Fitted")
        plt.ylabel("Accuracy")
        plt.title("Testing Accuracy")
        
        plt.savefig('accuracy.png')
        plt.show()
        

    def classify_text(self, vectors, vocab):
        """
        vectors: [vector1, vector2, ...]
        predictions: [0, 1, ...]
        """
        predictions: list = []
        for vector in vectors:
            if len(vector) != len(vocab):
                raise ValueError(f"Length of vectorized text ({len(vector)}) does not match length of vocab ({len(vocab)})")
            
            # calculate the logrithmic class priors
            positive_log_prior = math.log(self.n_positive_scentences / (self.n_negative_scentences + self.n_positive_scentences))
            negative_log_prior = math.log(self.n_negative_scentences / (self.n_negative_scentences + self.n_positive_scentences))
            
            
            probability_positive = positive_log_prior
            probability_negative = negative_log_prior
            for i, token in enumerate(vector):
                if token == 0:
                    continue
                else:
                    # calculate the logrithmic likelihood
                    probability_positive += math.log(self.postive_word_counts[vocab[i]])
                    probability_negative += math.log(self.negative_word_counts[vocab[i]])

            predictions.append(1 if probability_positive > probability_negative else 0)
            
        return predictions
    