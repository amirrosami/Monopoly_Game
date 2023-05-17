
from enum import Enum
import copy
from random import randint
class NodeTypes(Enum):
    Max=1
    Chance=2
    Min=3


class Action:
    def __init__(self,name:str,id:int) -> None:
        self.Name=name
        self.Id=id

class Property:
    def __init__(self,position:int,name:str,owner:int,hastax:bool,price:int,rentprice:int):
        self.HasTax:bool=hastax 
        self.Name:str=name
        self.Price:int=price
        self.RentPrice:int=rentprice
        self.Position:int=position  
        self.Owner=owner  # agentId || null

#define properties and actions:
Properties:list[Property]=[
    Property(0,"Start",None,False,0,0),
    Property(1,"salmas",None,False,200,100),
    Property(2,"tabriz",None,False,200,100),
    Property(3,"Airport",None,False,300,100),
    Property(4,"Electric Company",None,False,400,100),
    Property(5,"prison",None,True,200,0),
    Property(6,"shiraz",None,False,200,100),
    Property(7,"tehran",None,False,200,100),
    Property(8,"mashhad",None,False,200,100),
    Property(9,"zanjan",None,False,200,100),
]

#StateTypes=["max","chancemin","min","chancemax"]


##############################################

class  Agent:
    def __init__(self,type:str,id:int,name:str,position:int,cash:int,properties:list[Property]=[]):
       self.Type=type #human or robot
       self.Id=id
       self.Name=name
       self.cash=cash
       self.Properties=properties
       self.Position=position
       
   




class State:
    def __init__(self,agent1:Agent,agent2:Agent,properties:list[Property]):
        self.Agent1=agent1  
        self.Agent2=agent2
        self.Properties=properties


    def printState(self):
        print("*********state*********")
        print("agent1.position: ",self.Agent1.Position)
        print("agent1.cash: ",self.Agent1.cash)
        agent1props=[]
        for prop in self.Agent1.Properties:
            agent1props.append((prop.Name,prop.Position))
        print("agent1.propeties: ",agent1props)
        
        #agent2
        print("agent2.position: ",self.Agent2.Position)
        print("agent2.cash: ",self.Agent2.cash)
        agent2props=[]
        for prop in self.Agent2.Properties:
            agent2props.append((prop.Name,prop.Position))
        print("agent2.propeties: ",agent2props)
        
        
        
    def IsTerminal(self):
        if self.Agent1.cash<=0 or self.Agent2.cash <=0 :
            return True

    def GetBuyState(self,player:str):
        agent1=copy.deepcopy(self.Agent1)
        agent2=copy.deepcopy(self.Agent2)
        properties=copy.deepcopy(self.Properties)
        if player=="human":
            currentproperty=copy.deepcopy(properties[agent1.Position])
            agent1.cash=agent1.cash - currentproperty.Price
            agent1.Properties.append(currentproperty)
            properties[agent1.Position].Owner=agent1.Id
            
        elif player=="max":
            currentproperty=copy.deepcopy(properties[agent2.Position])
            agent2.cash=agent2.cash - currentproperty.Price
            agent2.Properties.append(currentproperty)
            properties[agent2.Position].Owner=agent2.Id
            
            
        return State(agent1,agent2,properties)

            
        
        
    def GetSellState(self,player:str):
        agent1=copy.deepcopy(self.Agent1)
        agent2=copy.deepcopy(self.Agent2)
        properties=copy.deepcopy(Properties)
        if player=="max":
            agent2.cash =agent2.cash + (properties[agent2.Position].Price *.9)
            Properties[agent2.Position].Owner==None
        elif player=="human":
            agent1.cash =agent1.cash + (properties[agent1.Position].Price *.9)
            properties[agent1.Position].Owner==None
        return State(agent1,agent2,properties)
    
    def GetRentState(self,player:str):
        agent1=copy.deepcopy(self.Agent1)
        agent2=copy.deepcopy(self.Agent2)
        if player =="human":
            agent1.cash -= Properties[self.Agent1.Position].RentPrice
            agent2.cash +=Properties[self.Agent1.Position].RentPrice
        elif player=="max":
            agent2.cash -= Properties[self.Agent2.Position].RentPrice
            agent1.cash +=Properties[self.Agent2.Position].RentPrice

        return State(agent1,agent2,copy.deepcopy(Properties))

    
      
    def GetDoNothingState(self):
        agent1=copy.deepcopy(self.Agent1)
        agent2=copy.deepcopy(self.Agent2)
        newproperties=copy.deepcopy(self.Properties)
        return State(agent1,agent2,newproperties)
      
    def GetChanceState(self,chancetype,roll:int):
        agent1=copy.deepcopy(self.Agent1)
        agent2=copy.deepcopy(self.Agent2)
        newproperties=copy.deepcopy(self.Properties)
        if chancetype=="chancemax":
            agent2.Position =(agent2.Position + roll)%len(Properties)
        elif chancetype=="chancemin":
            agent1.Position =(agent1.Position + roll)%len(Properties)

        return State(agent1,agent2,newproperties)
        
        
    
    
    def get_successors(self,StateType):
        successors:list[State]=[]
        if StateType=="chancemin":
            for i in range(1,7):
                successors.append([self.GetChanceState("chancemin",i),"roll{0}".format(i)])
        elif StateType=="chancemax":
            for i in range(1,7):
                successors.append([self.GetChanceState("chancemax",i),"roll{0}".format(i)])
        elif StateType=="max":
            currentproperty=Properties[self.Agent2.Position]
            if  currentproperty.Owner==self.Agent1.Id:
                successors.append([self.GetRentState("max"),"rent"])
                return successors
            elif self.Agent2.cash >= currentproperty.Price  and currentproperty.Owner==None and currentproperty.HasTax==False:
                successors.append([self.GetBuyState("max"),"buy"])
                
            elif currentproperty.Owner==self.Agent2.Id:
                successors.append([self.GetSellState("max"),"sell"])
            
            
        elif StateType=="human":
            currentproperty=Properties[self.Agent1.Position]
            if currentproperty.Owner==self.Agent2.Id:
                successors.append([self.GetRentState("human"),"rent"])
                return successors
            
            if self.Agent1.cash >= currentproperty.Price  and currentproperty.Owner==None and currentproperty.HasTax==False:
                successors.append([self.GetBuyState("human"),"buy"])
             
            if currentproperty.Owner==self.Agent1.Id:
                successors.append([self.GetSellState("human"),"sell"])

        successors.append([self.GetDoNothingState(),"DoNothing"])
        return successors
    
            
            
            
            
            
    
        
        
