import pygame as pg
import main
import pygame.freetype as freetype
import json
import random

black = (0, 0, 0)
white = (255, 255, 255)
brown = (210, 105, 30)

class Quizbehaviour(object):
    def __init__(self):
        self.screen_size = main.SCREEN_SIZE
        self.clock = pg.time.Clock()
        self.quiz = True
        self.quizrectsize = (self.screen_size[0] / 2, self.screen_size[1] / 4)
        self.quizrectcenterpos = (self.screen_size[0] / 2, self.screen_size[1] / 6)
        self.answerrectsize = (self.screen_size[0] / 2, self.screen_size[1] / 10)
        self.answerrectcenterpos = (self.screen_size[0] / 5, self.screen_size[1] / 2)
        self.font = pg.font.Font('fonts/freesansbold.ttf', 20)

    def quiz_popup(self, color):
        questionnumber = 0 #placeholder, has to be a random question from the json

        with open("Questions.json") as f:
            questiondata = json.load(f)

        text = questiondata[color][questionnumber]['question']

        #put answers in a list and shuffle the list, so that it's ready for blitting
        correctanswer = questiondata[color][questionnumber]['correctanswer']
        answer2 = questiondata[color][questionnumber]['answer2']
        answer3 = questiondata[color][questionnumber]['answer3']
        answerlist = [correctanswer,answer2,answer3]
        random.shuffle(answerlist)

        while self.quiz:
            for event in pg.event.get():
               if event.type == pg.QUIT:
                   pg.quit()
                   quit()



            ##draw question rectangle
            rect = pg.Rect(self.screen_size[0] / 10, self.screen_size[1] / 10, self.quizrectsize[0], self.quizrectsize[1])
            rect.center = self.quizrectcenterpos
            pg.draw.rect(main.SCREEN, brown, rect)

            #draw text on the question rect
            self.blit_text(main.SCREEN, text, (self.quizrectcenterpos[0] / 2, self.quizrectcenterpos[1] - self.quizrectsize[1] / 2), self.font)


            #draw answer buttons
            padding = 0
            for answer in answerlist:

                self.button(answer,(self.screen_size[0] / 2), (self.screen_size[1] / 2.3 + padding),self.answerrectsize[0],self.answerrectsize[1], white, brown)
                padding += 200



            pg.display.update()
            self.clock.tick(60)


    def blit_text(self,surface, text, pos, font, color=pg.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = (self.screen_size[0] - (self.screen_size[0] - (self.quizrectcenterpos[0] + self.quizrectsize[0] / 2)), 600)
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.


    def button(self, msg, x, y, width, height, inactivecolor, activecolor, action=None):
        smalltext = pg.font.Font('fonts/freesansbold.ttf', 50)
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        rect = pg.Rect(x, y, width, height)
        rect.center = (x, y)
        if x + (width / 2) > mouse[0] > x - (width / 2) and y + (height / 2) > mouse[1] > y - (height / 2):
            pg.draw.rect(main.SCREEN, activecolor, rect)
            if click[0] == 1:
                action()
        else:
            pg.draw.rect(main.SCREEN, inactivecolor, rect)

        #self.text_objects(msg, smalltext, x, y)
        self.blit_text(main.SCREEN,msg,(x,y),self.font)