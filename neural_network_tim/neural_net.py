import json
import pickle
import random

import nltk
import numpy as np
import tensorflow
import tflearn

from nltk.stem.lancaster import LancasterStemmer


stemmer = LancasterStemmer()

with open("intents.json") as intents_file:
    data = json.load(intents_file)

try:
    # Try to load pre-existing processed training and output data
    # Note: If you modify intents.json, delete data.pickle and
    # re-run this file!
    with open("data.pickle", "rb") as fob:
        words, labels, training, output = pickle.load(fob)
except:
    words = []
    labels = []
    # List of patterns
    docs_x = []
    # For every pattern, what intent it's a part of
    docs_y = []

    for intent in data["intents"]:
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

        # Stemming
        for pattern in intent["patterns"]:
            # Take each word that is in our pattern and strip it down to the
            # root word. For example:
            #   - "there?" becomes "there"
            #   - "what's" becomes "what"
            #
            # This step is helpful later when training our model. In training,
            # we only care about the meaning of the word, not anything extra
            # attached to it (i.e. extra characters like '?' or apostrophes.
            #
            # This step can make training more accurate, as we're ignoring
            # things that could otherwise steer the model in the wrong
            # direction.

            # Step 1: Tokenize
            # Get all the words in our pattern, separate them with something
            # like a space. nltk can do this for us.
            tokenized_words = nltk.word_tokenize(pattern)
            words.extend(tokenized_words)
            docs_x.append(tokenized_words)
            docs_y.append(intent["tag"])

    # Stem words and remove duplicate words
    # Lets us know how many words have we seen already, i.e. the
    # vocabulary size of the model.
    # Also remove "?" as we they often appear in sentences but we
    # don't want them to have any meaning in our model.
    # TODO: in future, maybe remove other stuff like "!" too?
    words = [stemmer.stem(word.lower()) for word in words if word != "?"]
    # Remove duplicates and sort alphabetically
    words = sorted(list(set(words)))

    labels = sorted(labels)

    # Create training and testing output
    #
    # Neural networks only understand numbers, not strings.
    # We'll create a "bag of words", telling us if a word occurd in a given
    # pattern. i.e. in a sentence.
    #
    # Also see: One-hot encoding: https://en.wikipedia.org/wiki/One-hot

    # Holds bags of words
    training = []
    # Same but for labels?
    output = []

    # "Template" list for one-hot encoding
    out_empty = [0 for _ in range(len(labels))]

    # Create bag of words
    for index, doc in enumerate(docs_x):
        # Bag of words, one-hot encoded
        bag = []

        stemmed_words = [stemmer.stem(word) for word in doc]

        for word in words:
            if word in stemmed_words:
                # If word occurs in pattern, add 1
                bag.append(1)
            else:
                bag.append(0)
        
        # Generate output - I think we're one-hot encoding the labels too
        # basically.
        # Copy out_empty, which is how a one-hot encoding list looks like but
        # with all 0s.
        output_row = out_empty[:]
        # Look through labels list and see where the tag is in the list
        # (remember docs_y holds every tag). Then set the corresponding index
        # in our one-hot encoding list to a 1.
        output_row[labels.index(docs_y[index])] = 1
        # Append this one-hot encoded list to our output list
        output.append(output_row)
        # Append bag of words to training list
        training.append(bag)

    # Need to work with numpy arrays for tflearn
    training = np.array(training)
    output = np.array(output)

    # Pickle and save training and output data so that we don't have to
    # pre-process it in future runs.
    with open("data.pickle", "wb") as fob:
        pickle.dump((words, labels, training, output), fob)

# Start building model with tflearn
# tflearn is similar to tensorflow
# tensorflow.reset_default_graph()
tensorflow.compat.v1.reset_default_graph()

# Define input shape that we're expecting for our model
net = tflearn.input_data(shape=[None, len(training[0])])
# Add fully connected layer to our neural network
# With 8 neurons for our first 2 hidden layers
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
# Output layer. softmax allows us to get probabilities for each output.
# Softmax goes through and gives us a probability for each neuron in
# this layer.
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# model = tflearn.DNN(net)

