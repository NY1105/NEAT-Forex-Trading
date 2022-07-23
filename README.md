# Deep Learning Trading

> "If it works, it is not online."

This project utilizes NeuroEvolution of Augmenting Topologies (NEAT) algorithm to create Artificial Feed Foward Neural Networks. 

## Installation

	pip install -r requirements.txt

## Usage

Enter your prefered training pair and period in `getdata.py` and run it for fetching data.

Enter your prefered settings in `main.py` (recommended training to testing ratio is 4:1), and run it for training and testing the trained Neural Network. 

## Experimental design

### Data
The project examines the profit of 'EURUSD' and is capable for other forex currencies pairs over a variable period with 1 minute timeframe.

### Trading Window
To prevent overfitting, we deployed a sliding-window evaluation approach. This approach forms several overlapping study periods, each of which contains a training and a test window. In each study period, models are estimated on the training data and generate predictions for the test data, which facilitate model assessment. Subsequently, the study period is shifted by the length of one test period.
![SlidingWindow](/img/SlidingWindow.png)

### Generations and Genomes
With the sliding-window approach, there will be infinite generations until the trading window reached the selected datetime as an end. Each generations will have 50 genomes as default.

### Inputs
The current model intake the percentage change of close prices and percentage change of volumes in the past 15 minutes.

### Activation functions
We train the FNN using a rectified linear unit (relu) activation function. 

## Results
![Result](/img/Graph1.png)
![Result](/img/Graph2.png)
![Result](/img/Graph3.png)
![Report](/img/StartTrain.png)
![Report](/img/Train.png)
![Report](/img/TrainReport.png)
![Report](/img/BuySell.png)

## References
[# NEAT-Python Overview](https://neat-python.readthedocs.io/en/latest/neat_overview.html)
[# Forex exchange rate forecasting using deep recurrent neural networks](https://link.springer.com/article/10.1007/s42521-020-00019-x)
[# Machine Learning vs. the Forex Market](https://youtu.be/_dWRo05gHbA)
[# Python Pong AI Tutorial - Using NEAT](https://youtu.be/2f6TmKm7yx0)