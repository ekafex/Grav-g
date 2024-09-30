import cadquery as cq

class ESP32:
    def __init__(self):
        self.pcb_L, self.pcb_W, self.pcb_H = 54.7, 28.0, 1.6            # ESP32 PCB dims.
        self.antenna_L, self.antenna_W, self.antenna_H = 6.5, 18.0, 1.0 # ESP32 Antenna circuit dims.
        self.USB_L, self.USB_W, self.USB_H = 5.7, 8.14, 3.0             # ESP32 micro USB port dims.
        self.CPU_L, self.CPU_W, self.CPU_H = 17.8, 15.9, 3.2            # ESP32 CPU chip dims.
        self.chip_L, self.chip_W, self.chip_H = 5.0, 5.0, 1.0           # ESP32 UART chip dims.
        self.pin_L, self.pin_W, self.pin_H, self.pins = 48.2, 2.6, 2.7, 6.0 # ESP32 pins dims.
        self.Diameter_Screw_Hole = 3.0                                  # ESP32 Screws hole dia.
        #-------------------------
        self.pnts = []
        for i in range(19):
            self.pnts.append((self.pin_L/2-i*2.5-2, (self.pcb_W-self.pin_W)/2-1))
            self.pnts.append((self.pin_L/2-i*2.5-2,-(self.pcb_W-self.pin_W)/2+1))
    #############################
    def CAD(self):
        r = (
            cq.Workplane('XY').box(self.pcb_L, self.pcb_W, self.pcb_H)
            .faces('>Z').workplane().tag('pcb')
            .rect(self.pcb_L-self.Diameter_Screw_Hole,self.pcb_W-self.Diameter_Screw_Hole, forConstruction=True)
            .vertices().hole(self.Diameter_Screw_Hole/2)
            .faces('<Z').workplane().tag('pcbb')
            .pushPoints([(0,(self.pcb_W-self.pin_W)/2-1),(0,-(self.pcb_W-self.pin_W)/2+1)])
            .rect(self.pin_L,self.pin_W).extrude(self.pin_H, combine=True)
            .faces('<Z').workplane(offset=0)
            .pushPoints(self.pnts).rect(0.5,0.5).extrude(self.pins)
            .workplaneFromTagged("pcb").center((self.pcb_L-self.antenna_L)/2-0.3,0).rect(self.antenna_L,self.antenna_W).extrude(self.antenna_H)
            .workplaneFromTagged("pcb").center((self.pcb_L-2*self.antenna_L-self.CPU_L)/2-0.3,0).rect(self.CPU_L,self.CPU_W).extrude(self.CPU_H)
            .workplaneFromTagged("pcb").center(-self.pcb_L/2+self.USB_L/2-1,0).rect(self.USB_L,self.USB_W).extrude(self.USB_H)
            .workplaneFromTagged("pcb").center(-self.pcb_L/2+self.USB_L+self.chip_L,-2.5).rect(self.chip_L,self.chip_W).extrude(self.chip_H)
            # .workplaneFromTagged("pcbb").center(0,(Wpcb-Wp)/2-1).hole(1)
            )
        return r

###################################################################################