# Train our model
try:
    model = tflearn.DNN(net)
    # Don't train model if we already have a trained model from a previous run
    model.load("model.tflearn")
except:
    # Fit our model (pass it training data)
    model = tflearn.DNN(net)
    # model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.fit(training, output, n_epoch=10000, batch_size=8, show_metric=True)
    # Save model so that we can load it in future runs instead of re-training it
    # every run. Note that if your training data changes, you should re-run the
    # training. In that case, delete previous .tflearn files.
    model.save("model.tflearn")

# Start making predictions
# When we trained our model, we fed it bags of words. We also have to give
# bags of words to our model when we want to make a prediction.

# Turn a sentence input from the user into a bag of words
def bag_of_words(sentence, words):
    """
    Args:
        words: list of words (all the words we have in the json)
    """
    # Set up an empty bag for one-hot encoding
    bag = [0 for _ in range(len(words))]

    # Tokenize the words in the sentence
    tokenized_words = nltk.word_tokenize(sentence)
    # Stem our tokenized words
    stemmed_words = [stemmer.stem(word.lower()) for word in tokenized_words]

    for stemmed_word in stemmed_words:
        for index, word in enumerate(words):
            if word == stemmed_word:
                bag[index] = 1

    # Need to work with numpy arrays
    return np.array(bag)

def chat():
    print("Start talking (or /quit)")

    while True:
        msg = input("> ")
        if msg.lower() == "/quit" or msg.lower() == "/q":
            break

        # Turn the msg into a bag of words, feed it to the model
        # and get what the model's response would be.
        # This returns probablities for each label.
        # Tries to classify the user input and say how much it thinks
        # each neuron (each neuron represents a specific label).
        results = model.predict([bag_of_words(msg, words)])[0]

        # Pick out the greatest number/probability
        # Returns the index of the greatest value in our list
        results_index = np.argmax(results)
        # This index corresponds to an index in our labels list. So we
        # can use it to figure out the label!
        # print(results_index)
        tag = labels[results_index]
        # print(tag)

        # If the highest probablity is not high enough to be deemed acceptable
        # (for example, it's only 20% rather than 70% or above), then give
        # a generic response rather than assuming the predcition was correct.
        # Make the acceptable treshold 70%:
        if results[results_index] >= 0.7:
            # Get list of responses to the predicted tag
            for intent in data["intents"]:
                if intent["tag"] == tag:
                    responses = intent["responses"]
            # Pick a random response from the list of responses
            # print(responses[random.randint(0, len(responses))])
            print(random.choice(responses))
        else:
            # The probability for the prediction was lower than acceptable, so
            # give a generic response instead, rather than making a potentially
            # bad assumption.
            print("Soz, I dunt get it")

# chat()
def predict(sentence):
    # Turn the sentence into a bag of words, feed it to the model
    # and get what the model's response would be.
    # This returns probablities for each label.
    # Tries to classify the user input and say how much it thinks
    # each neuron (each neuron represents a specific label).
    results = model.predict([bag_of_words(sentence, words)])[0]
    # Pick out the greatest number/probability
    # Returns the index of the greatest value in our list
    results_index = np.argmax(results)
    # This index corresponds to an index in our labels list. So we
    # can use it to figure out the label!
    tag = labels[results_index]

    # If the highest probablity is not high enough to be deemed acceptable
    # (for example, it's only 20% rather than 70% or above), then give
    # a generic response rather than assuming the predcition was correct.
    # Make the acceptable treshold 70%:
    if results[results_index] >= 0.7:
        # Get list of responses to the predicted tag
        for intent in data["intents"]:
            if intent["tag"] == tag:
                responses = intent["responses"]
        # Pick a random response from the list of responses
        return random.choice(responses)
    else:
        # The probability for the prediction was lower than acceptable, so
        # give a generic response instead, rather than making a potentially
        # bad assumption.
        return None
        # print("Soz, I dunt get it")
