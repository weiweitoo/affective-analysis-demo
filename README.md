# Affective Analysis Demo
Visit [here](http://www.hitoo.co/affective-analysis-demo/fyp-poster.pdf) for poster softcopy

## Abstract
Affective Analysis(AA) in language aims to understand and predict the affective context from a text corpus. Emotion ratings can be represented in different model and Emotion Representation Mapping (ERM) are aim to convert an emotion rating from one representation schema into another one, e.g., mapping from VAD emotion to categorical emotion and vice versa. However, existing work is lack of using state-ofthe-art architecture, transformer and attention mechanism in Affective Analysis task and Emotion Representation Mapping task. Thus, we are here to purpose the use of Transformer and LSTM architecture to complete affective analysis task in narrative story domain and describe the emotion ratings in both VAD emotion schema and categorical emotion schema. Also, we present the first use of attention-mechanism approach to perform Emotion Representation Mapping(ERM) where it maps emotion from Valence-Arousal-Dominance schema to categorical schema and proven that attention-mechanism helps to achieve the SOTA performance especially when the mapping is performed under complicated situation such as cross-lingual or sentencelevel instead of word-level. Equally important, we project this work to be the first to experiment on how ERM concept can be applied in affective analysis task as well.

## Objective
1. Use of attention mechanism in Emotion Representation Mapping task and from complex VAD emotion to 8 category 
2. Propose an architecture based on the state-of-the-art architecture to perform Affective Analysis(Both Dimensional Space and Categorical Space) in narrative story domain and declared as benchmark result.
3. Experiment the use of emotion representation mapping concept in affective analysis task

# TechStack
* Tensorflow 2.0
* Flask
* VueJS
* ElementUI