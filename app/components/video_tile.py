import reflex as rx
from app.states.call_state import CallState


def status_badge(status: str) -> rx.Component:
    return rx.el.div(
        rx.match(
            status,
            (
                "connecting",
                rx.el.span(
                    class_name="absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75 animate-ping"
                ),
            ),
            (
                "reconnecting",
                rx.el.span(
                    class_name="absolute inline-flex h-full w-full rounded-full bg-yellow-400 opacity-75 animate-ping"
                ),
            ),
            (
                "connected",
                rx.el.span(
                    class_name="absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
                ),
            ),
            rx.el.span(
                class_name="absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"
            ),
        ),
        rx.el.span(
            class_name=rx.cond(
                status == "connected",
                "relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500",
                "relative inline-flex rounded-full h-2.5 w-2.5 bg-yellow-500",
            )
        ),
        class_name="flex h-2.5 w-2.5 relative",
    )


def video_tile(
    id: str,
    name: str,
    status: str,
    is_local: bool = False,
    is_cam_on: bool = True,
    is_mic_on: bool = True,
    is_sharing: bool = False,
    is_recording: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.video(
            id=id,
            auto_play=True,
            muted=is_local,
            plays_inline=True,
            class_name="w-full h-full object-cover "
            + rx.cond(~is_cam_on, "hidden", ""),
        ),
        rx.cond(
            ~is_cam_on,
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={name}",
                    class_name="w-24 h-24 rounded-full bg-gray-700",
                ),
                class_name="w-full h-full flex items-center justify-center bg-gray-800",
            ),
        ),
        rx.el.div(
            rx.el.div(
                status_badge(status),
                rx.el.p(name, class_name="font-medium text-sm"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon(
                    tag=rx.cond(is_mic_on, "mic", "mic-off"),
                    class_name=rx.cond(is_mic_on, "text-gray-200", "text-red-500"),
                    size=16,
                ),
                class_name="p-1.5 bg-black/20 rounded-full",
            ),
            class_name="absolute bottom-3 left-3 right-3 flex justify-between items-center p-1 bg-black/30 backdrop-blur-sm rounded-lg",
        ),
        rx.cond(
            is_sharing,
            rx.el.div(
                rx.icon("monitor-up", size=16),
                rx.el.p(CallState.text.stop_sharing, class_name="text-sm font-medium"),
                class_name="absolute top-3 left-3 flex items-center gap-2 p-2 bg-blue-600/80 rounded-lg animate-pulse",
            ),
            None,
        ),
        rx.cond(
            is_recording,
            rx.el.div(
                rx.icon("bookmark_check", size=16, class_name="text-red-500"),
                rx.el.p("REC", class_name="text-sm font-medium text-red-400"),
                class_name="absolute top-3 right-3 flex items-center gap-2 p-2 bg-black/50 rounded-lg animate-pulse",
            ),
            None,
        ),
        class_name="aspect-video bg-gray-900 rounded-xl overflow-hidden relative text-white shadow-lg",
    )