import os
from datetime import datetime
from detection.objdet import obj_det
from coord_mapping.coord import CoordPixel, Coord3D, CoordRobot #Probably find a way to clean this up
from coord_mapping.cam_coord_transform import CamCoordTransformer
from coord_mapping.robot_coord_transform import RobotCoordTransformer
from motor.motor_utils import robot_coord_to_servo
from controls.naive_controller import NaiveController
from controls.planned_controller import PlannedController

def save_pred(
		txt_file,
		detected_obj,
		pixel_coord,
		world_coord,
		robot_coord,
		):
	with open(txt_file, 'w') as f:
		obj, conf, xyxy, cls = detected_obj
		f.write(f'objs : {str(obj)} \n')
		f.write(f'cls  : {str(cls)} \n')
		f.write(f'confs: {conf} \n')
		f.write(f'xyxy: {xyxy} \n')

		f.write('\n')
		f.write(f'pixel_coord: {str(pixel_coord.u)} {str(pixel_coord.v)} \n')
		f.write(f'world_coord: {str(world_coord.x)} {str(world_coord.y)} {str(world_coord.z)} \n')
		f.write(f'robot_coord: {str(robot_coord.theta_1)} {str(robot_coord.theta_2)} {str(robot_coord.theta_3)} \n')

def run(
	target_objs = [39, 75],
	conf_threshold = 0.25, 
	target_depth = 200,
	planning = "naive",
):
	run_folder = os.path.join('runs', datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) 
	os.makedirs(run_folder, exist_ok=True)

	###1. Object Detection: Loops end when detected first vase/bottle
	detected_obj = obj_det(target_objs = target_objs, conf_threshold = conf_threshold, folder=run_folder)

	###2. Coordinate conversion: Convert object's coordinate to robot's world coordinate
	u1, v1, u2, v2 = detected_obj[2]
	u = int((u1 + u2) / 2)
	v = int((v1 + v2) / 2)
	pixel_coord = CoordPixel(u, v)
	print(pixel_coord)

	cam_coord_transformer = CamCoordTransformer()
	world_coord = cam_coord_transformer.pixel_to_world_coord(pixel_coord, target_depth)
	print(world_coord)


	###3. Config inference: From object's coordinate, infer robot's joints' angles
	robot_coord_transformer = RobotCoordTransformer()
	robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
	print(robot_coord)
		
	save_pred(
		txt_file=os.path.join(run_folder, 'predicted.txt'),
		detected_obj = detected_obj,
		pixel_coord = pixel_coord,
		world_coord = world_coord,
		robot_coord = robot_coord,
		)	
		
	if not robot_coord_transformer.is_above_ground(robot_coord):
		return "Object unattainable by the robot's configuration"

	###4. Target Motor Angle: From target robot angles in kinematics, infer target angles to be input in motors
	servo_angles = robot_coord_to_servo(robot_coord)
	with open(os.path.join(run_folder, 'predicted.txt'), 'a') as f:
		f.write(f'motor_input:  {str(servo_angles.servo1)} {str(servo_angles.servo2)} {str(servo_angles.servo3)} \n')
	print(servo_angles)
	
	'''
	###5. Execute
	if planning == 'naive':
		controller = NaiveController()
	else:
		# sequence = Planner.do_something()
		# controller = PlannedController(sequence)
		raise NotImplemented
	
	controller.execute(servo_angles)
	'''
	
	print('Donezo')
	
if __name__ == "__main__":
	run()
