import reflex as rx
from app.states.call_state import CallState


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, size=24, class_name="text-indigo-400"),
            class_name="p-3 rounded-lg bg-gray-800 w-fit",
        ),
        rx.el.h3(title, class_name="font-bold mt-4 text-lg"),
        rx.el.p(description, class_name="text-sm text-gray-400 mt-1"),
        class_name="p-6 rounded-xl "
        + rx.cond(CallState.theme == "dark", "bg-[#151a21]", "bg-gray-100")
        + f" {CallState.motion_class} border "
        + rx.cond(
            CallState.theme == "dark",
            "border-gray-800 hover:border-indigo-600",
            "border-gray-200 hover:border-indigo-400",
        ),
    )


def home() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("phone-call", size=32, class_name="text-indigo-500"),
                rx.el.h1(CallState.text.app_name, class_name="text-4xl font-extrabold"),
                class_name="flex items-center gap-4",
            ),
            rx.el.p(
                "1:1 video calls, screen share, chat, recording—simple but advanced.",
                class_name="text-gray-400 max-w-lg text-center",
            ),
            rx.el.form(
                rx.el.input(
                    name="room_name",
                    placeholder=CallState.text.enter_room,
                    class_name="w-full md:w-80 px-4 py-3 bg-transparent rounded-l-lg outline-none font-mono",
                ),
                rx.el.button(
                    CallState.text.join_button,
                    type="submit",
                    class_name=f"px-6 py-3 bg-indigo-600 hover:bg-indigo-700 font-semibold rounded-r-lg {CallState.motion_class}",
                ),
                on_submit=CallState.join_lobby,
                class_name="flex items-center rounded-lg border "
                + rx.cond(
                    CallState.theme == "dark",
                    "bg-[#151a21] border-gray-700 focus-within:border-indigo-500",
                    "bg-white border-gray-300 focus-within:border-indigo-500",
                )
                + f" {CallState.motion_class}",
            ),
            class_name="flex flex-col items-center gap-6",
        ),
        rx.el.div(
            feature_card(
                icon="video",
                title=CallState.text.feature_1_title,
                description=CallState.text.feature_1_desc,
            ),
            feature_card(
                icon="monitor-up",
                title=CallState.text.feature_2_title,
                description=CallState.text.feature_2_desc,
            ),
            feature_card(
                icon="message-circle",
                title=CallState.text.feature_3_title,
                description=CallState.text.feature_3_desc,
            ),
            feature_card(
                icon="record-circle",
                title=CallState.text.feature_4_title,
                description=CallState.text.feature_4_desc,
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl w-full",
        ),
        class_name="flex flex-col items-center justify-center min-h-screen gap-16 px-4 py-12 "
        + rx.cond(CallState.theme == "dark", "text-white", "text-black"),
    )