class Game:
    def __init__(self,agents:list[Agent],currentState:State):
        self.Agents=agents
        self.CurrentState:State=currentState
        self.value:list=[]

    
    def EvalFunc(self,state:State):
        sumValProps=0
        for property in state.Agent2.Properties:
            sumValProps +=property.Price
        value=state.Agent2.cash + sumValProps
        return value
    
    
    
    
    # def GetNextStateType(self,currentplayer):
    #     return StateTypes[(currentplayer+1)%len(players)]            
    
    
    def ExpectiMiniMax(self,state:State,Depth,currentplayer:str):
        state.printState()
        
        if Depth==0:
            return None,self.EvalFunc(state)   
        if currentplayer=="max":
            max_value = float('-inf')
            successors=state.get_successors("max")
            bestmove=successors[0]
            for successor in successors:
                
                bestmove,value = self.ExpectiMiniMax(successor[0], Depth - 1,"chancemin")
                self.value.append((value,successor))
                print(successor[1])
                if value > max_value:
                    bestmove=successor
                    max_value=value 
            return bestmove,max_value
        elif currentplayer=="chancemax":
            ExpectedValue = 0
            for successor in state.get_successors("chancemax"):
                bestmove,value =self.ExpectiMiniMax(successor[0], Depth - 1,"max")
                ExpectedValue =ExpectedValue + value* (1/6)                
            return None,ExpectedValue
        
        elif currentplayer=="chancemin":
            ExpectedValue = 0
            for successor in state.get_successors("chancemin"):
                bestmove,value =self.ExpectiMiniMax(successor[0], Depth - 1,"min")
                ExpectedValue =ExpectedValue + value* (1/6)
            return None,ExpectedValue
        else:
            min_value = float('inf')
            successors=state.get_successors("min")
            bestmove=successors[0]
            for successor in successors :
                bestmove,value = self.ExpectiMiniMax(successor[0], Depth - 1,"chancemax")
                if value < min_value:
                    bestmove=successor
                    min_value=value 
            return bestmove,min_value
             
       
    def MakeRobotDecision(self):
        bestaction,bestvalue=self.ExpectiMiniMax(self.CurrentState,2,"max")
        bestaction=0
        bestchoice=""
        for action in self.value:
            if action[0] > bestaction:
                bestaction=action[0]
                self.CurrentState=action[1][0]
                bestchoice=action[1][1]
        print("Current position : ",Properties[self.CurrentState.Agent2.Position].Name)
        #print("robot1 choosed action:",bestaction[1])
        print("robot1 choosed action:",bestchoice)
        input("press any key to continue...")
       # self.CurrentState=bestaction[0]
        
        
    def MakeHumanDecision(self):
        print("Current Position : ",Properties[self.CurrentState.Agent1.Position].Name)
        print("price : ",Properties[self.CurrentState.Agent1.Position].Price)
        if self.CurrentState.Properties[self.CurrentState.Agent1.Position].Owner != None:
            print("Owner : ",self.CurrentState.Properties[self.CurrentState.Agent1.Position].Owner)
        else:
            print("\n!has no owner\n") 
        print("possible Actions: ")
        possibleactions=self.CurrentState.get_successors("human")
        for i in range(len(possibleactions)):
            print(i,")",possibleactions[i][1])
        selectedaction=int(input("Enter Your Action:"))
        if selectedaction < len(possibleactions) and selectedaction>=0 :
                print("\nyou choosed action: ",possibleactions[selectedaction][1])
                input("\npress any key to continue...\n")
                self.CurrentState=copy.deepcopy(possibleactions[selectedaction][0])
                print("your cash(after apply action): ",self.CurrentState.Agent1.cash)
                input("\npress any key to continue...")

                
                
    
    
    def RollDice(self):
           return randint(1, 6)
    

    def Play(self):
        i=0    #current playerId
        while(True):
            roll=self.RollDice()
            print(self.Agents[i].Name , "rolled " ,roll,"\n")
            input("press any key to continue...")
            self.Agents[i].Position =(self.Agents[i].Position + roll) % len(Properties)
            if self.Agents[i].Type=="human":
                self.CurrentState.Agent1.Position= (self.CurrentState.Agent1.Position + roll)% len(self.CurrentState.Properties)
                self.MakeHumanDecision()
            elif self.Agents[i].Type=="robot":
                self.CurrentState.Agent2.Position= (self.CurrentState.Agent2.Position + roll)% len(self.CurrentState.Properties)
                self.CurrentState.printState()
                self.MakeRobotDecision()
            if self.CurrentState.IsTerminal():
                print("Game Over")
                if self.CurrentState.Agent1.cash>0 :
                    print(self.CurrentState.Agent1.Name ," won!!!!!")
                else:
                    print(self.CurrentState.Agent2.Name," won!!!!!!")
            i=(i+1) % len(self.Agents)
            
            
            
    


#############################################

def ConfigGame():
    #Config Agents :
    player1Name=input("Enter Player name:")
    agent1=Agent("human",0,player1Name,0,1000)
    agent2=Agent("robot",1,"robot1",0,1000)
    firststate=State(agent1,agent2,Properties)
    #Define Game: 
    game=Game([agent1,agent2],firststate)
    return game
    
def Main():
    game=ConfigGame()
    game.Play()


def Main2():
    agent1=Agent("human",0,"amir",2,800,[Property(2,"tabriz",0,False,200,100)])
    Properties[2].Owner=0
    agent2=Agent("robot",1,"robot1",4,1000,[])
    currstate=State(agent1,agent2,copy.deepcopy(Properties))
    game=Game([agent1,agent2],currstate)
    action,val=game.ExpectiMiniMax(currstate,1,"max")
    print("vlauues:  \n" ,game.value)
    return
#Main()
Main()
        
            
        
    