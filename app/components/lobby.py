import reflex as rx
from app.states.call_state import CallState


def lobby_toggle_button(
    icon_on: str,
    icon_off: str,
    text: str,
    is_on: rx.Var[bool],
    on_click: rx.event.EventType,
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            tag=rx.cond(is_on, icon_on, icon_off),
            size=24,
            class_name=rx.cond(is_on, "text-white", "text-red-500"),
        ),
        rx.el.span(text, class_name="text-xs font-medium"),
        on_click=on_click,
        class_name=f"flex flex-col items-center justify-center gap-2 w-20 h-20 rounded-xl {CallState.motion_class} "
        + rx.cond(
            is_on,
            rx.cond(
                CallState.theme == "dark",
                "bg-gray-700 hover:bg-gray-600",
                "bg-gray-600 text-white hover:bg-gray-700",
            ),
            rx.cond(
                CallState.theme == "dark",
                "bg-red-900/50 text-red-300 hover:bg-red-900/70",
                "bg-red-100 text-red-600 hover:bg-red-200",
            ),
        ),
    )


def lobby() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(CallState.text.lobby_title, class_name="text-2xl font-bold"),
            rx.el.p(
                f"Room: {CallState.room_name}",
                class_name="font-mono text-sm text-gray-400",
            ),
            class_name="text-center",
        ),
        rx.el.div(
            rx.el.video(
                id="local-video",
                auto_play=True,
                muted=True,
                plays_inline=True,
                class_name="w-full h-full object-cover "
                + rx.cond(~CallState.is_camera_on, "hidden", ""),
            ),
            rx.cond(
                ~CallState.is_camera_on,
                rx.el.div(
                    rx.icon("video-off", size=48, class_name="text-gray-600"),
                    class_name="w-full h-full flex items-center justify-center "
                    + rx.cond(CallState.theme == "dark", "bg-gray-800", "bg-gray-200"),
                ),
            ),
            class_name="w-full max-w-2xl aspect-video rounded-xl overflow-hidden bg-gray-800 shadow-lg relative",
        ),
        rx.el.div(
            lobby_toggle_button(
                icon_on="mic",
                icon_off="mic-off",
                text=rx.cond(CallState.is_mic_on, "Mic On", "Mic Off"),
                is_on=CallState.is_mic_on,
                on_click=CallState.toggle_mic(),
            ),
            lobby_toggle_button(
                icon_on="video",
                icon_off="video-off",
                text=rx.cond(CallState.is_camera_on, "Cam On", "Cam Off"),
                is_on=CallState.is_camera_on,
                on_click=CallState.toggle_camera(),
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.button(
                CallState.text.back_button,
                on_click=lambda: CallState.set_page_state("home"),
                class_name="px-8 py-3 rounded-lg font-semibold "
                + rx.cond(
                    CallState.theme == "dark",
                    "bg-gray-800 hover:bg-gray-700",
                    "bg-gray-200 hover:bg-gray-300",
                )
                + f" {CallState.motion_class}",
            ),
            rx.el.button(
                rx.icon("arrow-right", class_name="mr-2"),
                CallState.text.join_call_button,
                on_click=CallState.join_call,
                class_name="px-8 py-3 rounded-lg font-semibold bg-indigo-600 hover:bg-indigo-700 flex items-center"
                + f" {CallState.motion_class}",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex flex-col items-center justify-center gap-8 min-h-screen p-4 "
        + rx.cond(CallState.theme == "dark", "text-white", "text-black"),
        on_mount=rx.call_script('init_local_media("local-video")'),
    )