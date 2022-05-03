import logging
import os

import bpy
from numpy import arange
from vlips import Beacon, Camera, ExifWriter, Scene

from .camera_movement import CameraMovement
from .camera_orientation import CameraOrientation
from .constants import *

log = logging.getLogger(__name__)


class VLIPSSimulation:

    # region Actions

    @staticmethod
    def empty_scene(context):
        """
        Remove every item from the scene to start it from scratch.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        """

        log.info("Empty scene")
        log.debug(f"VLIPSSimulation.empty_scene("
                  f"context={context})")

        # Remove objects
        for scene_object in context.scene.objects:
            if scene_object.type == "MESH":
                scene_object.hide_set(False)
                scene_object.select_set(state=True)
            elif scene_object.type == "GRID":
                scene_object.select_set(state=True)
            elif scene_object.type == "FONT":
                scene_object.select_set(state=True)
            else:
                scene_object.select_set(state=False)
            bpy.data.objects.remove(scene_object, do_unlink=True)

        # Remove materials
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)

        # Remove lights
        for light in bpy.data.lights:
            bpy.data.lights.remove(light)

        # Remove cameras
        for camera in bpy.data.cameras:
            bpy.data.cameras.remove(camera)

        # Remove collections
        for collection in bpy.data.collections:
            bpy.data.collections.remove(collection)

    @staticmethod
    def setup_scene(
            context,
            tile_side,
            floor_side_tiles
    ):
        """
        Configure the scene for the simulation.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param tile_side: size of the side of each of the tiles shown in the
        floor, in millimeters.
        :param floor_side_tiles: number of tiles in the floor.
        """

        log.info("Setup scene")
        log.debug(f"VLIPSSimulation.setup_scene("
                  f"context={context}, "
                  f"tile_side={tile_side}, "
                  f"floor_side_tiles={floor_side_tiles})")

        # Set the scene units
        context.scene.unit_settings.system = "METRIC"
        context.scene.unit_settings.length_unit = "METERS"
        context.scene.unit_settings.scale_length = 0.001
        context.space_data.overlay.grid_scale = 0.001
        context.space_data.clip_end = 1e+06
        context.scene.unit_settings.system_rotation = "DEGREES"

        log.debug(f"- context.scene.unit_settings.system={context.scene.unit_settings.system}")
        log.debug(f"- context.scene.unit_settings.system_rotation={context.scene.unit_settings.system_rotation}")

        # Set some properties of the scene that depends on the camera
        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)
        if camera_properties.orientation == CameraOrientation.LANDSCAPE.value.identifier:
            context.scene.render.resolution_x = camera_properties.resolution_width
            context.scene.render.resolution_y = camera_properties.resolution_height
        else:
            context.scene.render.resolution_x = camera_properties.resolution_height
            context.scene.render.resolution_y = camera_properties.resolution_width
        context.scene.render.resolution_percentage = 100

        log.debug(f"- context.scene.render.resolution_x={context.scene.render.resolution_x}")
        log.debug(f"- context.scene.render.resolution_y={context.scene.render.resolution_y}")
        log.debug(f"- context.scene.render.resolution_percentage={context.scene.render.resolution_percentage}")
        log.debug(f"- context.scene.unit_settings.scale_length={context.scene.unit_settings.scale_length}")

    # endregion

    @staticmethod
    def zoom_to_scene():
        """
        Zoom to have the room in the viewport
        """

        log.info("Zoom to scene")
        log.debug("VLIPSSimulation.zoom_to_scene()")

        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for region in area.regions:
                    if region.type == "WINDOW":
                        bpy.ops.view3d.view_all(
                            use_all_regions=True,
                            center=True)

    @staticmethod
    def setup_room(
            context,
            name,
            width,
            depth,
            height,
            thickness
    ):
        """
        Set the room of the simulation. If the room doesn't exist, create one.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param name: name given to the room, so it can be later accessed.
        :param width: length of the room in the X-axis, in millimeters.
        :param depth: length of the room in the Y-axis, in millimeters.
        :param height: height of the room, in the Z-axis, in millimeters.
        :param thickness: thickness of the borders of the room, in millimeters.
        """

        log.info("Set the room up")
        log.debug(f"VLIPSSimulation.setup_room("
                  f"context={context}, "
                  f"name={name}, "
                  f"width={width}, "
                  f"depth={depth}, "
                  f"height={height}, "
                  f"thickness={thickness})")

        # Create the room if it doesn't exist
        if name not in context.scene.objects:
            log.debug("- room doesn't exist: create")

            bpy.ops.mesh.primitive_cube_add()
            room = context.active_object
            room.name = name
            room.modifiers.new(name="Wireframe", type="WIREFRAME")
        else:
            log.debug("- room already exists")

            room = context.scene.objects[name]

        # Set camera dimensions and thickness
        room.dimensions = (width, depth, height)
        room.location = (0, 0, height / 2)
        # room.modifiers["Wireframe"].thickness = thickness

        log.debug(f"- room.dimensions={room.dimensions}")
        log.debug(f"- room.location={room.location}")
        log.debug(f"- room.modifiers[\"Wireframe\"].thickness={room.modifiers['Wireframe'].thickness}")

    @staticmethod
    def setup_beacon(
            context,
            name,
            width,
            height,
            room_properties=None
    ):
        """
        Set the beacon of the simulation. If the beacon doesn't exit, create
        one.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param name: name given to the beacon, so it can be later accessed.
        :param width: width of the beacon, in millimeters.
        :param height: height of the beacon, in millimeters.
        :param room_properties: properties of the room. Optional. Passed
        directly only when it can be out of sync like, for example, in a chain
        operation (room height changed, so beacon location should too).
        """

        log.info("Set the beacon up")
        log.debug(f"VLIPSSimulation.setup_beacon("
                  f"context={context}, "
                  f"name={name}, "
                  f"width={width}, "
                  f"height={height}, "
                  f"room_properties={room_properties})")

        # Create the beacon if it doesn't exist
        if name not in context.scene.objects:
            log.debug("- beacon doesn't exist: create")

            bpy.ops.mesh.primitive_plane_add()
            beacon = context.active_object
            beacon.name = name
        else:
            log.debug("- beacon already exists")

            beacon = context.scene.objects[name]

        # Set the beacon dimensions, location, and rotation
        beacon.dimensions = (width, height, 0)

        if room_properties is None:
            room_properties = context.window_manager.operator_properties_last(
                SETUP_ROOM_OPERATOR_NAME)

        beacon_location = (
            0,
            0,
            room_properties.height)
        beacon.location = beacon_location
        beacon_rotation = DEFAULT_BEACON_ROTATION
        beacon.rotation_euler = (
            math.radians(beacon_rotation[0]),
            math.radians(beacon_rotation[1]),
            math.radians(beacon_rotation[2]))

        # Configure the beacon so it is a light source
        material = bpy.data.materials.new(name="Plane Light Emission Shader")
        material.use_nodes = True
        material_output = material.node_tree.nodes.get("Material Output")
        emission = material.node_tree.nodes.new("ShaderNodeEmission")
        emission.inputs["Strength"].default_value = 1.0
        material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])
        material.diffuse_color = (1, 1, 1, 1)
        beacon.active_material = material

        log.debug(f"- beacon.dimensions={beacon.dimensions}")
        log.debug(f"- beacon.location={beacon.location}")
        log.debug(f"- beacon.rotation_euler={beacon.rotation_euler}")
        log.debug(f"- beacon.active_material={beacon.active_material}")

    @staticmethod
    def setup_camera(
            context,
            name,
            make,
            model,
            orientation,
            facing,
            resolution_width,
            resolution_height,
            focal_length,
            pixel_size,
            beacon_distance,
            rotation_x_angle,
            rotation_z_angle,
            show_fov,
            scene_properties=None,
            room_properties=None,
            beacon_properties=None,
            x=None,
            y=None
    ):
        """
        Set the camera of the simulation. If the camera doesn't exit, create
        one.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param name: name given to the camera, so it can be later accessed.
        :param make: name of the make this camera tries to mimic.
        :param model: name of the model this camera tries to mimic.
        :param orientation: portrait or landscape.
        :param facing: is the camera front of back facing?
        :param resolution_width: width of the photos taken by the camera, in
        pixels.
        :param resolution_height: height of the photos taken by the camera, in
        pixels.
        :param focal_length: focal length of the lens/sensor couple, in
        millimeters.
        :param pixel_size: size of each pixel in the sensor, in millimeters.
        :param beacon_distance: distance between the beacon and the camera, in
        millimeters.
        :param rotation_x_angle: rotation around camera's X axis, in degrees
        (pitch).
        :param rotation_z_angle: rotation around camera's Z axis, in degrees
        (yaw).
        :param show_fov: draw camera's field of vision on the floor.
        :param scene_properties: properties of the scene. Optional. Passed
        directly only when it can be out of sync like, for example, in a chain
        operation (tile side changed, so beacon FOV should too).
        :param room_properties: properties of the room. Optional. Passed
        directly only when it can be out of sync like, for example, in a chain
        operation (room height changed, so beacon location should too).
        :param beacon_properties: properties of the beacon. Optional. Passed
        directly only when it can be out of sync like, for example, in a chain
        operation (beacon location changed, so camera location should too).
        :param x: if provided, it will change the position of the camera to that
        x coordinate when the beacon is on the ceiling.
        :param y: if provided, it will change the position of the camera to that
        y coordinate when the beacon is on the ceiling.
        """

        log.info("Set the camera up")
        log.debug(f"VLIPSSimulation.setup_camera("
                  f"context={context}, "
                  f"name={name}, "
                  f"make={make}, "
                  f"model={model}, "
                  f"orientation={orientation}, "
                  f"facing={facing}, "
                  f"resolution_width={resolution_width}, "
                  f"resolution_height={resolution_height}, "
                  f"focal_length={focal_length}, "
                  f"pixel_size={pixel_size}, "
                  f"beacon_distance={beacon_distance}, "
                  f"rotation_x_angle={rotation_x_angle}, "
                  f"rotation_z_angle={rotation_z_angle}, "
                  f"show_fov={show_fov}, "
                  f"scene_properties={scene_properties}, "
                  f"room_properties={room_properties}, "
                  f"beacon_properties={beacon_properties}, "
                  f"x={x}, "
                  f"y={y})")

        # Create the camera if it doesn't exist
        if name not in context.scene.objects:
            log.debug("- camera doesn't exist: create")

            bpy.ops.object.camera_add()
            camera = context.active_object
            camera.name = name
        else:
            log.debug("- camera already exists")

            camera = context.scene.objects[name]

        # Load room and beacon properties
        if room_properties is None:
            room_properties = context.window_manager.operator_properties_last(
                SETUP_ROOM_OPERATOR_NAME)
        if beacon_properties is None:
            beacon_properties = context.window_manager.operator_properties_last(
                SETUP_BEACON_OPERATOR_NAME)

        # Calculate the position of the camera, given its distance and angle
        # relative to the beacon. The camera is at the same height as the
        # beacon
        beacon = context.scene.objects[beacon_properties.name]
        if x is None and y is None:
            x = beacon.location.x
            y = beacon.location.y
        z = room_properties.height - beacon_distance
        camera_rotation = (
            DEFAULT_CAMERA_ROTATION[0] - rotation_x_angle,
            DEFAULT_CAMERA_ROTATION[1],
            DEFAULT_CAMERA_ROTATION[2] - rotation_z_angle)

        # Set camera location and rotation
        camera.location = (x, y, z)
        camera.rotation_euler = (
            math.radians(camera_rotation[0]),
            math.radians(camera_rotation[1]),
            math.radians(camera_rotation[2])
        )

        log.debug(f"- camera.location={camera.dimensions}")
        log.debug(f"- camera.rotation_euler={camera.rotation_euler}")

        # Set scene and camera configuration given the camera properties
        camera.data.lens = focal_length
        camera.data.sensor_width = resolution_width * pixel_size
        camera.data.display_size = 150
        camera.data.clip_end = 1e+06

        context.scene.camera = camera
        if orientation == CameraOrientation.LANDSCAPE.value.identifier:
            context.scene.render.resolution_x = resolution_width
            context.scene.render.resolution_y = resolution_height
        else:
            context.scene.render.resolution_x = resolution_height
            context.scene.render.resolution_y = resolution_width

        log.debug(f"- camera.data.lens={camera.data.lens}")
        log.debug(f"- camera.data.sensor_width={camera.data.sensor_width}")
        log.debug(f"- context.scene.render.resolution_x={context.scene.render.resolution_x}")
        log.debug(f"- context.scene.render.resolution_y={context.scene.render.resolution_y}")

        # FOV
        VLIPSSimulation.update_camera_fov(
            context=context,
            name=name,
            focal_length=focal_length,
            pixel_size=pixel_size,
            beacon_distance=beacon_distance,
            show_fov=show_fov,
            scene_properties=scene_properties,
            room_properties=room_properties,
            beacon_properties=beacon_properties)

        # Show texts on the wall
        texts_properties = context.window_manager.operator_properties_last(
            SETUP_TEXTS_OPERATOR_NAME)

        VLIPSSimulation.setup_texts(
            context=context,
            font_size=texts_properties.font_size,
            camera_beacon_distance=beacon_distance,
            camera_x=x,
            camera_y=y,
            camera_rotation_x_angle=rotation_x_angle,
            camera_rotation_z_angle=rotation_z_angle)

        camera.select_set(True)
        context.view_layer.objects.active = camera

    @staticmethod
    def update_camera_fov(
            context,
            name,
            focal_length,
            pixel_size,
            beacon_distance,
            show_fov,
            scene_properties,
            room_properties,
            beacon_properties
    ):
        """
        Update camera's Field of Vision (FOV) given the camera properties.

        Note: you will see lots of operations here that could be performed with
        less repetition, overwriting values. It is intentional, as the different
        FOVs calculated will be added to the viewport for future reference.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param name: name given to the camera, so it can be later accessed.
        :param focal_length: focal length of the lens/sensor couple, in
        millimeters.
        :param pixel_size: size of each pixel in the sensor, in millimeters.
        :param beacon_distance: distance between the beacon and the camera, in
        millimeters.
        :param show_fov: draw camera's field of vision on the floor.
        :param scene_properties: properties of the scene.
        :param room_properties: properties of the room.
        :param beacon_properties: properties of the beacon.
        """

        log.info("Update camera's Field of Vision (FOV)")
        log.debug(f"VLIPSSimulation.update_camera_fov("
                  f"context={context}, "
                  f"name={name}, "
                  f"focal_length={focal_length}, "
                  f"pixel_size={pixel_size}, "
                  f"beacon_distance={beacon_distance}, "
                  f"show_fov={show_fov}, "
                  f"scene_properties={scene_properties}, "
                  f"room_properties={room_properties}, "
                  f"beacon_properties={beacon_properties})")

        # Add the collection that will contain the different steps needed to
        # calculate the FOV.
        if CAMERA_FOV_COLLECTION_NAME not in bpy.data.collections:
            fov_collection = bpy.data.collections.new(CAMERA_FOV_COLLECTION_NAME)
            context.scene.collection.children.link(fov_collection)
        else:
            fov_collection = bpy.data.collections[CAMERA_FOV_COLLECTION_NAME]

        # Get the size of the tiles for the FOV.
        if scene_properties is None:
            scene_properties = context.window_manager.operator_properties_last(
                SETUP_SCENE_OPERATOR_NAME)
        tile_side = scene_properties.tile_side

        # Calculate camera sensor dimensions, resolution_x and y are set
        # depending on camera orientation.
        camera_sensor_width = context.scene.render.resolution_x * pixel_size
        camera_sensor_height = context.scene.render.resolution_y * pixel_size

        # Calculate the dimensions of the area covered by the lens, this is,
        # the FOV, as we know the distance between the camera and the
        # beacon. This is done with basic trigonometry, as the triangles are
        # similar.
        fov_full_width = camera_sensor_width * beacon_distance / focal_length
        fov_full_height = camera_sensor_height * beacon_distance / focal_length

        # Subtract half a beacon around the perimeter of the FOV to count
        # for the need of having to move the camera to the fringe of said
        # FOV. Half in one side, half in the other, is a full beacon.
        fov_beacon_width = fov_full_width - beacon_properties.width
        fov_beacon_height = fov_full_height - beacon_properties.height

        # Adjust the dimensions of the FOV so only full tiles can fit into
        # it.
        fov_width_in_tiles_original = fov_beacon_width // tile_side
        fov_height_in_tiles_original = fov_beacon_height // tile_side

        # Make the number of tiles even, so the corners of four tiles always
        # are in the coordinates' origin.
        if fov_width_in_tiles_original % 2 != 0:
            fov_width_in_tiles = fov_width_in_tiles_original - 1
        else:
            fov_width_in_tiles = fov_width_in_tiles_original

        if fov_height_in_tiles_original % 2 != 0:
            fov_height_in_tiles = fov_height_in_tiles_original - 1
        else:
            fov_height_in_tiles = fov_height_in_tiles_original

        # If any of the dimensions of the FOV in tiles is 0, set both to 0.
        if fov_width_in_tiles <= 0 or fov_height_in_tiles <= 0:
            log.debug("- one of FOV's dimensions is 0: set both to 0")
            fov_width_in_tiles = 0
            fov_height_in_tiles = 0

        # Calculate the final dimensions of the FOV, again in metric units.
        fov_width = fov_width_in_tiles * tile_side
        fov_height = fov_height_in_tiles * tile_side

        # Add FOVs

        VLIPSSimulation.add_fov(
            context=context,
            name=CAMERA_FOV_FULL_NAME,
            beacon_distance=beacon_distance,
            show_fov=show_fov,
            room_properties=room_properties,
            width=fov_full_width,
            height=fov_full_height,
            color=CAMERA_FOV_FULL_COLOR,
            collection=fov_collection)

        VLIPSSimulation.add_fov(
            context=context,
            name=CAMERA_FOV_BEACON_NAME,
            beacon_distance=beacon_distance,
            show_fov=show_fov,
            room_properties=room_properties,
            width=fov_beacon_width,
            height=fov_beacon_height,
            color=CAMERA_FOV_BEACON_COLOR,
            collection=fov_collection)

        VLIPSSimulation.add_fov(
            context=context,
            name=CAMERA_FOV_TILES_NAME,
            beacon_distance=beacon_distance,
            show_fov=show_fov,
            room_properties=room_properties,
            width=fov_width_in_tiles_original * tile_side,
            height=fov_height_in_tiles_original * tile_side,
            color=CAMERA_FOV_TILES_COLOR,
            collection=fov_collection)

        VLIPSSimulation.add_fov(
            context=context,
            name=CAMERA_FOV_EVEN_TILES_NAME,
            beacon_distance=beacon_distance,
            show_fov=show_fov,
            room_properties=room_properties,
            width=fov_width,
            height=fov_height,
            color=CAMERA_FOV_EVEN_TILES_COLOR,
            collection=fov_collection,
            show_wire=True,
            x_subdivisions=fov_width_in_tiles,
            y_subdivisions=fov_height_in_tiles)

    @staticmethod
    def add_fov(
            context,
            name,
            beacon_distance,
            show_fov,
            room_properties,
            width,
            height,
            color,
            collection,
            show_wire=False,
            x_subdivisions=0,
            y_subdivisions=0
    ):
        """
        Add camera's Field of Vision (FOV) to the viewport.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param name: name given to the FOV, so it can be later accessed.
        :param beacon_distance: distance between the beacon and the camera, in
        millimeters.
        :param show_fov: draw camera's field of vision just behind the camera.
        :param room_properties: properties of the room.
        :param width: width of the FOV, in millimeters.
        :param height: height of the FOV, in millimeters.
        :param color: color of the FOV, with red, green, blue, and alpha
        components.
        :param collection: reference to the collection where the FOV should be
        included.
        :param show_wire: if `False`, a plane will be used to represent the FOV;
        if `True`, a grid.
        :param x_subdivisions: FOV's width in tiles, only used when `show_wire`
        is True.
        :param y_subdivisions: FOV's height in tiles, only used when
        `show_wire` is True.
        """

        log.info("Add camera's Field of Vision (FOV)")
        log.debug(f"VLIPSSimulation.add_fov("
                  f"context={context}, "
                  f"name={name}, "
                  f"beacon_distance={beacon_distance}, "
                  f"show_fov={show_fov}, "
                  f"room_properties={room_properties}, "
                  f"width={width}, "
                  f"height={height}, "
                  f"color={color}, "
                  f"collection={collection}, "
                  f"show_wire={show_wire}, "
                  f"x_subdivisions={x_subdivisions}, "
                  f"y_subdivisions={y_subdivisions})")

        previous_hide_state = True
        if name in context.scene.objects:
            log.debug(f"- FOV named \"{name}\" already exists: destroy it")

            for ob in context.selected_objects:
                ob.select_set(False)

            previous_hide_state = context.scene.objects[name].hide_get()
            context.scene.objects[name].hide_set(False)
            context.scene.objects[name].select_set(True)
            bpy.ops.object.delete()

        if show_wire:
            bpy.ops.mesh.primitive_grid_add(
                x_subdivisions=x_subdivisions,
                y_subdivisions=y_subdivisions)
        else:
            bpy.ops.mesh.primitive_plane_add(location=[0, 0, 0])

        fov = context.active_object
        fov.hide_set(True)

        if show_wire:
            fov.show_wire = True

        fov.name = name
        fov.location = [
            DEFAULT_CAMERA_FOV_LOCATION[0],
            DEFAULT_CAMERA_FOV_LOCATION[1],
            room_properties.height - beacon_distance
        ]
        fov.rotation_euler = [
            math.radians(DEFAULT_CAMERA_FOV_ROTATION[0]),
            math.radians(DEFAULT_CAMERA_FOV_ROTATION[1]),
            math.radians(DEFAULT_CAMERA_FOV_ROTATION[2])
        ]
        fov.dimensions = (width, height, 0)

        material = bpy.data.materials.new(name)
        material.diffuse_color = color
        fov.active_material = material

        collection.objects.link(fov)

        context.collection.objects.unlink(fov)

        if name == CAMERA_FOV_EVEN_TILES_NAME:
            if show_fov:
                fov.hide_set(False)
            else:
                fov.hide_set(True)
        else:
            fov.hide_set(previous_hide_state)

    @staticmethod
    def setup_texts(
            context,
            font_size,
            camera_beacon_distance=None,
            camera_x=None,
            camera_y=None,
            camera_rotation_x_angle=None,
            camera_rotation_z_angle=None
    ):
        """
        Show in the floor of the room a series of lines with the current
        distance and angle between the camera and the beacon.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        :param font_size: size in millimeters of the font used to display the texts.
        :param camera_beacon_distance: distance from the camera to the beacon,
        in millimeters.
        :param camera_x: x coordinate of the position of the camera.
        :param camera_y: y coordinate of the position of the camera.
        :param camera_rotation_x_angle: rotation around camera's X axis, in degrees.
        :param camera_rotation_z_angle: rotation around camera's Z axis, in degrees.
        """

        log.info("Set the texts up")
        log.debug(f"VLIPSSimulation.setup_texts("
                  f"context={context}, "
                  f"font_size={font_size}, "
                  f"camera_beacon_distance={camera_beacon_distance}, "
                  f"camera_x={camera_x}, "
                  f"camera_y={camera_y}, "
                  f"camera_rotation_x_angle={camera_rotation_x_angle}, "
                  f"camera_rotation_z_angle={camera_rotation_z_angle})")

        # Add the collection that will contain the different steps needed to
        # calculate the FOV
        if TEXT_COLLECTION_NAME not in bpy.data.collections:
            text_collection = bpy.data.collections.new(TEXT_COLLECTION_NAME)
            context.scene.collection.children.link(text_collection)
        else:
            text_collection = bpy.data.collections[TEXT_COLLECTION_NAME]

        if camera_beacon_distance is None and \
                camera_x is None and \
                camera_y is None:
            log.debug("- camera_beacon_distance, camera_x, camera_y not provided")
            log.debug("- load from camera properties")

            camera_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_OPERATOR_NAME)

            camera = context.scene.objects[camera_properties.name]
            camera_x = camera.location[0]
            camera_y = camera.location[1]

            camera_beacon_distance = camera_properties.beacon_distance
            camera_rotation_x_angle = camera_properties.rotation_x_angle
            camera_rotation_z_angle = camera_properties.rotation_z_angle

            log.debug(f"- camera_x={camera_x}")
            log.debug(f"- camera_y={camera_y}")
            log.debug(f"- camera_beacon_distance={camera_beacon_distance}")
            log.debug(f"- camera_rotation_x_angle={camera_rotation_x_angle}")
            log.debug(f"- camera_rotation_z_angle={camera_rotation_z_angle}")

        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
        tile_side = scene_properties.tile_side

        if camera_x != 0:
            grid_x = int(camera_x / tile_side)
        else:
            grid_x = 0

        if camera_y != 0:
            grid_y = int(camera_y / tile_side)
        else:
            grid_y = 0

        texts = {
            TEXT_HEIGHT_KEY:
                f"{TEXT_HEIGHT_KEY}: {(room_properties.height - camera_beacon_distance) / 1000:.2f} m",
            TEXT_X_KEY:
                f"{TEXT_X_KEY}: {camera_x / 1000:.3f} m",
            TEXT_Y_KEY:
                f"{TEXT_Y_KEY}: {camera_y / 1000:.3f} m",
            TEXT_GRID_KEY:
                f"{TEXT_GRID_KEY}: {grid_x}, {grid_y}",
            TEXT_ROTATION_KEY:
                f"{TEXT_ROTATION_KEY}: ",
            TEXT_ROTATION_X_KEY:
                f"- {TEXT_ROTATION_X}: {camera_rotation_x_angle:.2f}º",
            TEXT_ROTATION_Z_KEY:
                f"- {TEXT_ROTATION_Z}: {camera_rotation_z_angle:.2f}º"
        }

        log.debug(f"- texts={texts}")

        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)

        for index, (key, value) in enumerate(texts.items()):
            # Create the font object if it doesn't exist
            if key not in context.scene.objects:
                log.debug(f"- text {key} doesn't exist: create")

                curve = bpy.data.curves.new(type="FONT", name=key)
                font = bpy.data.objects.new("Font Object", curve)
                font.name = key
                text_collection.objects.link(font)
            else:
                log.debug(f"- text {key} already exists")

                font = context.scene.objects[key]

            # Set object text, size, location, and rotation
            font.data.body = value
            font.data.size = font_size

            font.location = (
                -(room_properties.width / 2) + font_size,
                (room_properties.depth / 2),
                font_size * (len(texts) - index))
            font.rotation_euler = (math.radians(90), 0, 0)

            log.debug(f"- font.data.body: {font.data.body}")
            log.debug(f"- font.data.size: {font.data.size}")
            log.debug(f"- font.location: {font.location}")
            log.debug(f"- font.rotation_euler: {font.rotation_euler}")

    @staticmethod
    def create_scene(
            context
    ):
        """
        Set the scene up and then create a simulation containing a room, a
        beacon, and a camera.

        :param context: Blender's current context containing the scene where
        the simulation must reside.
        """

        log.info("Set the camera up")
        log.debug(f"VLIPSSimulation.setup_camera("
                  f"context={context})")

        # Set the scene up
        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)

        VLIPSSimulation.setup_scene(
            context,
            tile_side=scene_properties.tile_side,
            floor_side_tiles=scene_properties.floor_side_tiles
        )

        # Set the room up
        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)

        VLIPSSimulation.setup_room(
            context=context,
            name=room_properties.name,
            depth=room_properties.depth,
            width=room_properties.width,
            height=room_properties.height,
            thickness=room_properties.thickness)

        # Set the beacon up
        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)

        VLIPSSimulation.setup_beacon(
            context=context,
            name=beacon_properties.name,
            width=beacon_properties.width,
            height=beacon_properties.height)

        # Set the camera up
        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)

        VLIPSSimulation.setup_camera(
            context=context,
            name=camera_properties.name,
            make=camera_properties.make,
            model=camera_properties.model,
            orientation=camera_properties.orientation,
            facing=camera_properties.facing,
            resolution_width=camera_properties.resolution_width,
            resolution_height=camera_properties.resolution_height,
            focal_length=camera_properties.focal_length,
            pixel_size=camera_properties.pixel_size,
            beacon_distance=camera_properties.beacon_distance,
            rotation_x_angle=camera_properties.rotation_x_angle,
            rotation_z_angle=camera_properties.rotation_z_angle,
            show_fov=camera_properties.show_fov)

        # Show texts on the floor
        texts_properties = context.window_manager.operator_properties_last(
            SETUP_TEXTS_OPERATOR_NAME)

        VLIPSSimulation.setup_texts(
            context=context,
            font_size=texts_properties.font_size)

        # Let the view port show the whole scene
        VLIPSSimulation.zoom_to_scene()

    @staticmethod
    def render_scene(
            context,
            filepath
    ):
        """
        Render the scene in the context, save it as an image in the path
        provided. All the details needed to recreate the scene are stored as
        EXIF data in the image.

        :param context: Blender's current context containing the scene to be
        rendered.
        :param filepath: path to the file where the rendered scene should be
        saved.
        """

        log.info("Render scene")
        log.debug(f"VLIPSSimulation.render_scene("
                  f"context={context}, "
                  f"filepath={filepath})")

        # Load all the properties needed to both render the image and recreate
        # the scene later if needed
        scene_properties = context.window_manager.operator_properties_last(
            SETUP_SCENE_OPERATOR_NAME)
        room_properties = context.window_manager.operator_properties_last(
            SETUP_ROOM_OPERATOR_NAME)
        beacon_properties = context.window_manager.operator_properties_last(
            SETUP_BEACON_OPERATOR_NAME)
        beacon = context.scene.objects[beacon_properties.name]
        camera_properties = context.window_manager.operator_properties_last(
            SETUP_CAMERA_OPERATOR_NAME)
        camera = context.scene.objects[camera_properties.name]
        camera_rotation = (
            math.degrees(camera.rotation_euler[0]),
            math.degrees(camera.rotation_euler[1]),
            math.degrees(camera.rotation_euler[2])
        )

        # Render and save as image. First, hide the room, so it doesn't show in
        # the resulting image
        room = context.scene.objects[room_properties.name]
        room.hide_render = True
        context.scene.render.image_settings.file_format = "JPEG"
        context.scene.render.image_settings.quality = 100
        context.scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)
        room.hide_render = False

        # Create helper instances of objects that ease the storage of the data
        # as EXIF in the image

        scene = Scene(
            tile_side=round(scene_properties.tile_side),
            floor_sides_tiles=scene_properties.floor_side_tiles)

        beacon = Beacon(
            name=beacon_properties.name,
            dimensions=(round(beacon_properties.width), round(beacon_properties.height), 0),
            location=(round(beacon.location.x), round(beacon.location.y), round(beacon.location.z)),
            rotation=DEFAULT_BEACON_ROTATION)

        camera_location_x = round(camera.location.x)
        camera_location_y = round(camera.location.y)
        camera_location_z = round(camera.location.z)
        tile_side = scene_properties.tile_side
        grid_location_x = round(camera.location.x / tile_side)
        grid_location_y = round(camera.location.y / tile_side)
        camera_rotation_x_angle = camera_properties.rotation_x_angle
        camera_rotation_z_angle = camera_properties.rotation_z_angle
        camera = Camera(
            name=camera_properties.name,
            facing=Camera.Facing.from_str(camera_properties.facing),
            resolution_width=camera_properties.resolution_width,
            resolution_height=camera_properties.resolution_height,
            focal_length=camera_properties.focal_length,
            pixel_size=camera_properties.pixel_size,
            make=camera_properties.make,
            model=camera_properties.model,
            software=f"{ADDON_SHORT_NAME} ({ADDON_VERSION})",
            location=(camera_location_x, camera_location_y, camera_location_z),
            rotation=camera_rotation,
            grid_location=(grid_location_x, grid_location_y),
            rotation_x_angle=camera_rotation_x_angle,
            rotation_z_angle=camera_rotation_z_angle)

        # Store the data as EXIF in the image
        ExifWriter().save_exif_data(
            filepath=filepath,
            scene=scene,
            beacon=beacon,
            camera=camera)

    @staticmethod
    def get_camera_movement_steps(
            context: bpy.types.Context,
            camera_movement: CameraMovement) -> [float]:
        """
        Get the list of steps of the camera movement.

        :param context: Blender's current context containing the scene to be
        rendered.
        :param camera_movement: type of movement the camera will describe.

        :return: list of steps the camera movement will describe.
        :rtype: [float]
        """

        log.info("Get camera movement steps")
        log.debug(f"VLIPSSimulation.get_camera_movement_steps("
                  f"context={context}, "
                  f"camera_movement={camera_movement})")

        if camera_movement == CameraMovement.BEACON_DISTANCE:
            camera_movement_beacon_distance_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_DISTANCE_OPERATOR_NAME)
            distance_start = camera_movement_beacon_distance_properties.camera_beacon_distance_start
            distance_end = camera_movement_beacon_distance_properties.camera_beacon_distance_end
            distance_step = camera_movement_beacon_distance_properties.camera_beacon_distance_step
            camera_movement_steps = arange(distance_start, distance_end + distance_step, distance_step)
        elif camera_movement == CameraMovement.ROTATION_X_ANGLE:
            camera_movement_rotation_x_angle_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_ROTATION_X_ANGLE_OPERATOR_NAME)
            angle_start = camera_movement_rotation_x_angle_properties.camera_rotation_x_angle_start
            angle_end = camera_movement_rotation_x_angle_properties.camera_rotation_x_angle_end
            angle_step = camera_movement_rotation_x_angle_properties.camera_rotation_x_angle_step
            camera_movement_steps = arange(angle_start, angle_end + angle_step, angle_step)
        elif camera_movement == CameraMovement.ROTATION_Z_ANGLE:
            camera_movement_rotation_z_angle_properties = context.window_manager.operator_properties_last(
                SETUP_CAMERA_MOVEMENT_ROTATION_Z_ANGLE_OPERATOR_NAME)
            angle_start = camera_movement_rotation_z_angle_properties.camera_rotation_z_angle_start
            angle_end = camera_movement_rotation_z_angle_properties.camera_rotation_z_angle_end
            angle_step = camera_movement_rotation_z_angle_properties.camera_rotation_z_angle_step
            camera_movement_steps = arange(angle_start, angle_end + angle_step, angle_step)
        else:
            camera_movement_steps = []

        return camera_movement_steps

    @staticmethod
    def get_camera_movement_steps_digits(camera_movement_steps: list) -> int:
        """
        Get the number of digits the list of camera movement steps has.

        :param camera_movement_steps: number of items in the list of movements.

        :return: number of digits in the number items in the list of movements.
        :rtype: int
        """

        log.info("Get file path")
        log.debug(f"VLIPSSimulation.get_camera_movement_steps_digits("
                  f"camera_movement_steps={len(camera_movement_steps)} items)")

        max_index = len(camera_movement_steps) - 1
        max_index_as_string = str(max_index)

        return len(max_index_as_string)

    @staticmethod
    def get_camera_movement_file_path(
            index: int,
            max_index_digits: int,
            file_prefix: str,
            output_path: str,
            fov_scan_enabled: bool,
            beacon_distance_enabled: bool,
            rotation_x_angle_enabled: bool,
            rotation_z_angle_enabled: bool,
            camera_movement_step: dict
    ) -> str:
        """
        Compose the file path for the output render in a camera movement
        step.

        :param index: current step of the camera movement sequence.
        :param max_index_digits: number of digits of the upper limit of the
        sequence.
        :param file_prefix: name of the file used for the renders.
        :param output_path: folder where the renders will be saved to.
        :param fov_scan_enabled: True if the camera is going to go through
        the entire FOV, False otherwise.
        :param beacon_distance_enabled: True if the distance between the camera
        and the beacon is going to go change, False otherwise.
        :param rotation_x_angle_enabled: True if rotation of the camera around the X
        axis is going to go change, False otherwise.
        :param rotation_z_angle_enabled: True if rotation of the camera around the Z
        axis is going to go change, False otherwise.
        :param camera_movement_step: dictionary describing the current step of
        the camera movement.

        :return: full file path, file name included, where the render will be
        saved to.
        """

        log.info("Get file path")
        log.debug(f"VLIPSSimulation.get_camera_movement_file_path("
                  f"index={index}, "
                  f"max_index_digits={max_index_digits}, "
                  f"file_prefix={file_prefix}, "
                  f"output_path={output_path}, "
                  f"fov_scan_enabled={fov_scan_enabled}, "
                  f"beacon_distance_enabled={beacon_distance_enabled}, "
                  f"rotation_x_angle_enabled={rotation_x_angle_enabled}, "
                  f"rotation_z_angle_enabled={rotation_z_angle_enabled}, "
                  f"camera_movement_step={camera_movement_step})")

        file_suffix = str(index).zfill(max_index_digits)
        if file_prefix == "":
            file_name = f"{file_suffix}"
        else:
            file_name = f"{file_prefix}_{file_suffix}"

        if fov_scan_enabled:
            grid_x, grid_y = camera_movement_step[CAMERA_MOVEMENT_FOV_GRID_COORDINATES]
            file_name = f"{file_name}_{grid_x:+}_{grid_y:+}"

        file_name = f"{file_name}.jpg"

        if beacon_distance_enabled:
            beacon_distance = camera_movement_step[CAMERA_MOVEMENT_BEACON_DISTANCE]
            output_path = os.path.join(output_path, f"distance_{int(beacon_distance):+}")

        if rotation_x_angle_enabled:
            rotation_x = camera_movement_step[CAMERA_MOVEMENT_ROTATION_X_ANGLE]
            output_path = os.path.join(output_path, f"rotation_x_{int(rotation_x):+}")

        if rotation_z_angle_enabled:
            rotation_z = camera_movement_step[CAMERA_MOVEMENT_ROTATION_Z_ANGLE]
            output_path = os.path.join(output_path, f"rotation_z_{int(rotation_z):+}")

        return os.path.join(output_path, file_name)