class LCD:
    def __init__(self):
        # self.pcb_L, self.pcb_W, self.pcb_H    = 81.0, 36.0, 1.7 # LCD PCB dims.
        self.pcb_L, self.pcb_W, self.pcb_H    = 80.0, 41.0, 1.7 # LCD PCB dims.
        self.lcd_L, self.lcd_W, self.lcd_H    = 71.3, 24.0, 7.3 # LCD screen dims.
        self.circ_L, self.circ_W, self.circ_H = 42.0 ,16.0, 4.0 # LCD bottom circuit dims.
        self.Diameter_Screw_Hole = 4.0                          # LCD Screw whole hole dia.
        self.pin_Dia, self.pins               = 0.5, 7.0        # LCD bottom circuit pins diameter and length
    ################################
    def CAD(self):
        dl = (self.pcb_L-self.lcd_L)/2 -0.5
        x = -0.5*self.lcd_L
        pnts=[(x,-8),(x,8),(x-dl,5),(x-dl,-5)]
        pinsPnts = [(3.75,0),(1.25,0),(-1.25,0),(-3.75,0)]
        ################################
        r = (
            cq.Workplane('XY')
            .rect(self.pcb_L,self.pcb_W).extrude(self.pcb_H).tag('base')
            .faces('>Z')
            .rect(self.pcb_L-self.Diameter_Screw_Hole,self.pcb_W-self.Diameter_Screw_Hole, forConstruction=True)
            .vertices().hole(self.Diameter_Screw_Hole/2)
            .rect(self.lcd_L, self.lcd_W).extrude(self.lcd_H).tag('lcd')
            .faces('>Z', tag='base').polyline(pnts).close().extrude(4.7)
            .faces('<Z', tag='base')
            .moveTo((self.pcb_L-self.circ_L)/2-self.Diameter_Screw_Hole, (self.pcb_W-self.circ_W)/2-self.Diameter_Screw_Hole)
            .rect(self.circ_L, self.circ_W).extrude(-self.circ_H)
            .faces('>X').workplane(offset=-dl).center((self.pcb_W-self.circ_W)/2-self.Diameter_Screw_Hole,-self.lcd_H/2).pushPoints(pinsPnts).rect(self.pin_Dia, self.pin_Dia).extrude(self.pins)
            )
        return r

###################################################################################

class HC_SR04():
    def __init__(self):
        self.pcb_L, self.pcb_W, self.pcb_H       = 45, 20, 1.7  # HC-SR04 PCB dims.
        self.oscil_L, self.oscil_W, self.oscil_H = 10, 3.5, 3.4 # HC-SR04 Oscillator dims.
        self.RT_Diameter, self.RT_H              = 16.0, 12.0   # HC-SR04 Reciver/Transmiter echos cylindric diameter and height.
        self.RT_Distance                         = 42.0         # HC-SR04 Reciver/Transmiter echos outer distance
        self.Diameter_Screw_Hole                 = 1.5          # HC-SR04 PCB screws holes
        self.pin_L, self.pin_W, self.pin_H       = 10.25, 3.6, 4.0 # HC-SR04 PCB pins dims.
        self.pin_Dia, self.pins                  = 0.5, 7.0     # HC-SR04 PCB pins diameter and length
    ################################
    def CAD(self):
        r = (
            cq.Workplane('XY').box(self.pcb_L, self.pcb_W, self.pcb_H) # circuit PCB
            .edges('|Z').fillet(0.5)
            .faces('>Z').workplane().tag("circPlane")
            .rect(self.pcb_L-1.2*self.Diameter_Screw_Hole,self.pcb_W-1.2*self.Diameter_Screw_Hole, forConstruction=True)
            .vertices().hole(self.Diameter_Screw_Hole/2)
            # Oschillator
            .workplaneFromTagged("circPlane").center(0,(self.pcb_W-self.oscil_W)/2-0.2)
            .rect(self.oscil_L, self.oscil_W).extrude(self.oscil_H)
            .edges('|Z').fillet(0.9999*self.oscil_W/2)
            # Echo Transmitter & Reciever
            .workplaneFromTagged("circPlane")
            .pushPoints([(-(self.RT_Distance-self.RT_Diameter)/2,0),((self.RT_Distance-self.RT_Diameter)/2,0)])
            .circle(self.RT_Diameter/2).extrude(self.RT_H)
            # Pins
            .workplaneFromTagged("circPlane").center(0,-(self.pcb_W-self.pin_W)/2)
            .rect(self.pin_L,self.pin_W).extrude(self.pin_H)
            .faces('<Y').workplane()
            .pushPoints([(3.75,self.pin_H-0.5),(1.25,self.pin_H-0.5),(-1.25,self.pin_H-0.5),(-3.75,self.pin_H-0.5)])
            .rect(0.5,0.5).extrude(self.pins)
            )
        return r

###################################################################################

