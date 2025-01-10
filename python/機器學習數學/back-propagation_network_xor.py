import numpy as np


def sigmoid(x): #sigmoid函數
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x): #sigmoid微分
    return x * (1 - x)

train_data_input = np.zeros((100 ,2), dtype=np.int32)
train_data_output = np.zeros((100 ,1), dtype=np.int32)
test_data_input = np.zeros((100 ,2), dtype=np.int32)
test_data_output = np.zeros((100 ,1), dtype=np.int32)

def calculate_accuracy(data_input, data_output, weights_input_to_hidden, bias_hidden, weights_hidden_to_output, bias_output):

    # 向前傳播
    hidden_layer_input = np.dot(data_input, weights_input_to_hidden) + bias_hidden
    hidden_layer_output = sigmoid(hidden_layer_input)
    
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_to_output) + bias_output
    predicted_output = sigmoid(output_layer_input)

    predicted_classes = (predicted_output > 0.5).astype(int)  #predicted值以0.5為界線分成0或1
    accuracy = np.mean(predicted_classes == data_output)  #計算正確率

    return accuracy

for i in range(100): #生成訓練資料集和測試資料集
    train_data_input[i][0] = np.random.randint(0, 2)  #生成0或1
    train_data_input[i][1] = np.random.randint(0, 2)
    test_data_input[i][0] = np.random.randint(0, 2)
    test_data_input[i][1] = np.random.randint(0, 2)
    train_data_output[i] = (train_data_input[i][0] ^ train_data_input[i][1]) #計算xor
    test_data_output[i] = (test_data_input[i][0] ^ test_data_input[i][1])

input_neurons = 2  #input layer神經元數
hidden_neurons = 6 #hidden layer神經元數，可調整
output_neurons = 1 #output layer神經元數
learning_rate = 0.3

weights_input_to_hidden = np.random.uniform(-1, 1, (input_neurons, hidden_neurons)) #隨機初始weight，範圍-1到1
weights_hidden_to_output = np.random.uniform(-1, 1, (hidden_neurons, output_neurons))
bias_hidden = np.zeros((hidden_neurons)) #初始bias，數值0
bias_output = np.zeros((output_neurons))

epochs = 200 #訓練次數，可調整

for i in range(epochs):
    #前向傳播
    hidden_layer_input = np.dot(train_data_input, weights_input_to_hidden) + bias_hidden
    hidden_layer_output = sigmoid(hidden_layer_input)
    
    output_layer_input = np.dot(hidden_layer_output, weights_hidden_to_output) + bias_output
    predicted_output = sigmoid(output_layer_input)

    error = train_data_output - predicted_output #計算誤差

    #反向傳播
    delta_predicted_output = error * sigmoid_derivative(predicted_output)
    error_hidden_layer = np.dot(delta_predicted_output, weights_hidden_to_output.T) #.T是轉置矩陣
    delta_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_layer_output)

    #更新weight和bias
    weights_hidden_to_output += np.dot(hidden_layer_output.T, delta_predicted_output) * learning_rate
    weights_input_to_hidden += np.dot(train_data_input.T, delta_hidden_layer) * learning_rate
    bias_output += np.sum(delta_predicted_output, axis=0) * learning_rate
    bias_hidden += np.sum(delta_hidden_layer, axis=0) * learning_rate

    if i % 10 == 0:
        loss = np.mean(np.abs(error))

        #用訓練資料集測試正確率
        train_accuracy = calculate_accuracy(
            train_data_input, train_data_output, 
            weights_input_to_hidden, bias_hidden, 
            weights_hidden_to_output, bias_output
        )
        
        #用測試資料集測試正確率
        test_accuracy = calculate_accuracy(
            test_data_input, test_data_output, 
            weights_input_to_hidden, bias_hidden, 
            weights_hidden_to_output, bias_output
        )
        print(f"Epoch {i}, Loss: {loss:.4f}, train accuracy: {train_accuracy * 100:.2f}%, test accuracy: {test_accuracy * 100:.2f}%")

#顯示訓練結果
print("hidden layer 到 output layer 權重")
print(weights_hidden_to_output)
print("input layer 到 hidden layer 權重")
print(weights_input_to_hidden)
print("output layer 偏置")
print(bias_output)
print("hidden layer 偏置")
print(bias_hidden)

#用訓練資料集測試正確率
train_accuracy = calculate_accuracy(
    train_data_input, train_data_output, 
    weights_input_to_hidden, bias_hidden, 
    weights_hidden_to_output, bias_output
)

#用測試資料集測試正確率
test_accuracy = calculate_accuracy(
    test_data_input, test_data_output, 
    weights_input_to_hidden, bias_hidden, 
    weights_hidden_to_output, bias_output
)

print(f"訓練資料集正確率: {train_accuracy * 100:.2f}%, 測試資料集正確率: {test_accuracy * 100:.2f}%")


