from controller import Robot, Camera
import numpy as np

class HROSbot: 

    def __init__(self, bot):
        self.robot = bot
        self.robotTimestep = int(self.robot.getBasicTimeStep())
        self.TIMESTEP = 64
        #
        self.ruedaDerechaSuperior = self.robot.getDevice("fr_wheel_joint")
        self.ruedaDerechaInferior = self.robot.getDevice("rr_wheel_joint")
        self.ruedaIzquierdaSuperior = self.robot.getDevice("fl_wheel_joint")
        self.ruedaIzquierdaInferior = self.robot.getDevice("rl_wheel_joint")
        #
        self.ruedaDerechaSuperior.setPosition(float('inf'))
        self.ruedaDerechaInferior.setPosition(float('inf'))
        self.ruedaIzquierdaInferior.setPosition(float('inf'))
        self.ruedaIzquierdaSuperior.setPosition(float('inf'))
        #
        self.giroscopio = self.robot.getDevice("imu gyro")
        self.acelerometro = self.robot.getDevice("imu accelerometer")
        self.lidar = self.robot.getDevice("laser")
        #
        self.giroscopio.enable(self.robotTimestep)
        self.acelerometro.enable(self.robotTimestep)
        self.lidar.enable(self.robotTimestep)
        #
        self.frontLeftSensor = self.robot.getDevice("fl_range")
        self.frontRightSensor = self.robot.getDevice("fr_range")
        self.rearLeftSensor = self.robot.getDevice("rl_range")
        self.rearRightSensor = self.robot.getDevice("rr_range")
        #
        self.frontLeftSensor.enable(self.robotTimestep)
        self.frontRightSensor.enable(self.robotTimestep)
        self.rearLeftSensor.enable(self.robotTimestep)
        self.rearRightSensor.enable(self.robotTimestep)
        #
        self.frontLeftPositionSensor = self.robot.getDevice("front left wheel motor sensor")
        self.frontRightPositionSensor = self.robot.getDevice("front right wheel motor sensor")
        self.rearLeftPositionSensor = self.robot.getDevice("rear left wheel motor sensor")
        self.rearRightPositionSensor = self.robot.getDevice("rear right wheel motor sensor")
        #
        self.frontLeftPositionSensor.enable(self.TIMESTEP)
        self.frontRightPositionSensor.enable(self.TIMESTEP)
        self.rearLeftPositionSensor.enable(self.TIMESTEP)
        self.rearRightPositionSensor.enable(self.TIMESTEP)
        #
        self.anteriorValorPositionSensor = [0,0,0,0]
        self.DefaultPositionSensorAnterior()
        self.limiteSensor = 2.0
        self.radioRueda = 0.0425
        self.encoderUnit = (2*np.pi*self.radioRueda)/6.28 #
 
    def DefaultPositionSensorAnterior(self):
        for i in range(3) :
            self.anteriorValorPositionSensor[i]=0

    def metrosRecorridos(self):
        ps_values = [0, 0]
        distancia = [0, 0]
        distancia[0]=0
        distancia[1]=0
        ps_values[0] = self.frontLeftPositionSensor.getValue()-self.anteriorValorPositionSensor[0]
        ps_values[1] = self.frontRightPositionSensor.getValue()-self.anteriorValorPositionSensor[1]
        #print("position values: {} {}".format(ps_values[0],ps_values[1]))
        for i in range(2):
            distancia[i] = ps_values[i]*self.encoderUnit

        #print("metros recorridos: {} {}".format(distancia[0], distancia[1]))

        return distancia;


    def avanzar(self, distancia, velocidad):
        print("Avanzar")
        dist = [0, 0]
        dist[0] = 0
        dist[1] = 0

        self.robot.step(self.robotTimestep)
        fls =self.frontLeftSensor.getValue() 
        frs = self.frontRightSensor.getValue()

        if((fls>distancia and frs>distancia)):
            while ((dist[0]<distancia or dist[1]<distancia)and(self.robot.step(self.robotTimestep) != -1)):
                dist =  self.metrosRecorridos()
                self.ruedaDerechaSuperior.setVelocity(velocidad)
                self.ruedaDerechaInferior.setVelocity(velocidad)
                self.ruedaIzquierdaInferior.setVelocity(velocidad)
                self.ruedaIzquierdaSuperior.setVelocity(velocidad)
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)
        self.anteriorValorPositionSensor[0] = self.frontLeftPositionSensor.getValue()
        self.anteriorValorPositionSensor[1] = self.frontRightPositionSensor.getValue()

    def retroceder(self, distancia, velocidad):
        print("Retroceder")
        dist = [0, 0]
        distancia = -1*distancia
        self.robot.step(self.robotTimestep)
        rls = self.rearLeftSensor.getValue()
        rrs = self.rearRightSensor.getValue()

        dist[0] = 0
        dist[1] = 0

        if((rls>distancia and rrs>distancia)):
            while ((dist[0]>distancia or dist[1]>distancia)and(self.robot.step(self.robotTimestep) != -1)):
                dist =  self.metrosRecorridos()
                self.ruedaDerechaSuperior.setVelocity(-velocidad)
                self.ruedaDerechaInferior.setVelocity(-velocidad)
                self.ruedaIzquierdaInferior.setVelocity(-velocidad)
                self.ruedaIzquierdaSuperior.setVelocity(-velocidad)
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)
        self.anteriorValorPositionSensor[0] = self.frontLeftPositionSensor.getValue()
        self.anteriorValorPositionSensor[1] = self.frontRightPositionSensor.getValue()
    

    def giroDerecha(self):
        print("Derecha")
        velocidad = 2.0
        vel_atras = 3.0
        m_atras =0.2
        
        self.robot.step(self.robotTimestep)
        rls = self.rearLeftSensor.getValue()
        rrs = self.rearRightSensor.getValue()

      
        if((rls>m_atras and rrs>m_atras)):
            self.retroceder(m_atras,vel_atras)
       
        ang_z = 0

        while ((self.robot.step(self.robotTimestep) != -1)and(ang_z>(-0.5*np.pi))):
            gyroZ =self.giroscopio.getValues()[2]
            ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
           
            self.ruedaDerechaSuperior.setVelocity(0.0)
            self.ruedaDerechaInferior.setVelocity(0.0)
            self.ruedaIzquierdaInferior.setVelocity(velocidad)
            self.ruedaIzquierdaSuperior.setVelocity(velocidad)
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)


    def giroIzquierda(self):
        velocidad = 2.0
        vel_atras = 3.0
        m_atras =0.2
        
        self.robot.step(self.robotTimestep)
        rls = self.rearLeftSensor.getValue()
        rrs = self.rearRightSensor.getValue()

      
        if((rls>m_atras and rrs>m_atras)):
            self.retroceder(m_atras,vel_atras)
       
        ang_z = 0

        while ((self.robot.step(self.robotTimestep) != -1)and(ang_z<(0.5*np.pi))):
            gyroZ =self.giroscopio.getValues()[2]
            ang_z=ang_z+(gyroZ*self.robotTimestep*0.001)
           
            self.ruedaDerechaSuperior.setVelocity(velocidad)
            self.ruedaDerechaInferior.setVelocity(velocidad)
            self.ruedaIzquierdaInferior.setVelocity(0.0)
            self.ruedaIzquierdaSuperior.setVelocity(0.0)
            
        self.ruedaDerechaSuperior.setVelocity(0)
        self.ruedaDerechaInferior.setVelocity(0)
        self.ruedaIzquierdaInferior.setVelocity(0)
        self.ruedaIzquierdaSuperior.setVelocity(0)