import cadquery as cq
# from ocp_vscode import show_object, reset_show, set_defaults
# reset_show()

import Parts

ESP32     = Parts.ESP32()
LCD       = Parts.LCD()
HCSR04    = Parts.HC_SR04()
Mic       = Parts.Mic()
ServoSG90 = Parts.Servo_SG90()

# r = Mic().CAD(alpha=60)
# r = Servo_SG90().CAD(HReise=0, alpha=0)
###################################################

lcd=[80,36,18]
hand=[45,40,35,110]
# top =[35,42,166]
top =[35,68,166]
top_shift = 40.0 # the amount of forward movement from center of the top part


thick = 2.3
corner = 8
Din,Dout = 3, 8
Dbore, depthBore = 6, 4
sInset = 2.5+Dout/2
chanH = 1.5

splitPlane = -0.368*top[1]

tol = 1.0
#==================================================
Xo_Box, Yo_Box = 95., 6.75
LWu, LWb = 26, 17
hw = 1.5
#==================================================
x_esp, y_esp, z_esp       =   0.0, -5.0,  45.0
x_LCD, y_LCD, z_LCD       =   10.0,  0.0, 138.0
x_Servo, y_Servo, z_Servo =  89.0,-15.0, 125.0
x_echo, y_echo, z_echo    =  72.0,  0.0, 117.5
x_mic, y_mic, z_mic       = 47.0,  0.0, 117.0
Switch_D = 6.0
#==================================================
xh,yh = hand[0]/2,hand[3]
xt,yt = top[2]/2-top_shift, yh+top[0]
# xt,yt = top[2]/2+top_shift, yh+top[0]

screwHand = [(-xh+1.2*sInset,1.2*sInset),(xh-1.2*sInset,1.2*sInset),
             (-xh+sInset,0.98*yh-sInset),(xh-sInset,0.95*yh-sInset)]
screwTop = [(-xt+sInset,yh+sInset),(-xt+sInset,yt-sInset),
            (xt+2*top_shift-sInset,yh+sInset+8),(xt+2*top_shift-sInset,yt-sInset),
            (xt-20,0.87*yt)]
