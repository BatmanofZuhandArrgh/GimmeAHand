import pygame
from controls.controller import Controller
from controls.controls_utils import run_motor

ROTATION_SPEED = 2 # degrees per second

class JoystickController(Controller):
    def __init__(self) -> None:
        super().__init__()

        self.joystick = None
        self.joystick_init() 
        self.show_manual()
        
        self.axes = [0 for x in range(4)]
        self.buttons = [0 for x in range(10)]

        self.motor_counter = [0 for x in range(4)]

    def show_manual(self):
        print("==================================")
        print('Manual:')
        print(
        '''
        Developed on PS2 Wired Controller, using PyGame.  \n
        Press Select to quit\n
        Press Left and Right to control Servo 1 (Turning the arm left and right)\n
        Press Up and Down to control Servo 2\n
        Press 1 and 3 to control Servo 3\n
        Press 2 and 4 to control end-effector\n
        '''
        )

    def joystick_init(self):
        pygame.init()
        pygame.joystick.init()

        # Check if there are any joysticks
        if pygame.joystick.get_count() == 0:
            print("No joystick found.")
        else:
            # Get the first joystick
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print("Initialized joystick:", self.joystick.get_name())

    def joystick_quit(self):
        pygame.quit()

    def manual_control(self):
        self.go_online()

        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Read joystick input
            for i in range(self.joystick.get_numaxes()):
                axis = self.joystick.get_axis(i)
                # print(f"Axis {i}: {axis}")   

                if i == 1 and axis <-0.5: #Up
                    self.axes[2] = 1
                elif i == 1 and axis > 0.5: #Down
                    self.axes[3] = 1
                elif i == 0 and axis <-0.5: #Left
                    self.axes[0] = 1
                    break
                elif i == 0 and axis > 0.5: #Right
                    self.axes[1] = 1
                    break
                else: 
                    self.axes = [0 for x in range(4)]
            # print(f"Axes: {self.axes}: Up Down Left Right")

            for i in range(self.joystick.get_numbuttons()):
                button = self.joystick.get_button(i)
                self.buttons[i] = button
            # print(f"Buttons: {self.buttons}")

            # Add a small delay to avoid maxing out CPU
            pygame.time.delay(100) #1 second per input

            #Escape game
            if self.buttons[8] == 1:
                running = False
                self.joystick_quit()
                
                self.go_offline()
                self.all_motor_relax()
                self.end_routine()

                print('Escape')
                break
            
            #Servo 1
            if self.axes[0] == 1:
                self.motor_counter[0] -= 1  
                self.servos['1'].angle -= ROTATION_SPEED
            elif self.axes[1] == 1:
                self.motor_counter[0] += 1 
                self.servos['1'].angle += ROTATION_SPEED

            #Servo 2
            if self.axes[2] == 1:
                self.motor_counter[1] += 1      
                self.servos['2'].angle += ROTATION_SPEED      
            elif self.axes[3] == 1:
                self.motor_counter[1] -= 1
                self.servos['2'].angle -= ROTATION_SPEED

            #Servo 3
            if self.buttons[0] == 1:
                self.motor_counter[2] += 1
                self.servos['3'].angle += ROTATION_SPEED            
            elif self.buttons[2] == 1:
                self.motor_counter[2] -= 1 
                self.servos['3'].angle -= ROTATION_SPEED

            #EE
            if self.buttons[1] == 1: #Open
                self.motor_counter[3] += 1
                cur_angle = self.servos['ee'].angle 
                self.servos['ee'].angle = cur_angle - ROTATION_SPEED if cur_angle > 50 + ROTATION_SPEED else cur_angle
            
            elif self.buttons[3] == 1: #Close
                self.motor_counter[3] -= 1 
                cur_angle = self.servos['ee'].angle 
                self.servos['ee'].angle = cur_angle + ROTATION_SPEED if cur_angle < 90 - ROTATION_SPEED else cur_angle

            print(self.motor_counter)
            print('========================')

if __name__ == '__main__':
    controller = JoystickController()
    controller.manual_control()
