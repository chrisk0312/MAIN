import numpy as np
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN

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
model.add(SimpleRNN(units=10, input_shape = (3,1))) #timesteps, features
# 3-D tensor with shape (batch_size, timesteps, features).
model.add(Dense(32))
model.add(Dense(64))
model.add(Dense(128))
model.add(Dense(256))
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

# 6. 모델 예측
initial_sequence = np.array([8, 9, 10]).reshape(1, 3, 1)
predicted_values = []

for i in range(1,6):
    y_pred = model.predict(initial_sequence)
    predicted_values.append(y_pred[0,0])  # Extract the predicted value
    initial_sequence = np.concatenate([initial_sequence[:, 1:, :], y_pred.reshape(1, 1, 1)], axis=1)

print('Predicted values:', predicted_values)


# RNN (Recurrent Neural Network) is a type of artificial neural network designed to recognize patterns 
# in sequences of data, such as text, genomes, handwriting, or the spoken word. 
# Unlike feedforward neural networks, RNNs can use their internal state (memory) to process sequences of inputs, 
# which makes them ideal for such tasks.
# RNNs are called "recurrent" because they perform the same task for every element of a sequence,
# with the output being dependent on the previous computations.
# This recurrence relation makes them suitable for tasks where the current output depends not just on the current input,
# but also on a series of previous inputs.

# On the other hand, CNN, or Convolutional Neural Network, is a class of deep learning neural networks, most commonly applied to analyzing visual imagery. They are designed to automatically and adaptively learn spatial hierarchies of features from tasks with grid-like topology, such as an image.

# CNNs are composed of one or more convolutional layers, often with a subsampling layer, which are followed by one or more fully connected layers as in a standard multilayer neural network. The architecture of a CNN is designed to take advantage of the 2D structure of an input image (or other 2D input such as a speech signal).

# In summary, the main difference between RNNs and CNNs is that RNNs are typically used for sequential data while CNNs are used for grid-like data (such as images). Both are categories of neural networks and are used in different types of tasks based on the nature of the data and the problem at hand.