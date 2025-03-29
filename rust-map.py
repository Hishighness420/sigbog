import obspython as S
import time

class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_settings = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id
        self.load()

    def load(self):
        self.hotkey_saved_key = S.obs_data_get_array(self.obs_settings, str(self._id))
        S.obs_data_array_release(self.hotkey_saved_key)
        self.hotkey_id = S.obs_hotkey_register_frontend(str(self._id), str(self._id), self.callback)
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)
        self.save()

    def save(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(self.obs_settings, str(self._id), self.hotkey_saved_key)
        S.obs_data_array_release(self.hotkey_saved_key)

def mapkey_callback(pressed):
    # When the hotkey is pressed, toggle the cover in both scenes.
    if pressed:
        toggle(True)
    else:  
        time.sleep(data.delay)
        toggle(False)

def toggle(boolean):
    # Toggle the image visibility in the fullscreen scene.
    if data.fullscreen_scene != "":
        fs_source = S.obs_get_source_by_name(data.fullscreen_scene)
        if fs_source is not None:
            fs_scene = S.obs_scene_from_source(fs_source)
            fs_scene_item = S.obs_scene_find_source(fs_scene, data.image)
            if fs_scene_item is not None:
                S.obs_sceneitem_set_visible(fs_scene_item, boolean)
            S.obs_source_release(fs_source)
    
    # Toggle the image visibility in the vertical scene.
    if data.vertical_scene != "":
        vs_source = S.obs_get_source_by_name(data.vertical_scene)
        if vs_source is not None:
            vs_scene = S.obs_scene_from_source(vs_source)
            vs_scene_item = S.obs_scene_find_source(vs_scene, data.image)
            if vs_scene_item is not None:
                S.obs_sceneitem_set_visible(vs_scene_item, boolean)
            S.obs_source_release(vs_source)

def script_description():
    return ("Adds a hotkey for your Rust game map cover that affects two scenes: one for fullscreen "
            "and one for vertical (mobile) streaming.\n\n"
            "Tutorial:\n"
            "  rust_map_source_name:  The name of the image source that acts as your map cover.\n"
            "  rust_fullscreen_scene_name: The name of your fullscreen scene.\n"
            "  rust_vertical_scene_name: The name of your vertical scene (for mobile).\n"
            "  rust_map_delay:        Delay (in seconds) before removing the cover after releasing the hotkey.\n\n"
            "After setting these, assign the 'RustMap Push to Hide' hotkey in OBS.")

def script_properties():
    properties = S.obs_properties_create()
    S.obs_properties_add_text(properties, "rust_map_source_name", "rust_map_source_name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_fullscreen_scene_name", "Fullscreen Scene Name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_text(properties, "rust_vertical_scene_name", "Vertical Scene Name:", S.OBS_TEXT_DEFAULT)
    S.obs_properties_add_float_slider(properties, "rust_map_delay", "Reveal Delay (seconds):", 0, 1, 0.01)
    return properties

def script_update(settings):
    data.image = S.obs_data_get_string(settings, "rust_map_source_name")
    data.fullscreen_scene = S.obs_data_get_string(settings, "rust_fullscreen_scene_name")
    data.vertical_scene = S.obs_data_get_string(settings, "rust_vertical_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_load(settings):
    data.hotkey = Hotkey(mapkey_callback, settings, "RustMap Push to Hide")
    data.image = S.obs_data_get_string(settings, "rust_map_source_name")
    data.fullscreen_scene = S.obs_data_get_string(settings, "rust_fullscreen_scene_name")
    data.vertical_scene = S.obs_data_get_string(settings, "rust_vertical_scene_name")
    data.delay = S.obs_data_get_double(settings, "rust_map_delay")

def script_save(settings):
    data.hotkey.save()

class Data:
    image = ""
    fullscreen_scene = ""
    vertical_scene = ""
    delay = 0.0
    hotkey = None

data = Data()
