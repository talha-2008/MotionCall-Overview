import reflex as rx
from app.states.call_state import CallState


def settings_toggle(
    label: str, icon: str, on_change: rx.event.EventType, is_checked: rx.Var[bool]
) -> rx.Component:
    return rx.el.label(
        rx.el.div(
            rx.icon(icon, size=18, class_name="text-gray-400"),
            rx.el.span(label, class_name="font-medium text-sm"),
            class_name="flex items-center gap-3",
        ),
        rx.el.div(
            rx.el.input(
                type="checkbox",
                class_name="sr-only peer",
                on_change=on_change,
                checked=is_checked,
            ),
            rx.el.div(
                class_name="w-11 h-6 bg-gray-200 rounded-full peer-focus:ring-2 peer-focus:ring-indigo-300 dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-indigo-600"
            ),
        ),
        class_name="flex items-center justify-between p-3 hover:bg-gray-800 rounded-lg cursor-pointer",
    )


def settings_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("settings-2", size=20),
            rx.el.h3(CallState.text.settings_title, class_name="font-bold text-lg"),
            class_name="flex items-center gap-3 p-4 border-b "
            + rx.cond(CallState.theme == "dark", "border-gray-700", "border-gray-200"),
        ),
        rx.el.div(
            settings_toggle(
                label=rx.cond(
                    CallState.theme == "dark",
                    CallState.text.dark_mode,
                    CallState.text.light_mode,
                ),
                icon=rx.cond(CallState.theme == "dark", "moon", "sun"),
                on_change=CallState.toggle_theme,
                is_checked=CallState.theme == "dark",
            ),
            settings_toggle(
                label=f"{CallState.text.language}: {CallState.language.upper()}",
                icon="languages",
                on_change=CallState.toggle_language,
                is_checked=CallState.language == "bn",
            ),
            settings_toggle(
                label=CallState.text.reduced_motion,
                icon="accessibility",
                on_change=CallState.toggle_reduced_motion,
                is_checked=CallState.reduced_motion,
            ),
            class_name="p-4 flex flex-col gap-2",
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
        + rx.cond(CallState.is_settings_open, "translate-x-0", "translate-x-full")
        + f" {CallState.motion_class} z-30",
    )