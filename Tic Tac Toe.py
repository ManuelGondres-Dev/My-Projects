#First scripted game in Python 

import pygame 
from sys import exit
import random
import json

pygame.init()

Width,Height = 900,900

Fps = 60

Running = True
Game_Active = False
Game_Mode = "PVP"
Can_Click = True
Wins = 0

Bot_Wait_Time = random.randint(2,5)

Display = pygame.display.set_mode((Width,Height))

pygame.display.set_caption("Tic Tac Toe")

Clock = pygame.time.Clock()

print("Running!")

Game = [
        "","","",
        "","","",
        "","",""
        ]

Tiles = []

Tile_Size = Height//5

X_Spacing = -Tile_Size 
Y_Spacing = -Tile_Size

Symbols = ["o","x"]

Title_Font = pygame.font.Font("Pixeltype.ttf",size = 80)
Status_Font = pygame.font.Font("Pixeltype.ttf",size = 60)
Base_Font = pygame.font.Font("Pixeltype.ttf",size = 45)

Background_Music = pygame.mixer.Sound("yakastreams-retro-gaming-271301.mp3")
Background_Music.play(-1)
Background_Music.set_volume(0.2)

Button_Pressed_SFX = pygame.mixer.Sound("Button Press Sound Effect.mp3")
Button_Pressed_SFX.set_volume(0.2)

Button_Pressed_SFX2 = pygame.mixer.Sound("Button Press Sound Effect 2.mp3")

Win_SFX = pygame.mixer.Sound("Winner sound effect.mp3")
Win_SFX.set_volume(0.2)

Lose_SFX = pygame.mixer.Sound("Lose sound effect.mp3")
Lose_SFX.set_volume(0.2)
White = (255,255,255)

