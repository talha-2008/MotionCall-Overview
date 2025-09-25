import reflex as rx
from app.states.call_state import CallState
from app.components.home import home
from app.components.lobby import lobby
from app.components.call import call_interface


def index() -> rx.Component:
    return rx.el.main(
        rx.match(
            CallState.page_state,
            ("home", home()),
            ("lobby", lobby()),
            ("call", call_interface()),
            home(),
        ),
        class_name="font-['Inter'] "
        + rx.cond(CallState.theme == "dark", "dark bg-[#0f1216]", ""),
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.script(
            "const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });"
        ),
        rx.script(src="/webrtc.js"),
    ],
)
app.add_page(index, title="MotionCall by Talha")