class Mic:
    def __init__(self):
        self.pcb_L, self.pcb_W, self.pcb_H          = 35.0, 15.3, 1.7# Mic PCB dims.
        self.Diameter_Screw_Hole, self.hole_H       = 3.5, 9         # Mic screw hole dims.
        self.potent_L, self.potent_W, self.potent_H = 9.5, 4.3, 9.5  # Mic potentiometer dims.
        self.potent_screw_Diam, self.potent_screw_H = 2.3, 1.65      # Mic potentiometer screw cylinder D & H
        self.mic_Dia, self.mic_H                    = 10.0, 7.0      # Mic microphone cylinder D & H
        self.pin_L, self.pin_W, self.pin_H          = 2.5, 10.0, 5.0 # Mic pins dims.
        self.pin_Dia, self.pins                     = 0.5, 7.0       # Mic pins diameter and length.
    ################################
    def CAD(self, alpha=60):
        r = (
             # PCB
             cq.Workplane('XY').box(self.pcb_L, self.pcb_W, self.pcb_H)
             .faces('>Z').workplane().tag('pcb')
             .moveTo(-self.pcb_L/2+self.hole_H, 0).hole(self.Diameter_Screw_Hole/2)
             .moveTo((self.pcb_L-5)/2, 0).rect(6,9).cutThruAll()
             # Potentiometer
             .workplaneFromTagged("pcb").center(-1.7,(self.pcb_W-self.potent_W )/2-0.5)
             .rect(self.potent_L,self.potent_W).extrude(self.potent_H, combine=True)
             .faces('>Z').workplane().center(-(self.potent_L-self.potent_screw_Diam)/2+0.2,(self.potent_W-self.potent_screw_Diam)/2-0.2)
             .circle(self.potent_screw_Diam/2).extrude(self.potent_screw_H, combine=True)
             # Mic
             .workplaneFromTagged("pcb")#.center((Lc-Dm)/2,0)
             .transformed(offset=cq.Vector((self.pcb_L-self.mic_Dia)/2, 0, 0), rotate=cq.Vector(0, alpha, 0))
             .circle(self.mic_Dia/2).extrude(self.mic_H)
             # Pins
             .workplaneFromTagged("pcb").center(1-(self.pcb_L-self.pin_L)/2, 0)
             .rect(self.pin_L, self.pin_W).extrude(self.pin_H)
             .faces('<X').workplane(offset=-1)
             .pushPoints([(3.75,self.pin_H-self.pin_Dia),(1.25,self.pin_H-self.pin_Dia),(-1.25,self.pin_H-self.pin_Dia),(-3.75,self.pin_H-self.pin_Dia)])
             .rect(self.pin_Dia,self.pin_Dia).extrude(self.pins)
             )
        return r

###################################################################################

