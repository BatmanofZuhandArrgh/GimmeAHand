import numpy as np
import pickle
from coord import CoordPixel, Coord3D


class CamCoordTransformer:
	def __init__(self, camera_angle: float = 20.0, intrinsic_mat_file: str = None, pixel_width: int = 2592, pixel_height: int = 1944):
		self.intrinsic_mat = self.load_intrinsic_mat(intrinsic_mat_file, pixel_width, pixel_height)
		self.rotation_mat = self.get_rotation_mat(camera_angle)

	def load_intrinsic_mat(self, mat_file: str = None, pixel_width: int = 2592, pixel_height: int = 1944):
		""" mat_file: path to pickled intrinsic matrix file (if None, use f=2500 based on measured intrinsic matrix) """
		mat = None
		if mat_file is None:
			cam_f = 2500.0
			mat = np.array([
				[cam_f,   0.0,   0.0],
				[  0.0, cam_f,   0.0],
				[  0.0,   0.0,   1.0],
			])
		else:
			with open(mat_file, "rb") as f:
				mat = np.array(pickle.load(f))
		mat[0, 2] = (pixel_width - 1) / 2.0
		mat[1, 2] = (pixel_height - 1) / 2.0
		return mat

	def get_rotation_mat(self, camera_angle: float = 20.0):
		""" camera_angle: degree compared to vertical axis (default to 20 degree based on measured extrinsic matrix) """
		s = np.sin(np.deg2rad(camera_angle))
		c = np.cos(np.deg2rad(camera_angle))
		mat = np.array([
			[1.0, 0.0, 0.0],
			[0.0,  -c,  -s],
			[0.0,   s,  -c],
		])
		return mat

	def pixel_to_world_coord(self, pixel_coord: CoordPixel, target_z: float) -> Coord3D:
		""" convert pixel coord to world 3D coord (origin is at the base of the camera position, target depth must be given) """
		target_z = np.absolute(target_z)
		img_coord = np.array([pixel_coord.u, pixel_coord.v, 1.0])
		cam_coord = np.matmul(np.linalg.inv(self.intrinsic_mat), img_coord)
		cam_coord = cam_coord / cam_coord[2] * target_z
		world_coord = np.matmul(np.linalg.inv(self.rotation_mat), cam_coord)
		world_coord = world_coord / world_coord[2] * target_z * -1.0
		result = Coord3D(x=world_coord[0], y=world_coord[1], z=world_coord[2])
		return result


if __name__ == "__main__":
	cam_coord_transformer = CamCoordTransformer(intrinsic_mat_file="cam_calibrate/intrinsic_mat.pkl")
	u = int(input("Input u: "))
	v = int(input("Input v: "))
	pixel_coord = CoordPixel(u, v) # pixel
	target_z = 250.0 # 250 mm
	world_coord = cam_coord_transformer.pixel_to_world_coord(pixel_coord, target_z)
	print(world_coord)