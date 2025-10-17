import reflex as rx
from app.states.state import State
from app.components.ui import input_panel, output_panel


def index() -> rx.Component:
    """The main page of the ATS Resume Regenerator."""
    return rx.el.main(
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    rx.icon("file-text", class_name="size-6 text-orange-400"),
                    rx.el.h1(
                        "ATS Resume Regenerator",
                        class_name="text-xl font-bold text-gray-100",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="w-full p-4 border-b border-gray-800",
            ),
            rx.el.div(
                input_panel(),
                output_panel(),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-px w-full h-full flex-grow bg-gray-800",
            ),
            class_name="flex flex-col h-screen w-full",
        ),
        class_name="font-['Inter'] bg-gray-900 text-gray-300",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="orange"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)