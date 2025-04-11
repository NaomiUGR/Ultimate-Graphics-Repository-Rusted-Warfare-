#!/usr/bin/python


#'apt-get install python-imaging' if you are missing image

import Image
from PIL import ImageFont
from PIL import ImageDraw 

import os
import subprocess
import sys
import re
import time


mapImage  = Image.open(sys.argv[1])
unitImage = Image.open(sys.argv[2])


teamFont = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 18)
teamFontBackground = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 19)


teamFontSmall = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf', 16)



playerCountMatch=re.search(r'\[(.*;)?p([0-9]*)\].*', sys.argv[1])

if playerCountMatch:

  playerCount=int(playerCountMatch.groups()[1])

else:
  print "File must start with [1-9p] to get spawn points"
  sys.exit(0)






print "playerCount:"+str(playerCount)


class Team:
   def __init__(self, id, color, mapOverride=None):
    self.id=id
    self.color=color
    self.mapOverride=mapOverride
    if not self.mapOverride:
      self.mapOverride=self.color
    self.x=0
    self.y=0
    self.diff=500
    self.avgX=0
    self.avgY=0
    self.avgTotal=1

teams=[]

teams.append( Team(1,(0,255,0)) )
teams.append( Team(2,(255,0,0)) )
teams.append( Team(3,(0,0,255),  (50,100,150) ) )
teams.append( Team(4,(255,255,0), (200,200,0)) )
teams.append( Team(5,(0,255,255), (230,170,100)) )
teams.append( Team(6,(255,255,255), (93, 218, 218)) )
teams.append( Team(7,(0,0,0), (184, 106, 205)) )
teams.append( Team(8,(255,0,255), (106, 108, 205) ) )

teams.append( Team(9,(255, 127, 24), (205, 132, 30) ) )
teams.append( Team(10,(147, 104, 196), (120, 0, 176) ) )



def colorDiff(a,b):
  return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

unitImageWidth=unitImage.size[0]
unitImageHeight=unitImage.size[1]



for team in teams:
  if team.id<=playerCount:
    for x in xrange(0,unitImageWidth):
      for y in xrange(0,unitImageHeight):
        #print x
        pixel=unitImage.getpixel((x, y))
        
        if (pixel[3]!=0):
          diff=colorDiff(pixel, team.mapOverride)
          if team.diff>diff:
            #team.x=x
            #team.y=y
            team.avgX=x
            team.avgY=y
            team.avgTotal=1
            team.diff=diff
          elif team.diff==diff:
            team.avgX+=x
            team.avgY+=y
            team.avgTotal+=1
    
    team.x=team.avgX/team.avgTotal
    team.y=team.avgY/team.avgTotal
    
    imageLayer=Image.new("RGBA", mapImage.size)
    draw = ImageDraw.Draw(imageLayer)
    
    textX=(team.x / float(unitImageWidth) )*float(mapImage.size[0])
    textY=(team.y / float(unitImageHeight) )*float(mapImage.size[1])
    textString=str(team.id)
    
    offsetX=0
    offsetY=0
    #offsetX=-2
    #offsetY=-2
    
    font=teamFont
    
    #if len(textString)>=2:
      #font=teamFontSmall
      #offsetX=-3
      #offsetY+=1
    
    w, h = draw.textsize(textString, font=font )
    
    
    textPos=(textX-(w/2)+offsetX,textY-(h/2)-3+offsetY) #was y -5
    
    #draw.text(textPos , textString, fill=(0,0,0), font=teamFontBackground )
    #eSize=13
    
    eSize=11
    
    draw.ellipse( (textX-eSize, textY-eSize, textX+eSize, textY+eSize), fill=(0,0,0,100) )
    
    
    draw.text(textPos , textString, fill=team.color, font=font )
    
    
    mapImage.paste(imageLayer, (0, 0), imageLayer)


mapImage = mapImage.convert("RGB")

mapImage.save(sys.argv[1])


