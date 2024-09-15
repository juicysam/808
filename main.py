import kivy
import simplepyble
from audio_list import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition,
                                    SlideTransition, CardTransition, SwapTransition,
                                    FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)

service_uuid = '19b10000-e8f2-537e-4f6c-d104768a1214'
audio_uuid = 'adef0863-849a-40fc-8f1c-dc7bb2dbb349'
folder_uuid = '4a1e0ed2-b9f6-43c9-ba88-db8ad5012065'
audioCommand_uuid = '4066ac78-4c68-4cf8-b2fe-aa286a44f799'
lights_uuid = '48562b92-6e32-4aa2-9343-2c4ae632898e'
eyes_uuid = 'b9959e9b-f8cb-4012-98ec-c54ba2287081'

#Window.size = (1344,2992)

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.connected = False

    def toggle_connect(self):
        if self.connected:
            disconnect()
            self.connected = False
        else:
            connect()
            self.connected = True


class PlaylistMenu(Screen):
    def write(self, value):
        write_audioCommand(value)

class HiFiRushPlaylist(Screen):
    def write(self, value):
        write_audioCommand(value)


class PsychPlaylist(Screen):
    def write(self, value):
        write_audioCommand(value)


class MemePlaylist(Screen):
    def write(self, value):
        write_audioCommand(value)


class AudioList(BoxLayout):
    label_text = StringProperty('default')
    button_text = StringProperty('default')
    folder_index = NumericProperty(0)
    file_index = NumericProperty(0)

    def write(self, folder, song):
        print(self.file_index)
        write_specificSong(folder, song)


class LightsMenu(Screen):
    pass


class EyesMenu(Screen):
    def write(self, folder, song):
        write_specificSong(folder, song)


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.transition = NoTransition()


class MainApp(App):
    def build(self):
        Window.clearcolor = (3 / 255, 2 / 255, 41 / 255)
        return MyScreenManager()


def connect():
    global peripheral
    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")

    choice = 0
    for i, adapter in enumerate(adapters):
        if adapter.address == '8a:88:4b:80:43:41':
            choice = i
            break
        elif adapter.address == '5C:33:7B:EB:B2:BA':
            choice = i
            break

    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))

    # Scan for 5 seconds
    adapter.scan_for(3000)
    peripherals = adapter.scan_get_results()

    # Query the user to pick a peripheral
    print("Please select a peripheral:")
    for i, address in enumerate(peripherals):
        if address.address() == 'f4:12:fa:65:a0:1d':
            peripheral = peripherals[i]
            break

    print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
    peripheral.connect()


def disconnect():
    peripheral.disconnect()
    print('disconnected')


def write_audio(value):
    try:
        # Write the content to the characteristic
        # Note: `write_request` required the payload to be presented as a bytes object.
        peripheral.write_request(service_uuid, audio_uuid, str.encode(value))
    except:
        print('808 is not connected')


def write_folder(value):
    try:
        # Write the content to the characteristic
        # Note: `write_request` required the payload to be presented as a bytes object.
        peripheral.write_request(service_uuid, folder_uuid, str.encode(chr(value)))
    except:
        print('808 is not connected')


def write_audioCommand(value):
    try:
        # Write the content to the characteristic
        # Note: `write_request` required the payload to be presented as a bytes object.
        peripheral.write_request(service_uuid, audioCommand_uuid, str.encode(chr(value)))
    except:
        print('808 is not connected')


def write_specificSong(folder, song):
    write_folder(folder)
    write_audio(chr(song))
    write_audioCommand(5)


def write_lights(value):
    try:
        # Write the content to the characteristic
        # Note: `write_request` required the payload to be presented as a bytes object.
        peripheral.write_request(service_uuid, lights_uuid, str.encode(value))
    except:
        print('808 is not connected')


def write_eyes(value):
    try:
        # Write the content to the characteristic
        # Note: `write_request` required the payload to be presented as a bytes object.
        peripheral.write_request(service_uuid, eyes_uuid, str.encode(value))
    except:
        print('808 is not connected')

if __name__ == "__main__":
    MainApp().run()
