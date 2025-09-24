import reflex as rx
from typing import TypedDict, Literal
from app.states.lang_state import TEXT_BN, TEXT_EN, TextContent


class Message(TypedDict):
    user: str
    text: str


rooms: dict[str, list[str]] = {}
sds: dict[str, dict] = {}


class CallState(rx.State):
    page_state: Literal["home", "lobby", "call"] = "home"
    room_name: str = ""
    theme: str = rx.LocalStorage("dark", name="motioncall_theme")
    language: str = rx.LocalStorage("bn", name="motioncall_lang")
    reduced_motion: bool = rx.LocalStorage(False, name="motioncall_reduced_motion")
    is_camera_on: bool = True
    is_mic_on: bool = True
    is_sharing_screen: bool = False
    is_recording: bool = False
    is_recording_consent_shown: bool = False
    is_chat_open: bool = False
    is_settings_open: bool = False
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
            if len(rooms.get(self.room_name, [])) >= 2:
                return rx.toast.error(f"Room '{self.room_name}' is full.")
            self.page_state = "lobby"
            return
        yield rx.toast.error(self.text["enter_room"])

    @rx.event
    def join_call(self):
        self.page_state = "call"
        return CallState.on_call_load

    @rx.event
    async def on_call_load(self):
        token = self.router.session.session_id
        if not token:
            return
        if self.room_name not in rooms:
            rooms[self.room_name] = []
        if token not in rooms[self.room_name]:
            rooms[self.room_name].append(token)
        if len(rooms[self.room_name]) > 1:
            self.connection_status = "connecting"
            yield rx.call_script(f"create_offer('{token}')")
        else:
            self.connection_status = "connecting"

    @rx.event
    def leave_call(self):
        token = self.router.session.session_id
        if self.room_name in rooms and token in rooms[self.room_name]:
            rooms[self.room_name].remove(token)
            if not rooms[self.room_name]:
                del rooms[self.room_name]
        return [rx.call_script("hangup()"), CallState.set_page_state("home")]

    @rx.event
    def handle_offer(self, offer: dict, token: str):
        sds[token] = offer
        other_peer = (
            rooms[self.room_name][0]
            if rooms[self.room_name][0] != token
            else rooms[self.room_name][1]
        )
        return CallState.handle_answer(offer, other_peer)

    @rx.event
    def handle_answer(self, offer: dict, token: str):
        return rx.call_script(f"create_answer('{token}', {offer})")

    @rx.event
    def handle_ice_candidate(self, candidate: dict, token: str):
        other_peer = (
            rooms[self.room_name][0]
            if rooms[self.room_name][0] != token
            else rooms[self.room_name][1]
        )
        return rx.call_script(f"add_ice_candidate('{other_peer}', {candidate})")

    @rx.event
    def set_connection_status(self, status: str):
        self.connection_status = status

    def toggle_camera(self):
        self.is_camera_on = not self.is_camera_on
        return rx.call_script(f"toggle_track('video', {self.is_camera_on})")

    def toggle_mic(self):
        self.is_mic_on = not self.is_mic_on
        return rx.call_script(f"toggle_track('audio', {self.is_mic_on})")

    def toggle_screen_share(self):
        self.is_sharing_screen = not self.is_sharing_screen
        return rx.call_script(f"toggle_screen_share({self.is_sharing_screen})")

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording_consent_shown = True
        else:
            self.is_recording = False
            yield (rx.call_script("stop_recording()"),)
            yield CallState.update_peer_recording_status(False)

    def confirm_recording(self):
        self.is_recording = True
        self.is_recording_consent_shown = False
        yield (rx.call_script("start_recording()"),)
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

    def toggle_settings(self):
        self.is_settings_open = not self.is_settings_open

    @rx.event
    def send_message(self, form_data: dict):
        message_text = form_data["chat_input"].strip()
        if message_text:
            self.messages.append({"user": self.text["you"], "text": message_text})
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
        return f"{self.router.page.full_raw_path.split('?')[0]}?room={self.room_name}"

    @rx.event
    def copy_link(self):
        return [
            rx.set_clipboard(self.page_url),
            rx.toast.success(self.text["copied_link"]),
        ]