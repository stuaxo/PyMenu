# -*- coding: utf-8 -*-
import pygame, sys, Common, MainMenu, Configuration, RenderControl, TaskHandler,subprocess
import platform, Suspend, BrightnessVolumeControl
import time, os

from pygame.locals import *

textFont = pygame.font.Font('theme/NotoSans-Regular.ttf', 10)


pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(50, 50)
config = Configuration.getConfiguration()


#set screen mode
if(Configuration.isRS97()):
    try:
        os.system('echo 2 > /proc/jz/lcd_a320')
    except Exception as ex:
        pass



def setVolume():
    if(Configuration.isRS97()):
        try:
            pass
            ##not working
            # from fcntl import ioctl
       
            # filename = "/dev/mixer"
            # SOUND_MIXER_WRITE_VOLUME = 0xc0044d00
            # oss_volume = 100 | (100 << 8)
          
            # fd = open(filename, "wb")            
            # ioctl(fd, SOUND_MIXER_WRITE_VOLUME, oss_volume)
            # fd.close()
        except Exception as ex:
            print("could not set volume: " + str(ex))

def init():
    lastRenderTime = 1
    setVolume()
    if(Configuration.isRS97() and platform.processor() == ""):
        realScreen = pygame.display.set_mode((320,240), HWSURFACE, 16)
        screen = pygame.Surface((config["screenWidth"],config["screenHeight"]))
    else:
        realScreen = pygame.display.set_mode((config["screenWidth"],config["screenHeight"]), HWSURFACE, 16)
        screen = realScreen
    

    renderObject = MainMenu.MainMenu(screen)

    suspend = Suspend.Suspend()
    brightness = BrightnessVolumeControl.BrightnessVolume()

    
    while True: # main game loop
        events = pygame.event.get()       
        for event in events:
            if event.type == QUIT:
                pygame.quit()            
                sys.exit()

        suspend.handleEvents(events)
        renderObject.handleEvents(events)
        brightness.handleEvents(events)
        
        if(RenderControl.isDirty()):   
            start = int(round(time.time() * 1000))            
            RenderControl.setDirty(False)
            renderObject.render(screen)
            brightness.render(screen)

            if("showFPS" in config["options"] and config["options"]["showFPS"]):
                if(lastRenderTime == 0):
                    lastRenderTime = 1
                textSurface = textFont.render(str(int(round(1000/lastRenderTime))) + "fps ~" + str(lastRenderTime) + "ms", True, (255,255,255))
                screen.blit(textSurface, (0,0))
                print("render time: " + str(lastRenderTime))


            
            realScreen.blit(screen, (0,0))
            
            

            pygame.display.update()
            lastRenderTime = int(round(time.time() * 1000))  - start
            

        TaskHandler.updateTasks()
        fpsClock.tick(Common.FPS)

init()