# screwTop = [(-xt+sInset,yh+sInset+6),(-xt+sInset,yt-sInset),
#             (xt-2*top_shift-sInset,yh+sInset),(xt-2*top_shift-sInset,yt-sInset)]
###################################################
cover = (
    # Handle
    cq.Workplane('XY')
    .rect(hand[0],hand[2]).extrude(hand[3]).tag('base')
    .faces('>Z').workplane(origin=(top_shift,0,top[0]/2))
    .rect(top[2],top[1]).extrude(top[0]).tag('top')
    #-------------------
    .faces('<Z',tag='base').workplane(offset=-thick,centerOption='CenterOfMass')
    .rect(hand[0]-2*thick, hand[2]-2*thick).extrude(-hand[3], combine='s')
    .faces('>Z',tag='base').workplane(origin=(top_shift,0,0),offset=thick)
    .rect(top[2]-2*thick,top[1]-2*thick).extrude(top[0]-2*thick, combine='s')
    #-------------------
    .edges().fillet(corner)
    #-------------------
    # the hole for throwing spheres
    .faces('>Z',tag='top').workplane(origin=(Xo_Box,Yo_Box,0)).rect(LWu+2*hw,LWu+2*hw)
    .workplane(offset=-top[0],origin=(Xo_Box,Yo_Box-(LWu-LWb)/2,0))
    .rect(LWb+2*hw,LWb+2*hw).loft()
    .faces('>Z',tag='top').workplane(origin=(Xo_Box,Yo_Box,0)).circle(LWu/2)
    .workplane(offset=-top[0],origin=(Xo_Box,Yo_Box-(LWu-LWb)/2,0))
    .circle(LWb/2).loft(combine='s')
    .edges().chamfer(2)
    #-------------------
    # screws handle
    .faces('>Y').workplane(origin=(0,0,0),offset=(hand[2]-top[1])/2-thick)
    .pushPoints(screwHand)
    .circle(Dout/2).circle(Din/2)
    .extrude(-hand[2]+2*thick)
    .workplane(origin=(0,0,0),offset=(hand[2]-top[1])/2+1.4*thick)
    .pushPoints(screwHand)
    .cboreHole(Din, Dbore, depthBore+2, 2*thick)
    #--------
    # screws top
    .faces('<Y').workplane(origin=(0,0,0),offset=-1.4*thick)
    .pushPoints(screwTop)
    .circle(Dout/2).circle(Din/2)
    .extrude(-top[1]+2.8*thick)
    .workplane(origin=(0,0,0),offset=top[1]/2+thick)
    .pushPoints(screwTop)
    .cboreHole(Din, Dbore, depthBore+17, 2*thick)
    # -------------------
    # the LCD hole
    .faces('>Z',tag='top')
    .workplane(origin=(x_LCD, y_LCD))
    .rect(LCD.lcd_L+tol, LCD.lcd_W+tol).extrude(-2*thick, combine='s')
    # -------------------
    # the LCD hold
    .faces('>Y',tag='top')
    .workplane(centerOption='CenterOfMass',offset=-thick+tol)
    .moveTo(top_shift-x_LCD, top[0]/2-2*thick-5-tol)
    .rect(LCD.pcb_L,2*thick)
    .workplane(centerOption='CenterOfMass',offset=-thick+tol-0.72*LCD.pcb_W)
    .moveTo(0,0.75*thick)
    .rect(LCD.pcb_L,thick).loft()
    #-------------------
    # the Servo hole
    .faces('>Z',tag='top')
    .workplane(origin=(x_Servo+ServoSG90.body_H/2-ServoSG90.Top_LargeCyl_Dia/2,y_Servo),offset=-top[0])
    .circle(ServoSG90.Top_LargeCyl_Dia/2)
    .extrude(2*thick, combine='s')
    .moveTo(ServoSG90.Top_LargeCyl_Dia/2,0+tol/2)
    .circle(ServoSG90.Top_SmallCyl_Dia/2+tol/2)
    .extrude(2*thick, combine='s')
    .faces('>Z',tag='top')
    .workplane(origin=(x_Servo+ServoSG90.body_H/2-ServoSG90.Top_LargeCyl_Dia/2, y_Servo-ServoSG90.Top_LargeCyl_Dia/2-thick/2-tol),offset=-top[0])
    .rect(ServoSG90.body_H+2*thick,thick).extrude('next')
    #-------------------
    # the Echo hole
    .faces('>Z',tag='top')
    .workplane(origin=(x_echo, y_echo),offset=-top[0])
    .pushPoints([(0, -(HCSR04.RT_Distance-HCSR04.RT_Diameter)/2),
                  (0,  (HCSR04.RT_Distance-HCSR04.RT_Diameter)/2)])
    .circle(HCSR04.RT_Diameter/2+tol/2).extrude(2*thick, combine='s')
    #-------------------
    # the Mic holes
    .faces('>Z',tag='top')
    .workplane(origin=(x_mic, y_mic),offset=-top[0])
    .moveTo((Mic.pcb_W-Mic.potent_W )/2-0.5, -1.7)
    .rect(Mic.potent_W+tol, Mic.potent_L+tol).extrude(2*thick, combine='s')
    .moveTo(0, (Mic.pcb_L-Mic.mic_Dia)/2)
    .circle(Mic.mic_Dia/2+tol/2).extrude(2*thick, combine='s')
    #-------------------
    # the USB holes
    .faces('<Z',tag='top').workplane(origin=(0,-7.4))
    .hole(7, 2*thick)
    # -------------------
    # the switch 1 hole
    .faces('>X',tag='base').workplane(origin=(0,0,0.8*hand[3]))
    .sketch().rect(15,20).vertices().fillet(6)
    .finalize().extrude(5)
    .faces('>X',tag='base').workplane(origin=(0,0,0.8*hand[3]),offset=Switch_D)
    .circle(Switch_D).extrude(-2*thick-Switch_D, combine='s')
    #-------------------
    # the switch 2 hole
    .faces('>Y',tag='top').workplane(centerOption='CenterOfMass').moveTo(40,0)
    .circle(Switch_D).extrude(-2*thick, combine='s')
    #==========================
    # text
    .faces('>Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(-50,3).text("FSHN",7,-1,font="DejaVuSans",kind="regular")
    .faces('>Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(-50,-3).text("Fizike",5,-1,font="DejaVuSans",kind="regular")
    .faces('>Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(0,0).text("Grav-g",10,-1,font="DejaVuSans",kind="bold")
    .faces('<Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(50,3).text("FSHN",7,-1,font="DejaVuSans",kind="regular")
    .faces('<Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(50,-3).text("Fizike",5,-1,font="DejaVuSans",kind="regular")
    .faces('<Y',tag='top').workplane(centerOption='CenterOfMass')
    .center(5,0).text("Grav-g",10,-1,font="DejaVuSans",kind="bold")
    #---------------------
    )

(tcover, bcover) = (
    cover.faces("<Y")#.workplane(-0.3165*top[1])
    .workplane(splitPlane)
    .split(keepTop=True, keepBottom=True)
    .all()
    )
tcover = tcover.translate((0,-50,0))

show_object(bcover, options=dict(alpha=0.5))


r = (
      cq.Assembly()
         # .add(tcover,name='Cover_Up',color=cq.Color("ghostwhite"))
         # .add(bcover,name='Cover_Bot',color=cq.Color("ghostwhite"))
       .add(
           ESP32.CAD().rotate((0,0,-1),(0,0,0),90), 
           name='ESP32',
           loc=cq.Location((x_esp,y_esp,z_esp),(1, 0, 0),90),
           color=cq.Color("gray60")
           )
      .add(
          LCD.CAD(),name='LCD',
          loc=cq.Location((x_LCD, y_LCD, z_LCD),(0,0,1),180),
          color=cq.Color("blue")
          )
        .add(
            HCSR04.CAD().rotate((0,0,-1),(0,0,0),-90),name='HC-SR04',
            loc=cq.Location((x_echo, y_echo, z_echo),(1, 0, 0),180),
            color=cq.Color("green")
            )
        .add(
            Mic.CAD(0).rotate((0,0,-1),(0,0,0),90), 
            name='Mic',
            loc=cq.Location((x_mic, y_mic, z_mic),(0, 1, 0),180),
            color=cq.Color("red")
            )
        .add(
            ServoSG90.CAD(HReise=0,alpha=90,XY=False),
            name='Servo',
            loc=cq.Location((x_Servo+ServoSG90.body_L/2,y_Servo,z_Servo),(0, 1, 0),180)
            )
      )

show_object(tcover, options=dict(alpha=0.3))
show_object(bcover, options=dict(alpha=0.3))
show_object(r, options=dict(alpha=0.))

path = '/home/drago/PROJECTS/LEARNING/CADquery/Brixh/Output/'
cq.exporters.export(tcover, path+"Cover_Up.stl")
cq.exporters.export(bcover, path+"Cover_Bot.stl")
# r.save(path + 'model.step')
# # obj = bcover.union(tcover)
# # tcover.save(path+ 'top.stl', cq.exporters.ExportTypes.STL)
# # bcover.exportStl(path+ 'bottom.stl')

###################################################
# def Handle():
#     r = (
#           cq.Workplane('XY').sketch()
#           .rect(hand[0],hand[2])
#           .rect(hand[0]-2*thick, hand[2]-2*thick, mode='s')
#           .vertices().fillet(corner)
#           .finalize().extrude(hand[3])
#           ################
#           .faces('<Z').workplane().sketch()
#           .rect(hand[0],hand[2]).vertices().fillet(corner)
#           .finalize().extrude(-thick)
#           ################
#           .faces('<Y').workplane(-1).moveTo(0,hand[3]/2)
#           .rect(hand[0]-sInset, hand[3]-sInset, forConstruction=True)
#           .vertices().circle(Dout/2).circle(Din/2).extrude(-hand[2]+2, True)
#           )
#     remove = (
#         cq.Workplane('XY').sketch()
#           .rect(1.2*hand[0],1.2*hand[2])
#           .rect(hand[0],hand[2], mode='s')
#           .vertices().fillet(corner)
#           .finalize().extrude(hand[3])
#         )
#     r = r.cut(remove)
#     (top, bot) = (
#         r.faces(">Y")
#         .workplane(-corner).moveTo(0,hand[3]/2)
#         .rect( 2*hand[1], hand[3])
#         .split(keepTop=True, keepBottom=True)
#         .all()
#     )
#     bot = bot.cut(top)
#     top = top.translate((0,30,0))
#     top = (
#           top.faces('<Y').workplane().moveTo(-hand[0]/2,thick/2)
#          .hLine(hand[0]-thick/2).vLine(hand[3]-thick/2)
#          .hLine(-thick/2).vLine(-hand[3]+thick)
#          .hLine(-hand[0]+2*thick).vLine(hand[3]-thick)
#          .hLine(-thick/2).vLine(-hand[3]+thick/2).close()
#          .extrude(-chanH, combine='s')
#          .faces('>Y').workplane().moveTo(0,hand[3]/2)
#          .rect(hand[0]-sInset, hand[3]-sInset, forConstruction=True)
#          .vertices().cboreHole(Din, Dbore, depthBore, 2*thick)
#           )
#     bot = (
#           bot.faces('>Y').workplane().moveTo(-hand[0]/2,thick/2)
#          .hLine(hand[0]-thick/2).vLine(hand[3]-thick/2)
#          .hLine(-thick/2).vLine(-hand[3]+thick)
#          .hLine(-hand[0]+2*thick).vLine(hand[3]-thick)
#          .hLine(-thick/2).vLine(-hand[3]+thick/2).close()
#          .extrude(chanH, combine='a')
#           )
#     r = top.union(bot)
#     return r
#######################################################
#######################################################
#######################################################

# r = Handle()

# show_object(r, options=dict(alpha=1.))

#######################################################

















