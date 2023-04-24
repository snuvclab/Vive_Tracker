# Copyright (c) Facebook, Inc. and its affiliates.

import argparse
import numpy as np
import os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from fairmotion_vis import camera, gl_render, glut_viewer
from fairmotion_utils import constants
from fairmotion_ops import conversions
# from fairmotion.data import bvh, asfamc
# from fairmotion.ops import conversions, math, motion as motion_ops
# from fairmotion.utils import utils

from IPython import embed
# import yaml

class ViveTrackerViewer(glut_viewer.Viewer):

    def __init__(
        self,
        v_track_updater,
        # config,
        play_speed=1.0,
        scale=1.0,
        thickness=1.0,
        render_overlay=False,
        hide_origin=False,
        **kwargs,
    ):
        # Load vive tracker updater
        self.vive_updater = v_track_updater
        # vis related info
        self.update_tracker = False
        self.cur_time = 0.0
        self.play_speed = 1.0
        super().__init__(**kwargs)

    def keyboard_callback(self, key):
        if key == b"s":
            self.update_tracker = True
            self.cur_time = 0.0
            self.time_checker.begin()
        if key == b" ":
            self.update_tracker = not self.update_tracker
        else:
            return False
        return True
    
    def render_tracker(self):
        for t in self.vive_updater.tracking_result:
            gl_render.render_sphere(t, r=0.01)
            gl_render.render_transform(t, scale=0.07, use_arrow=True)
    
    def render_callback(self):
        if self.update_tracker:
            self.vive_updater.update()
        self.render_tracker()

        gl_render.render_ground(
            size=[100, 100],
            color=[0.8, 0.8, 0.8],
            axis="y",
            origin=True,
            use_arrow=True,
            fillIn=True
        )

    def idle_callback(self):
        if not self.update_tracker:
            return
        time_elapsed = self.time_checker.get_time(restart=False)
        self.cur_time += self.play_speed * time_elapsed
        self.time_checker.begin()

    def overlay_callback(self):
        # if self.render_overlay:
        w, h = self.window_size
        gl_render.render_text(
            f"Press S to start tracking",
            pos=[0.05 * w, 0.05 * h],
            font=GLUT_BITMAP_TIMES_ROMAN_24,
        )

        gl_render.render_text(
            f"Time: {self.cur_time}",
            pos=[0.05 * w, 0.95 * h],
            font=GLUT_BITMAP_TIMES_ROMAN_24,
        )


def main(args):

    cam = camera.Camera(
        pos=np.array(args.camera_position),
        origin=np.array(args.camera_origin),
        vup=np.array([0,1,0]),
        fov=45.0,
    )
    viewer = ViveTrackerViewer(
        config=config,
        play_speed=args.speed,
        scale=args.scale,
        thickness=args.thickness,
        render_overlay=args.render_overlay,
        hide_origin=args.hide_origin,
        title="Boids Simulation Viewer",
        cam=cam,
        size=(1920, 1280),
    )
    viewer.run()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="Visualize BVH file with block body"
#     )
#     parser.add_argument("--config", type=str, default="")

#     # ########################### render options ##############################
#     # parser.add_argument("--scale", type=float, default=1.0)
#     # parser.add_argument(
#     #     "--thickness", type=float, default=1.0,
#     #     help="Thickness (radius) of character body"
#     # )
#     # parser.add_argument("--speed", type=float, default=1.0)
#     # parser.add_argument(
#     #     "--axis-up", type=str, choices=["x", "y", "z"], default="y"
#     # )
#     # parser.add_argument(
#     #     "--axis-face", type=str, choices=["x", "y", "z"], default="z"
#     # )
#     # parser.add_argument(
#     #     "--camera-position",
#     #     nargs="+",
#     #     type=float,
#     #     required=False,
#     #     default=(10.0, 10.0, 10.0),
#     # )
#     # parser.add_argument(
#     #     "--camera-origin",
#     #     nargs="+",
#     #     type=float,
#     #     required=False,
#     #     default=(0.0, 0.0, 0.0),
#     # )
#     # parser.add_argument("--hide-origin", action="store_true")
#     # parser.add_argument("--render-overlay", action="store_true")
#     # args = parser.parse_args()
#     # assert len(args.camera_position) == 3 and len(args.camera_origin) == 3, (
#     #     "Provide x, y and z coordinates for camera position/origin like "
#     #     "--camera-position x y z"
#     # )
#     main(args)