class Servo_SG90:
    def __init__(self):
        self.body_L, self.body_W, self.body_H             = 22.5, 12.0, 22.6 # SG90 body dims.
        self.Top_LargeCyl_Dia, self.Top_LargeCyl_H        = 12.0, 4.2        # SG90 top large cylinder [D,H]
        self.Top_SmallCyl_Dia, self.Top_SmallCyl_H        = 4.0, 4.2         # SG90 top small half cylinder [D,H]
        self.Shaf_Dia, self.Shaf_H                        = 4.8, 2.8         # SG90 shaf (cylinder) [D,H]
        self.ScrewBox_L, self.ScrewBox_W, self.ScrewBox_H = 32.3, 11.99, 2.5 # SG90 screws box dims.
        #-----------------
        self.ShafInCyl_Dia, self.ShafIn_H                 = 4.7, 2.0         # SG90 shaft inner cylinder [D,H]
        self.ShafOutCyl_Dia, self.ShafOut_H               = 7.0, 3.8         # SG90 shaft outer cylinder [D,H]
        self.ShafTail_LW, self.ShafTail_D,self.ShafTail_H = 16, 4.0, 1.4     # SG90 length, hight and Diameter of the tail of the shaft
    ######################
    def Motor(self):
        motor = (
                cq.Workplane('XY').box(self.body_L, self.body_W, self.body_H)
                # body
                .faces('>Z').workplane().tag("topPlane")
                .center((self.body_L-self.Top_LargeCyl_Dia)/2,0).circle(self.Top_LargeCyl_Dia/2).extrude(self.Top_LargeCyl_H)
                #large cylinder on the top of the body
                .workplaneFromTagged("topPlane")
                .center(self.body_L/2-self.Top_LargeCyl_Dia,0).circle(self.Top_SmallCyl_Dia/2).extrude(self.Top_SmallCyl_H)
                .faces('>Z').workplane().center(self.Top_LargeCyl_Dia/2,0)
                .polygon(12,self.Shaf_Dia).extrude(self.Shaf_H)
                # smaller cylinder on the top of the body
                .workplaneFromTagged("topPlane").workplane(offset=-self.ScrewBox_H).tag('screw')
                .rect(self.ScrewBox_L, self.ScrewBox_W).extrude(-self.ScrewBox_H)
                # plane for the screws
                .workplaneFromTagged("screw")
                .pushPoints([(-self.ScrewBox_L/2+3,0),(self.ScrewBox_L/2-3,0)]).hole(2)
                .pushPoints([(-self.ScrewBox_L/2+1,0),(self.ScrewBox_L/2-1,0)]).rect(3,1).cutThruAll()
                )
        return motor
    ######################
    def Shaft(self):
        shaft = (
              cq.Workplane()
              .circle(self.ShafOutCyl_Dia/2).polygon(12,self.ShafInCyl_Dia).extrude(self.ShafIn_H, combine=True)
              .faces('>Z').workplane()
              .circle(self.ShafOutCyl_Dia/2).extrude(self.ShafOut_H-self.ShafIn_H, combine=True)
              .sketch()
              .arc((0,0), self.ShafOutCyl_Dia/2, 0, 360.)
              .arc((self.ShafTail_LW,0), self.ShafTail_D/2, 0, 360.)
              .hull().finalize().extrude(self.ShafTail_H)
            )
        return shaft
    ######################
    def CAD(self, HReise=0, alpha=0, XY=False):
        motor = self.Motor()
        shaft = self.Shaft()
        # --------------------
        if XY:
            r = (
                  cq.Assembly()
                  .add(motor, color=cq.Color("blue"), name="Body",
                      loc=cq.Location((0,0,0),(0,0,1),90)
                      )
                  .add(shaft.rotate((0,0,-1),(0,0,1),90), 
                      loc=cq.Location((0,self.body_L/2-self.Top_LargeCyl_Dia/2,(self.body_H/2+self.Top_LargeCyl_H+HReise)),(0,0,1),alpha), 
                      color=cq.Color("gray"), name="Shaft")
                )
        else:
            r = (
                  cq.Assembly()
                  .add(motor, color=cq.Color("blue"), name="Body", loc=cq.Location((0,0,0),(0,0,1),0))
                  .add(shaft, 
                      loc=cq.Location((self.body_L/2-self.Top_LargeCyl_Dia/2,0,(self.body_H/2+self.Top_LargeCyl_H+HReise)),(0,0,1),alpha), 
                      color=cq.Color("gray"), name="Shaft")
                )
            # r = (
            #       cq.Assembly()
            #       .add(motor, color=cq.Color("blue"), name="Body", loc=cq.Location((0,0,0),(0,0,1),180))
            #       .add(shaft, 
            #           loc=cq.Location((0*self.body_L/2-self.Top_LargeCyl_Dia/2,0,(self.body_H/2+self.Top_LargeCyl_H+HReise)),(0,0,1),alpha), 
            #           color=cq.Color("gray"), name="Shaft")
            #     )
        return r

###################################################################################

# r = ESP32().CAD()
# r = LCD().CAD()
# r = HC_SR04().CAD()
# r = Mic().CAD(alpha=60)
# r = Servo_SG90().CAD(HReise=0, alpha=0, XY=False)

# show_object(r, options=dict(alpha=0.5))



