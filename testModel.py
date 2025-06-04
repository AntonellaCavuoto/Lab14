from model.model import Model

myModel = Model()
print(myModel.buildGraph(2, 5))
print(myModel.getLongestPath(10))
print(myModel.bestPath(10))