import numpy as np 
import torch 
import torch.nn as nn
import pkg_resources
import matplotlib.pyplot as plt

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
    

def predict(vector):
    
 
    
    vector1 = torch.tensor(vector[:-1], dtype=torch.int)

    model = NeuralNet(395, 10, 1)
    
    '''
    ######################  Training part #########################"

    resource_package = __name__
    resource_path = '/'.join(('', 'datasetFile.txt'))

    Xall_path = pkg_resources.resource_filename(resource_package, resource_path)
    dataset = np.loadtxt(fname=Xall_path, delimiter=',')

    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    X = train_size[:-1] # List of features 
    Y = train_size[-1] # Class (Malware / Legitimate)
    
    Y = Y.reshape(-1,1)
    X = X.reshape(-1,395)

    X1 = torch.tensor(X , dtype=torch.int)
    Y1 = torch.tensor(Y , dtype=torch.int)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.03)  
    num_epochs = 50
    Accuracy = []
    error = []
    for epoch in range(num_epochs):  # trains the NN 1,000 times
     
        outputs = model(X1.float())
        
        loss = criterion(outputs, Y1.float())
        error.append(loss.item())

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        b = outputs > 0.5 
        c = b.int()
        correct = (c == Y1).sum() 
        Accuracy.append(correct.item()/X1.shape[0])
        print("correct : ", X1.shape[0])
        print ('Epoch [{}/{}], Loss: {:.4f}, Accuracy : {:.4f}' 
            .format(epoch+1, num_epochs, loss.item(), correct.item()/X1.shape[0]))

    torch.save(model.state_dict(), "checkpoint.pth")
    index = list(range(1, num_epochs+1))
    print(index)
    plt.plot(index,error)
    plt.plot(index,Accuracy)
    plt.ylabel('Training Loss and Accuracy ')
    plt.show()

    '''
    model.load_state_dict(torch.load("checkpoint.pth"))
    model.eval()
    output = model(vector1.float())
    if output > 0.5 : 
        prediction = 1
    else : 
        prediction = 0 
    print(prediction)
    return prediction