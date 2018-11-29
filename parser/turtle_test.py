import turtle
wn = turtle.Screen()  # creates a graphics window
wn.screensize(800, 600)
alex = turtle.Turtle()  # create a turtle named alex
alex.pensize(6)
alex.dot("blue")
alex.penup()
alex.goto(50, 50)
alex.dot("green")
turtle.done()