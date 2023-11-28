import numpy as np
import pickle
from coord_mapping.coord import CoordPixel, Coord3D


class CamCoordTransformer:
	def __init__(
			self,
			cam_offset: Coord3D = Coord3D(88, 68, 72),
			cam_angle: float = 20.0, 
			intrinsic_mat_file: str = None,
			pixel_width: int = 640, #2592,
			pixel_height: int = 480, #1944,
	):
		'''
		cam_offset: offset in mm from the actually world coordinate origin
		cam_angle: pitch of camera from horizontal axis
		intrinsic_mat_file: path to pickled intrinsic matrix file 
		'''
		self.cam_offset = cam_offset
		self.intrinsic_mat = self.load_intrinsic_mat(intrinsic_mat_file, pixel_width, pixel_height)
		self.rotation_mat = self.get_rotation_mat(cam_angle)

	def load_intrinsic_mat(self, mat_file: str, pixel_width: int, pixel_height: int):
		"""mat_file: path to pickled intrinsic matrix file (if None, use f=2500 based on measured intrinsic matrix)"""
		mat = None
		if mat_file is None:
			cam_f = 2500.0
			fx = cam_f / 2592.0 * pixel_width
			fy = cam_f / 1944.0 * pixel_height
			mat = np.array([
				[  fx, 0.0, 0.0],
				[ 0.0,  fy, 0.0],
				[ 0.0, 0.0, 1.0],
			])
		else:
			with open(mat_file, "rb") as f:
				mat = np.array(pickle.load(f))

		# cx, cy assigned with actual center of the image
		mat[0, 2] = (pixel_width - 1) / 2.0
		mat[1, 2] = (pixel_height - 1) / 2.0
		return mat

	def get_rotation_mat(self, cam_angle: float):
		"""camera_angle: degree compared to vertical axis (default to 20 degree based on measured extrinsic matrix)"""
		s = np.sin(np.deg2rad(cam_angle))
		c = np.cos(np.deg2rad(cam_angle))
		mat = np.array([   #TODO verifyy
			[1.0, 0.0, 0.0],
			[0.0,  -c,  -s],
			[0.0,   s,  -c],
		])
		return mat

	def pixel_to_world_coord(self, pixel_coord: CoordPixel, target_z: float) -> Coord3D:
		"""convert pixel coord to world 3D coord (target depth must be given)"""
		target_z = np.absolute(target_z)
		img_coord = np.array([pixel_coord.u, pixel_coord.v, 1.0])
		cam_coord = np.matmul(np.linalg.inv(self.intrinsic_mat), img_coord)
		cam_coord = cam_coord / cam_coord[2] * target_z
		world_coord = np.matmul(np.linalg.inv(self.rotation_mat), cam_coord)
		world_coord = world_coord / world_coord[2] * target_z * -1.0
		x = world_coord[0] + self.cam_offset.x
		y = world_coord[1] + self.cam_offset.y
		z = world_coord[2] + self.cam_offset.z
		return Coord3D(x, y, z)


if __name__ == "__main__":
	cam_coord_transformer = CamCoordTransformer()
	u = int(input("Input u: "))
	v = int(input("Input v: "))
	pixel_coord = CoordPixel(u, v) # pixel
	target_z = 250.0 # 250 mm
	world_coord = cam_coord_transformer.pixel_to_world_coord(pixel_coord, target_z)
	print(world_coord)
