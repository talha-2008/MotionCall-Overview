import reflex as rx
from app.states.call_state import CallState


def control_button(
    icon: str,
    text: str,
    on_click: rx.event.EventType,
    active: bool,
    danger: bool = False,
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            tag=icon,
            size=20,
            class_name=rx.cond(
                danger,
                "text-white",
                rx.cond(
                    active,
                    "text-white",
                    rx.cond(
                        CallState.theme == "dark", "text-gray-200", "text-gray-700"
                    ),
                ),
            ),
        ),
        rx.el.span(
            text,
            class_name=rx.cond(
                danger,
                "text-white",
                rx.cond(
                    active,
                    "text-white",
                    rx.cond(
                        CallState.theme == "dark", "text-gray-300", "text-gray-600"
                    ),
                ),
            )
            + " text-xs font-medium",
        ),
        on_click=on_click,
        class_name=f"flex flex-col items-center justify-center gap-1.5 p-3 rounded-lg w-20 h-20 {CallState.motion_class} "
        + rx.cond(
            danger,
            "bg-red-600 hover:bg-red-700",
            rx.cond(
                active,
                "bg-indigo-600 hover:bg-indigo-700",
                rx.cond(
                    CallState.theme == "dark",
                    "bg-[#151a21] hover:bg-gray-800",
                    "bg-gray-100 hover:bg-gray-200",
                ),
            ),
        ),
    )


def call_controls() -> rx.Component:
    return rx.el.div(
        control_button(
            icon=rx.cond(CallState.is_mic_on, "mic", "mic-off"),
            text=rx.cond(
                CallState.is_mic_on, CallState.text.mic_on, CallState.text.mic_off
            ),
            on_click=CallState.toggle_mic(),
            active=~CallState.is_mic_on,
        ),
        control_button(
            icon=rx.cond(CallState.is_camera_on, "video", "video-off"),
            text=rx.cond(
                CallState.is_camera_on, CallState.text.cam_on, CallState.text.cam_off
            ),
            on_click=CallState.toggle_camera(),
            active=~CallState.is_camera_on,
        ),
        control_button(
            icon=rx.cond(CallState.is_sharing_screen, "monitor-up", "monitor"),
            text=rx.cond(
                CallState.is_sharing_screen,
                CallState.text.stop_sharing,
                CallState.text.share_screen,
            ),
            on_click=CallState.toggle_screen_share(),
            active=CallState.is_sharing_screen,
        ),
        control_button(
            icon=rx.cond(CallState.is_recording, "square", "record-circle"),
            text=rx.cond(
                CallState.is_recording,
                CallState.text.stop_recording,
                CallState.text.start_recording,
            ),
            on_click=CallState.toggle_recording,
            active=CallState.is_recording,
        ),
        control_button(
            icon="phone-off",
            text=CallState.text.hang_up,
            on_click=CallState.leave_call,
            active=True,
            danger=True,
        ),
        class_name="flex items-center justify-center gap-3 md:gap-4 p-4",
    )