import reflex as rx
from app.states.call_state import CallState, Message


def message_component(message: Message) -> rx.Component:
    is_user = message["user"] == CallState.text.you
    return rx.el.div(
        rx.el.p(message["text"], class_name="text-sm"),
        class_name=rx.cond(
            is_user,
            rx.cond(
                CallState.theme == "dark",
                "bg-indigo-600 self-end rounded-l-lg rounded-t-lg",
                "bg-indigo-500 text-white self-end rounded-l-lg rounded-t-lg",
            ),
            rx.cond(
                CallState.theme == "dark",
                "bg-gray-700 self-start rounded-r-lg rounded-t-lg",
                "bg-gray-200 text-gray-800 self-start rounded-r-lg rounded-t-lg",
            ),
        )
        + " p-3 max-w-[80%]",
    )


def chat_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("message-circle", size=20),
                rx.el.h3(CallState.text.chat_title, class_name="font-bold text-lg"),
                class_name="flex items-center gap-3 p-4 border-b "
                + rx.cond(
                    CallState.theme == "dark", "border-gray-700", "border-gray-200"
                ),
            ),
            rx.el.div(
                rx.cond(
                    CallState.messages.length() > 0,
                    rx.foreach(CallState.messages, message_component),
                    rx.el.div(
                        rx.icon("messages-square", size=48, class_name="text-gray-500"),
                        rx.el.p(
                            CallState.text.say_hi, class_name="text-gray-500 text-sm"
                        ),
                        class_name="flex flex-col items-center justify-center h-full gap-4 text-center",
                    ),
                ),
                class_name="flex-grow p-4 flex flex-col gap-4 overflow-y-auto",
            ),
            rx.el.form(
                rx.el.input(
                    name="chat_input",
                    placeholder=CallState.text.send_message_placeholder,
                    class_name="flex-grow bg-transparent outline-none text-sm",
                ),
                rx.el.button(
                    rx.icon("send", size=16),
                    type="submit",
                    class_name="p-2 rounded-md "
                    + rx.cond(
                        CallState.theme == "dark",
                        "bg-gray-700 hover:bg-gray-600",
                        "bg-gray-200 hover:bg-gray-300",
                    ),
                ),
                on_submit=CallState.send_message,
                reset_on_submit=True,
                class_name="flex items-center gap-2 p-2 m-4 border rounded-lg "
                + rx.cond(
                    CallState.theme == "dark",
                    "border-gray-700 bg-gray-900",
                    "border-gray-200 bg-white",
                ),
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="absolute top-0 right-0 h-full w-full max-w-sm "
        + rx.cond(
            CallState.theme == "dark",
            "bg-gray-900/80 text-white",
            "bg-white/80 text-black",
        )
        + " backdrop-blur-md border-l "
        + rx.cond(CallState.theme == "dark", "border-gray-700", "border-gray-200")
        + " transform "
        + rx.cond(CallState.is_chat_open, "translate-x-0", "translate-x-full")
        + f" {CallState.motion_class} z-30",
    )