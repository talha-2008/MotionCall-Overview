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
        rx.script(src="/webrtc.js"),
        rx.script("""
            function request_media_permissions() {
                navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                    .then(stream => {
                        window.localStream = stream;
                        rx.call_event("set_camera_permission", [true]);
                        rx.call_event("set_mic_permission", [true]);
                        const localVideo = document.getElementById('local-video');
                        if (localVideo) {
                            localVideo.srcObject = stream;
                        }
                        // Now that we have permissions, we can join the call
                        rx.call_event("join_call", []);
                    })
                    .catch(err => {
                        console.error("Error getting media permissions: ", err);
                        rx.call_event("set_camera_permission", [false]);
                        rx.call_event("set_mic_permission", [false]);
                        // Still try to join call, the backend will show a toast
                        rx.call_event("join_call", []);
                    });
            }
            """),
    ],
)
app.add_page(index, title="MotionCall by Talha")