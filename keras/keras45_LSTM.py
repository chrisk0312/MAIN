import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN, LSTM

#1. 데이터 
datasets = np.array([1,2,3,4,5,6,7,8,9,10])

x = np.array([[1,2,3],
              [2,3,4],
              [3,4,5],
              [4,5,6],
              [5,6,7],
              [6,7,8],
              [7,8,9],]
             )

y = np.array([4,5,6,7,8,9,10])
print(x.shape, y.shape) #(7, 3) (7,)
x = x.reshape(7,3,1)
print(x.shape, y.shape) #(7, 3, 1) (7,)


# 행무시(데이터 갯수) 열우선
#2
model =  Sequential()
#model.add(SimpleRNN(units=10, input_shape = (3,1))) #timesteps, features
# 3-D tensor with shape (batch_size, timesteps, features).
model.add(LSTM(units=10, input_shape = (3,1))) #timesteps, features
model.add(Dense(7, activation='relu'))
model.add(Dense(1))

#3
model.compile(loss = 'mse', optimizer='adam')
model.fit(x,y, epochs=1000)

#4
results =  model.evaluate(x,y)
print('loss', results)
y_pred = np.array([8,9,10]).reshape(1,3,1)
y_pred = model. predict(y_pred)
print('[8,9,10]의 결과', y_pred)

# LSTM(Long Short-Term Memory) is a type of Recurrent Neural Network (RNN) architecture. 
# It was designed to overcome the problem of vanishing and exploding gradients in traditional RNNs, 
# which makes it difficult for such networks to learn from long sequences of data.
# LSTMs introduce the concept of a "cell state," or a horizontal line running through the top of the diagram of the network.
# This allows information to be carried across many time steps, essentially providing the network with some form of memory. 
# This makes LSTMs particularly effective for tasks involving sequences of data 
# where context from earlier in the sequence may be informative for processing later parts of the sequence.
