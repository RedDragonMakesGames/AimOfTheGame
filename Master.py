import SetUpScreen
import AimOfTheGame

#Run the set up screen
setUpScreen = SetUpScreen.SetUp()
boardsetup = setUpScreen.Run()
game = AimOfTheGame.AimOfTheGame(boardsetup)
#Restart the board if the restart button was pressed
while game.Run() == True:
    board = game = AimOfTheGame.AimOfTheGame(boardsetup)