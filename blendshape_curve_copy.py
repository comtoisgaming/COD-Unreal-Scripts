import bpy
import math
import clipboard as c

class UE4BlendshapeCopy:
    def __init__(self):
        self.counter = 0

    def get_blendshapes(self):
        self.main_string = ""
        self.init()
        self.generate_values()
        self.close()

    def init(self):
        self.main_string += (
            "Begin Object Class=/Script/CurveEditor.CurveEditorCopyBuffer "
            "Name=\"CurveEditorCopyBuffer_0\" ExportPath=/Script/CurveEditor.CurveEditorCopyBuffer'\""
            "/Engine/Transient.CurveEditorCopyBuffer_0\"'\n"
        )
        self.main_string += (
            "Begin Object Class=/Script/CurveEditor.CurveEditorCopyableCurveKeys "
            "Name=\"CurveEditorCopyableCurveKeys_0\" ExportPath=/Script/CurveEditor.CurveEditorCopyableCurveKeys'\""
            "/Engine/Transient.CurveEditorCopyBuffer_0:CurveEditorCopyableCurveKeys_0\"'\n"
        )
        print("Begin Object")

    def generate_values(self, key_title=""):
        obj = bpy.context.active_object
        main_data = {}
        mesh_data = obj.data
        shape_keys = mesh_data.shape_keys.key_blocks
        key_title_list = shape_keys.keys()
        scene = bpy.context.scene
        new_shape_data = mesh_data.shape_keys.animation_data.action

        if len(bpy.context.selected_objects) == 0:
            raise TypeError("An object has to be selected to operate.")

        if obj.type != 'MESH':
            raise TypeError("A mesh needs to be actively selected to view shape keys.")

        if key_title == "" and len(shape_keys) == 0:
            raise TypeError("You need to specify a shape key or select one in Properties.")

        shape_key_title = key_title_list[obj.active_shape_key_index]

        if key_title != "":
            shape_key_title = key_title

        for fc in new_shape_data.fcurves:
            split_name = fc.data_path.split("\"")
            name = split_name[1]

            position_counter = 0
            key_positions = ""
            key_attributes = ""

            if name == shape_key_title:
                print("Data: ", name)

                for keyframe in range(len(fc.keyframe_points)):
                    current_frame = fc.keyframe_points[keyframe]

                    if keyframe > 0:
                        last_frame = fc.keyframe_points[keyframe - 1]

                        if current_frame.co.y != last_frame.co.y:
                            key_positions += (
                                "\"KeyPositions\"(" + str(position_counter) + ")=(InputValue=" +
                                str(current_frame.co.x / scene.render.fps) + "," +
                                "OutputValue=" + str(current_frame.co.y) + ")\n"
                            )

                            if (keyframe + 1) == len(fc.keyframe_points):
                                key_attributes += (
                                    "\"KeyAttributes\"(" + str(position_counter) + ")=(bHasInterpMode=True,"
                                    "LeaveTangent=-0.000000,TangentMode=(INVALID),ArriveTangentWeight=-0.000000,"
                                    "LeaveTangentWeight=0.000000)\n"
                                )
                            else:
                                key_attributes += (
                                    "\"KeyAttributes\"(" + str(position_counter) + ")=(bHasInterpMode=True,"
                                    "ArriveTangent=0.000000,LeaveTangent=0.000000,ArriveTangentWeight=0.000000,"
                                    "LeaveTangentWeight=0.000000)\n"
                                )

                            print(str(current_frame.co.x / scene.render.fps), current_frame.co.y)
                            position_counter += 1

                    elif keyframe == 0 or keyframe == len(fc.keyframe_points):
                        key_positions += (
                            "\"KeyPositions\"(" + str(position_counter) + ")=(InputValue=" +
                            str(current_frame.co.x / scene.render.fps) + "," +
                            "OutputValue=" + str(current_frame.co.y) + ")\n"
                        )

                        if (keyframe + 1) == len(fc.keyframe_points):
                            key_attributes += (
                                "\"KeyAttributes\"(" + str(position_counter) + ")=(bHasInterpMode=True,"
                                "LeaveTangent=-0.000000,TangentMode=(INVALID),ArriveTangentWeight=-0.000000,"
                                "LeaveTangentWeight=0.000000)\n"
                            )
                        else:
                            key_attributes += (
                                "\"KeyAttributes\"(" + str(position_counter) + ")=(bHasInterpMode=True,"
                                "ArriveTangent=0.000000,LeaveTangent=0.000000,ArriveTangentWeight=0.000000,"
                                "LeaveTangentWeight=0.000000)\n"
                            )

                        print(str(current_frame.co.x / scene.render.fps), current_frame.co.y)
                        position_counter += 1

            self.main_string += key_positions
            self.main_string += key_attributes

        self.main_string += "\"ShortDisplayName\"=" + shape_key_title + "\"\n"
        self.main_string += "\"LongDisplayName\"=" + shape_key_title + "\"\n"

    def close(self):
        self.main_string += "End Object\n"
        self.main_string += "\"Curves\"(0)=/Script/CurveEditor.CurveEditorCopyableCurveKeys'\"CurveEditorCopyableCurveKeys_0\"'\n"
        self.main_string += "\"bAbsolutePosition\"=True\n"
        self.main_string += "End Object\n"
        print("End Object")

if __name__ == "__main__":
    print("\n\n\n\n")
    copy = UE4BlendshapeCopy()
    copy.get_blendshapes()
    c.copy(copy.main_string)
