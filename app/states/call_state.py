import reflex as rx
from typing import TypedDict, Literal, Union
from app.states.lang_state import TEXT_BN, TEXT_EN, TextContent
import asyncio
import logging


class Message(TypedDict):
    user: str
    text: str


rooms: dict[str, list[str]] = {}
signals: dict[str, dict[str, Union[str, bool]]] = {}


class CallState(rx.State):
    page_state: Literal["home", "lobby", "call"] = "home"
    room_name: str = ""
    theme: str = rx.LocalStorage("dark", name="motioncall_theme")
    language: str = rx.LocalStorage("en", name="motioncall_lang")
    reduced_motion: bool = rx.LocalStorage(False, name="motioncall_reduced_motion")
    is_camera_on: bool = True
    camera_permission: bool | None = None
    mic_permission: bool | None = None
    is_mic_on: bool = True
    is_sharing_screen: bool = False
    is_recording: bool = False
    is_recording_consent_shown: bool = False
    is_chat_open: bool = False
    is_settings_open: bool = False
    is_menu_open: bool = False
    messages: list[Message] = []
    chat_input: str = ""
    connection_status: str = "connecting"
    peer_recording_status: bool = False

    @rx.var
    def text(self) -> TextContent:
        return TEXT_BN if self.language == "bn" else TEXT_EN

    @rx.var
    def motion_class(self) -> str:
        return (
            "transition-none" if self.reduced_motion else "transition-all duration-150"
        )

    @rx.event
    def join_lobby(self, form_data: dict[str, str]):
        self.room_name = form_data.get("room_name", "").strip()
        if self.room_name:
            token = self.router.session.client_token
            if (
                token in rooms.get(self.room_name, [])
                or len(rooms.get(self.room_name, [])) >= 2
            ):
                return rx.toast.error(
                    f"Room '{self.room_name}' is full or you are already in it."
                )
            self.page_state = "lobby"
            return
        yield rx.toast.error(self.text["enter_room"])

    @rx.event
    def set_camera_permission(self, status: bool):
        self.camera_permission = status

    @rx.event
    def set_mic_permission(self, status: bool):
        self.mic_permission = status

    @rx.event
    async def check_permissions_and_join(self):
        return rx.call_script("request_media_permissions()")

    @rx.event
    def join_call(self):
        if self.camera_permission is False or self.mic_permission is False:
            return rx.toast.error("Camera and Mic permissions are required to join.")
        self.page_state = "call"

    @rx.event
    def on_call_load(self):
        token = self.router.session.client_token
        if not token or not self.room_name:
            self.page_state = "home"
            return rx.toast.error("Room details not found. Returning to home.")
        if self.room_name not in rooms:
            rooms[self.room_name] = []
        if token not in rooms[self.room_name]:
            rooms[self.room_name].append(token)
        yield rx.call_script(f'init_peer_connection("{token}")')
        yield CallState.poll_signals

    @rx.event(background=True)
    async def poll_signals(self):
        token = self.router.session.client_token
        while True:
            async with self:
                if self.page_state != "call":
                    rooms.pop(self.room_name, None)
                    signals.pop(token, None)
                    return
                if token in signals:
                    signal = signals.pop(token)
                    yield rx.call_script(f"handle_signal({repr(signal)})")
            await asyncio.sleep(0.1)

    @rx.event
    def send_signal(self, signal: dict):
        my_token = self.router.session.client_token
        if self.room_name not in rooms:
            return
        other_peers = [p for p in rooms[self.room_name] if p != my_token]
        if other_peers:
            other_token = other_peers[0]
            signals[other_token] = signal

    @rx.event
    def user_joined(self):
        token = self.router.session.client_token
        if len(rooms.get(self.room_name, [])) > 1:
            self.connection_status = "connecting"
            yield rx.call_script("create_offer()")
        else:
            self.connection_status = "connecting"

    @rx.event
    def leave_call(self):
        token = self.router.session.client_token
        if self.room_name in rooms and token in rooms[self.room_name]:
            rooms[self.room_name].remove(token)
            if not rooms[self.room_name]:
                del rooms[self.room_name]
        self.page_state = "home"
        yield rx.call_script("hangup()")
        yield CallState.send_signal({"type": "peer_left"})
        self.is_sharing_screen = False
        self.is_recording = False
        self.messages = []

    @rx.event
    def set_connection_status(self, status: str):
        self.connection_status = status

    @rx.event
    def toggle_camera(self):
        self.is_camera_on = not self.is_camera_on
        return rx.call_script(
            f"toggle_track('video', {str(self.is_camera_on).lower()})"
        )

    @rx.event
    def toggle_mic(self):
        self.is_mic_on = not self.is_mic_on
        return rx.call_script(f"toggle_track('audio', {str(self.is_mic_on).lower()})")

    @rx.event
    def toggle_screen_share(self):
        self.is_sharing_screen = not self.is_sharing_screen
        return rx.call_script(
            f"toggle_screen_share({str(self.is_sharing_screen).lower()})"
        )

    @rx.event
    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording_consent_shown = True
        else:
            self.is_recording = False
            yield rx.call_script("stop_recording()")
            yield CallState.update_peer_recording_status(False)

    def confirm_recording(self):
        self.is_recording = True
        self.is_recording_consent_shown = False
        yield rx.call_script("start_recording()")
        yield CallState.update_peer_recording_status(True)

    def cancel_recording(self):
        self.is_recording_consent_shown = False

    @rx.event
    def update_peer_recording_status(self, status: bool):
        return rx.call_script(
            f'send_data_channel_message({{"type": "recording_status", "status": {str(status).lower()}}})'
        )

    @rx.event
    def set_peer_recording_status(self, status: bool):
        self.peer_recording_status = status

    def toggle_chat(self):
        self.is_chat_open = not self.is_chat_open
        self.is_settings_open = False
        self.is_menu_open = False

    def toggle_settings(self):
        self.is_settings_open = not self.is_settings_open
        self.is_chat_open = False
        self.is_menu_open = False

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def send_message(self, form_data: dict):
        message_text = form_data["chat_input"].strip()
        if message_text:
            new_message = {"user": self.text["you"], "text": message_text}
            self.messages.append(new_message)
            return rx.call_script(
                f'send_data_channel_message({{"type": "chat", "text": "{message_text}"}})'
            )

    @rx.event
    def add_chat_message(self, text: str):
        self.messages.append({"user": self.text["peer"], "text": text})

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"

    def toggle_language(self):
        self.language = "en" if self.language == "bn" else "bn"

    def toggle_reduced_motion(self):
        self.reduced_motion = not self.reduced_motion

    @rx.var
    def page_url(self) -> str:
        try:
            return (
                f"{self.router.page.full_raw_path.split('?')[0]}?room={self.room_name}"
            )
        except Exception as e:
            logging.exception(f"Error getting page_url: {e}")
            return ""

    @rx.event
    def copy_link(self):
        return [
            rx.set_clipboard(self.page_url),
            rx.toast.success(self.text["copied_link"]),
        ]