class Button:
    def __init__(self,Name,Color,Rect,Rect_Width = 0,Border_Radius=0,Position = (Width//2,Height//2),Text="",Text_Color=White):
        global Can_Click,Game_Active,Game_Mode,Last_Time,Running
        self.Name = Name
        self.Rect = Rect
        self.Rect.center = Position
        pygame.draw.rect(Display,Color,Rect,Rect_Width,border_radius=Border_Radius)
        if Text:
            Text_Label = Base_Font.render(Text,False,Text_Color)
            Display.blit(Text_Label,Text_Label.get_rect(center=Rect.center))
        if self.Rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and Can_Click:
            Button_Pressed_SFX.play()
            if self.Name == "Exit":
                Running = False
            elif self.Name == "Restart":
                Can_Click = False
                Game_Active = False
                pygame.time.delay(100)
                Set_Stats()
                Can_Click = True
            else:
                Can_Click = False
                Last_Time = pygame.time.get_ticks()//1000
                Game_Active = True
                print("Clicked")
                Can_Click = True
                Game_Mode = self.Name

def Set_Stats():
    global Player,Winner,Turn,Can_Click,Game,Tiles
    Game = [
        "","","",
        "","","",
        "","",""
        ]
    Can_Click = True
    Player = random.choice(Symbols)
    Winner = ""
    Turn = random.choice(Symbols)

def Update_Status():
    if Winner:
        if Winner == "tie":
            Status = Status_Font.render(f"Tie!",False,White)
        else:
            if Player == Winner:
                Status = Status_Font.render(f"You win!",False,White)
            else:
                Status = Status_Font.render(f"You lose!",False,White)
    else:
        if Player == Turn:
            Status = Status_Font.render(f"You're turn! ({Player})",False,White)
        else:
            Status = Status_Font.render(f"Opponent turn! ({"x" if Player == "o" else "o"})",False,White)

    Display.blit(Status,Status.get_rect(center = (Width//2,100)))

def Draw_X(Item):
    pygame.draw.line(Display,White,(Item.topleft[0],Item.topleft[1]+20),(Item.bottomright[0],Item.bottomright[1] - 20),15)
    pygame.draw.line(Display,White,(Item.topright[0],Item.topright[1]+20),(Item.bottomleft[0],Item.bottomleft[1] - 20),15)

def Tile_Checker(First,Second,Third):
    Data = [Game[First],Game[Second],Game[Third]]
    First_Tile = Tiles[First]
    Third_Tile = Tiles[Third]
    if all(Item == Turn for Item in Data):
        print("Game Over!")
        return True
    return False

def Check_Winner():
    Check_Tiles = [Tile_Checker(0,1,2),Tile_Checker(3,4,5),Tile_Checker(6,7,8),Tile_Checker(0,3,6),Tile_Checker(1,4,7),Tile_Checker(2,5,8),Tile_Checker(0,4,8),Tile_Checker(2,4,6)]
    for Func in Check_Tiles:
        if Func:
            print("Success")
            return True
    return False

def Wait_Then_Exit():
    global Game_Active
    global Can_Click
    Can_Click = False
    pygame.time.delay(800)
    Set_Stats()
    Game_Active = False

def Draw(Item,Position):
    global Game,Winner,Turn
    if not Game_Active:
       return

    Game[Position] = Turn

    if Check_Winner():
        Winner = Turn
    elif all(Game):
        Winner = "tie"

    if Turn == "x":
        Turn = "o"
        print("Inserted x")
        Button_Pressed_SFX2.play()
        Draw_X(Item)
    else:
        Turn = "x"
        Button_Pressed_SFX2.play()
        pygame.draw.circle(Display,White,Item.center,70,30)

def Bot_Choose():
    global Last_Time
    Current_Time = pygame.time.get_ticks()//1000
    print(Current_Time - Last_Time)
    if Current_Time - Last_Time >= Bot_Wait_Time:
        Result = random.choice([Position for Position, Item in enumerate(Game) if not Item])
        Draw(Tiles[Result],Result)

def Load_Data():
    global Wins
    try:
        with open("Highest Wins.json","r") as File:
            Wins = json.load(File)
    except FileNotFoundError:
            Wins = 0

def Save_Data():
    with open("Highest Wins.json","w") as File:
        json.dump(Wins,File)

Set_Stats()
Load_Data()

while Running:
    Events = pygame.event.get()
    for input in Events:
            if input.type == pygame.QUIT:
                Running = False
    if Game_Active:
        Display.fill(("#44D6FA"))
        if Winner:
            print("There is a winner")
            Win_SFX.stop()
            Lose_SFX.stop()
            if Winner == Player:
                Wins += 1
                Win_SFX.play()
            else:
                Lose_SFX.play()
            Wait_Then_Exit()
        for input in Events:
            if input.type == pygame.MOUSEBUTTONDOWN and Can_Click:
                for Position,Item in enumerate(Tiles):
                    Mouse_Pos = input.pos
                    if input.button == 1 and Item.collidepoint(Mouse_Pos) and not Game[Position]:
                        if (Game_Mode == "PVB" and Player == Turn) or Game_Mode == "PVP": 
                            Draw(Item,Position)
                            print("Pressed on a button!")
        if len(Tiles) >= 9:
            list.clear(Tiles)
        for Count in range(0,9):
            Tile = pygame.Rect(0,0,Tile_Size,Tile_Size)
            Tile.center = (Width//2 + X_Spacing,Height//2 + Y_Spacing)
            list.append(Tiles,Tile)
            if (Count + 1) % 3 == 0:
                X_Spacing = -Tile_Size
                Y_Spacing += Tile_Size + 3
            else:
                X_Spacing += Tile_Size + 3
            if Count == 8:
                X_Spacing = -Tile_Size 
                Y_Spacing = -Tile_Size
        for Item_Position,Item_Tile in enumerate(Tiles):
            pygame.draw.rect(Display,(0,0,0),Item_Tile,border_radius=15)  
            Symbol = Game[Item_Position]
            if Symbol:
                if Symbol == "x":
                    Draw_X(Item_Tile)
                else:
                    pygame.draw.circle(Display,White,Item_Tile.center,70,30)
        Button("Restart",((255,0,0)),pygame.Rect(0,0,300,80),0,15,(Width//2,Height - 80),"Restart")
        if Game_Mode == "PVB":
            if Turn== Player:
                Bot_Wait_Time = random.randint(2,5)
                Last_Time = pygame.time.get_ticks()//1000
            else:
                print("Bot turn")
                Bot_Choose()

        Update_Status()
    else:
        Display.fill(("#3EB8EC"))
        Title = Title_Font.render(f"{pygame.display.get_caption()[0]}",False,(White))
        Display.blit(Title,Title.get_rect(center = (Width//2,100)))
        Description = Status_Font.render("Choose a Game Mode!",False,(White))
        Display.blit(Description,Description.get_rect(center = (Width//2,160)))
        Wins_Label = Status_Font.render("You have no wins!" if Wins == 0 else f"You have: {Wins} {"Win!" if Wins == 1 else "Wins!"}",False,(White))
        Display.blit(Wins_Label,Wins_Label.get_rect(center = (Width//2,Height - 160)))
        Button("PVB",("#5BC8E4"),pygame.Rect(0,0,280,80),0,15,(Width//2-150,Height//2),"Player Vs Bot")
        Button("PVP",("#5BC8E4"),pygame.Rect(0,0,280,80),0,15,(Width//2+150,Height//2),"Player1 Vs Player2")
        Button("Exit",((255,0,0)),pygame.Rect(0,0,300,80),0,15,(Width//2,Height - 80),"Exit The Game")
    pygame.display.update()
    Clock.tick(Fps)

Save_Data()
pygame.quit()
exit()