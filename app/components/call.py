import reflex as rx
from app.states.call_state import CallState
from app.components.video_tile import video_tile
from app.components.controls import call_controls
from app.components.chat import chat_panel
from app.components.settings import settings_panel
from app.components.header import call_header


def recording_consent_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h3(CallState.text.start_recording, class_name="text-lg font-bold"),
            rx.el.p(
                "You are about to start recording this call. The other participant will be notified.",
                class_name="text-sm text-gray-400 mt-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=CallState.cancel_recording,
                    class_name="px-4 py-2 bg-gray-700 rounded-md hover:bg-gray-600",
                ),
                rx.el.button(
                    "Confirm & Record",
                    on_click=CallState.confirm_recording,
                    class_name="px-4 py-2 bg-indigo-600 rounded-md hover:bg-indigo-700",
                ),
                class_name="flex justify-end gap-4 mt-6",
            ),
            class_name="bg-gray-800 text-white p-6 rounded-lg shadow-2xl w-full max-w-md",
        ),
        open=CallState.is_recording_consent_shown,
        class_name="fixed inset-0 z-50 open:flex items-center justify-center bg-black/50 backdrop-blur-sm",
    )


def call_interface() -> rx.Component:
    return rx.el.main(
        call_header(),
        rx.el.div(
            video_tile(
                id="remote-video",
                name=CallState.text.peer,
                status=CallState.connection_status,
                is_local=False,
                is_sharing=CallState.is_sharing_screen,
                is_recording=CallState.peer_recording_status,
            ),
            video_tile(
                id="local-video",
                name=CallState.text.you,
                status="connected",
                is_local=True,
                is_cam_on=CallState.is_camera_on,
                is_mic_on=CallState.is_mic_on,
                is_recording=CallState.is_recording,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 w-full p-4 pt-20",
        ),
        rx.el.div(
            call_controls(),
            class_name="fixed bottom-4 left-1/2 -translate-x-1/2 z-20 "
            + rx.cond(CallState.theme == "dark", "bg-gray-900/80", "bg-white/80")
            + " backdrop-blur-md rounded-2xl border "
            + rx.cond(CallState.theme == "dark", "border-gray-800", "border-gray-200"),
        ),
        chat_panel(),
        settings_panel(),
        recording_consent_modal(),
        class_name="relative w-full min-h-screen",
    )