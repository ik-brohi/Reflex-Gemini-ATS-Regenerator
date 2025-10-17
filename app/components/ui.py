import reflex as rx
from app.states.state import State


def _custom_textarea(
    label: str, value: rx.Var[str], on_change: rx.event.EventHandler
) -> rx.Component:
    """A custom resizable textarea component."""
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-gray-400 mb-2 block"),
        rx.el.textarea(
            default_value=value,
            on_change=on_change,
            placeholder=f"Paste the {label.lower().split(' ')[2]} here...",
            class_name="w-full h-full flex-grow p-4 bg-gray-900 rounded-lg resize-none text-gray-300 placeholder-gray-600 border border-gray-700 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all duration-200",
        ),
        class_name="flex flex-col h-full",
    )


def _file_type_tag(icon: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="size-4"),
        rx.el.span(text, class_name="text-xs font-medium"),
        class_name="flex items-center gap-1.5 bg-gray-800 border border-gray-700 rounded-full px-2 py-1",
    )


def _resume_uploader() -> rx.Component:
    """The resume file uploader component."""
    return rx.el.div(
        rx.el.label(
            "Upload Your Resume",
            class_name="text-sm font-medium text-gray-400 mb-2 block",
        ),
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="size-8 text-gray-500"),
                rx.el.h3(
                    "Click to upload or drag and drop",
                    class_name="font-semibold text-gray-400",
                ),
                rx.el.p(
                    rx.selected_files("upload_area"), class_name="text-sm text-gray-500"
                ),
                class_name="flex flex-col items-center justify-center gap-2 p-6 border-2 border-dashed border-gray-700 rounded-lg bg-gray-900 cursor-pointer hover:bg-gray-800/50 transition-colors",
            ),
            id="upload_area",
            on_drop=State.handle_upload(rx.upload_files(upload_id="upload_area")),
            accept={
                "application/pdf": [".pdf"],
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                    ".docx"
                ],
                "text/plain": [".txt"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/png": [".png"],
            },
            max_files=1,
            class_name="w-full",
        ),
        rx.el.div(
            _file_type_tag("file-text", "PDF"),
            _file_type_tag("file-text", "DOCX"),
            _file_type_tag("file-text", "TXT"),
            _file_type_tag("image", "JPG/PNG"),
            class_name="flex flex-wrap items-center gap-2 mt-2",
        ),
        rx.cond(
            State.uploaded_file_name,
            rx.el.div(
                rx.icon("file-check-2", class_name="size-5 text-green-500"),
                rx.el.div(
                    rx.el.p(
                        State.uploaded_file_name,
                        class_name="text-sm font-medium text-gray-200",
                    ),
                    rx.el.p(
                        f"{(State.file_size / 1024).to_string()} KB - {State.upload_status}",
                        class_name="text-xs text-gray-400",
                    ),
                    class_name="flex-grow",
                ),
                class_name="mt-4 flex items-center gap-3 p-3 bg-gray-800 border border-gray-700 rounded-lg w-full",
            ),
        ),
        class_name="flex flex-col h-full",
    )


def input_panel() -> rx.Component:
    """The left panel for user inputs."""
    return rx.el.div(
        rx.el.div(
            _resume_uploader(),
            _custom_textarea(
                "Paste the Target Job Description Here",
                State.job_description,
                State.set_job_description,
            ),
            class_name="grid grid-rows-2 gap-4 h-full",
        ),
        rx.el.button(
            rx.cond(
                State.is_generating,
                rx.fragment(rx.spinner(class_name="text-orange-500"), "Generating..."),
                "Generate ATS Resume",
            ),
            on_click=State.handle_generation,
            disabled=State.is_generating,
            class_name="w-full mt-4 px-6 py-3 rounded-lg font-semibold text-white bg-orange-600 hover:bg-orange-700 disabled:bg-gray-700 disabled:cursor-not-allowed transition-colors duration-200 flex items-center justify-center gap-2",
        ),
        class_name="p-6 flex flex-col h-full bg-gray-950",
    )


def _status_indicator() -> rx.Component:
    """A component to display the current generation status."""
    return rx.el.div(
        rx.el.h3("Status", class_name="text-lg font-semibold text-gray-100 mb-3"),
        rx.el.div(
            rx.match(
                State.status,
                ("Ready", rx.icon("circle", class_name="text-gray-500")),
                ("Generating...", rx.spinner(class_name="text-blue-500")),
                ("Complete", rx.icon("check_check", class_name="text-green-500")),
                ("Error", rx.icon("circle_x", class_name="text-red-500")),
            ),
            rx.el.p(State.status, class_name="font-medium text-gray-300"),
            class_name="flex items-center gap-3 p-4 bg-gray-900 rounded-lg border border-gray-800",
        ),
        class_name="w-full",
    )


def output_panel() -> rx.Component:
    """The right panel for status and download."""
    return rx.el.div(
        _status_indicator(),
        rx.el.div(class_name="flex-grow"),
        rx.el.button(
            rx.icon("download", class_name="mr-2"),
            "Download Resume (.docx)",
            on_click=rx.download(url=rx.get_upload_url(State.generated_file_path)),
            disabled=~State.generation_complete,
            class_name="w-full px-6 py-3 rounded-lg font-semibold text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-700 disabled:cursor-not-allowed disabled:text-gray-400 transition-colors duration-200 flex items-center justify-center",
        ),
        class_name="p-6 flex flex-col h-full bg-gray-950",
    )