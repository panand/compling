Hi all. For this week, I'd like you to experiment with some simple language modeling.

Since there is a lot of data here, my advice is to start with a modest 1000 random POSTS and develop your code on that. When you are satisfied, you can enlarge to everything.

-- Generating simple LMs --

In this part, please compute unigram, bigram, and trigram probabilities from the MLE (i.e., from counts of the data).
If you'd like to try doing this in parallel with qsub, see that file. But I don't think you need to do that.

-- Generating text with LMs --

Now, construct some text with the LMs above. To do this, first choose a random word string of around 20 words (it can be exactly 20; I don't care). Choose an n-gram at random and then choose the best n-gram that overlaps with the previous n-gram. This will be sensible for 2+-grams, but for unigrams, such a strategy will be very uninteresting. Why?

If you have the time, try this for quadragrams. See if you are getting actual strings in the corpus by googling against the url 4forums.com.

--  Determining fit of an LM --

Now, compute how good a fit each LM is to the corpus. To do this, compute the overall log-likelihood of the corpus given probabilities estimated. Which one fares the best?

-- Implementing smoothing --

In the below problems, assume a trigram LM.

I. Implement add-lambda smoothing for 10 lambdas. Produce a table/graph of the log-likelihood by lambda value.

II. Now implement the 2-fold cross-validation model of Jelinek. This means you train on half, then re-estimate based on the held-out data. In doing this, we have to define a procedure to handle OOV terms. My suggestion here is to actually assume the total vocabulary throughout, so there are no OOV terms. 

III. Next, implement Witten-Bell. I've put some slides by Bill McCarthy in the slides directory, and these cover this method and Good-Turing really explicitly (i.e., the formulas are all there).

IV. Next, it's time for Good-Turing estimation. 

V. Finally, implement Katz backoff using Good-Turing. This is pretty involved. 

VI. At the end, you can compare these five LM models (including the best all-lambda) in terms of fit of the data and sentence generation.