import reflex as rx
from app.states.call_state import CallState


def header_button(
    icon: str, on_click: rx.event.EventType, active: bool = False
) -> rx.Component:
    return rx.el.button(
        rx.icon(
            icon,
            size=20,
            class_name=rx.cond(
                active,
                "text-indigo-400",
                rx.cond(
                    CallState.theme == "dark",
                    "text-gray-400 hover:text-white",
                    "text-gray-500 hover:text-black",
                ),
            ),
        ),
        on_click=on_click,
        class_name="p-2 rounded-lg "
        + rx.cond(
            active,
            rx.cond(CallState.theme == "dark", "bg-indigo-900/50", "bg-indigo-100"),
            rx.cond(
                CallState.theme == "dark", "hover:bg-gray-800", "hover:bg-gray-100"
            ),
        )
        + f" {CallState.motion_class}",
    )


def call_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.icon("phone-call", size=24, class_name="text-indigo-500"),
            rx.el.h1(CallState.text.app_name, class_name="font-bold text-xl"),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("door-open", size=16, class_name="text-gray-400"),
                rx.el.span(CallState.room_name, class_name="font-mono text-sm"),
                rx.el.button(
                    rx.icon("copy", size=14),
                    on_click=CallState.copy_link,
                    class_name="ml-2 text-gray-500 hover:text-white",
                ),
                class_name="hidden md:flex items-center gap-2 p-2 rounded-lg "
                + rx.cond(CallState.theme == "dark", "bg-gray-800", "bg-gray-100"),
            )
        ),
        rx.el.div(
            header_button(
                "message-circle", CallState.toggle_chat, CallState.is_chat_open
            ),
            header_button(
                "settings-2", CallState.toggle_settings, CallState.is_settings_open
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="fixed top-0 left-0 right-0 z-20 flex items-center justify-between p-3 "
        + rx.cond(
            CallState.theme == "dark",
            "bg-gray-900/80 text-white",
            "bg-white/80 text-black",
        )
        + " backdrop-blur-md border-b "
        + rx.cond(CallState.theme == "dark", "border-gray-800", "border-gray-200"),
    )