# import logging
# import flet as ft
# import asyncio
# import httpx

# # from knowledge_navigator.logger._custom_handler import RichConsoleHandler


# class LibrarianApp:
#     def __init__(self):
#         # Asynchronous HTTP client
#         self._async_req = httpx.AsyncClient(timeout=None)

#     async def fetch_data(self, query: str):
#         url = "http://localhost:8000/chat/get_query"
#         # Stream the response text from the server
#         async with self._async_req.stream(
#             method="POST", url=url, params={"query": query}
#         ) as response:
#             async for chunk in response.aiter_text():
#                 yield chunk

#     def get_theme_colors(self, theme_mode):
#         # Define theme colors based on the current mode
#         if theme_mode == ft.ThemeMode.LIGHT:
#             return {
#                 "user_bg": ft.colors.BLUE_50,
#                 "ai_bg": ft.colors.GREEN_50,
#                 "user_avatar_bg": ft.colors.BLUE,
#                 "ai_avatar_bg": ft.colors.GREEN,
#                 "text": ft.colors.BLACK,
#             }
#         else:
#             return {
#                 "user_bg": ft.colors.BLUE_900,
#                 "ai_bg": ft.colors.GREEN_900,
#                 "user_avatar_bg": ft.colors.BLUE_400,
#                 "ai_avatar_bg": ft.colors.GREEN_400,
#                 "text": ft.colors.WHITE,
#             }

#     def create_message_container(self, is_user, avatar_text, name, message, theme_mode):
#         # Create a message container for chat bubbles
#         colors = self.get_theme_colors(theme_mode)
#         bg_color = colors["user_bg"] if is_user else colors["ai_bg"]
#         avatar_bg = colors["user_avatar_bg"] if is_user else colors["ai_avatar_bg"]

#         return ft.Container(
#             content=ft.ListTile(
#                 leading=ft.CircleAvatar(
#                     content=ft.Text(avatar_text), bgcolor=avatar_bg
#                 ),
#                 title=ft.Text(name, weight=ft.FontWeight.BOLD, color=colors["text"]),
#                 subtitle=ft.Text(message, color=colors["text"], selectable=True),
#             ),
#             bgcolor=bg_color,
#             border_radius=ft.border_radius.all(10),
#             margin=ft.margin.symmetric(vertical=5),
#         )

#     async def on_query_submit(
#         self,
#         page,
#         query_input,
#         response_output,
#         submit_button,
#         progress_ring,
#         chat_history,
#     ):
#         query = query_input.value.strip()
#         if query:
#             # Display user's query immediately
#             user_message = self.create_message_container(
#                 True, "U", "User", query, page.theme_mode
#             )
#             chat_history.append(user_message)
#             response_output.controls.append(user_message)
#             page.update()

#             # Show progress ring while processing
#             submit_button.visible = False
#             progress_ring.visible = True
#             page.update()

#             # Set up container for AI response
#             response_text = ft.Text(
#                 "", overflow=ft.TextOverflow.VISIBLE, selectable=True
#             )
#             ai_message = self.create_message_container(
#                 False, "AI", "AI Librarian", "", page.theme_mode
#             )
#             ai_message.content.subtitle = response_text
#             chat_history.append(ai_message)
#             response_output.controls.append(ai_message)

#             # Fetch and display AI response in chunks
#             async for response_chunk in self.fetch_data(query):
#                 response_text.value += response_chunk
#                 page.update()

#             # Hide progress ring and reset input
#             progress_ring.visible = False
#             submit_button.visible = True
#             query_input.value = ""
#             page.update()

#     async def theme_changer(self, page, chat_history):
#         # Toggle theme between light and dark
#         page.theme_mode = (
#             ft.ThemeMode.DARK
#             if page.theme_mode == ft.ThemeMode.LIGHT
#             else ft.ThemeMode.LIGHT
#         )
#         theme_switcher_icon = (
#             ft.icons.LIGHT_MODE
#             if page.theme_mode == ft.ThemeMode.LIGHT
#             else ft.icons.DARK_MODE
#         )
#         # Update chat bubbles with new theme colors
#         for message in chat_history:
#             is_user = message.content.title.value == "User"
#             message.bgcolor = self.get_theme_colors(page.theme_mode)[
#                 "user_bg" if is_user else "ai_bg"
#             ]
#             message.content.leading.bgcolor = self.get_theme_colors(page.theme_mode)[
#                 "user_avatar_bg" if is_user else "ai_avatar_bg"
#             ]
#             message.content.title.color = self.get_theme_colors(page.theme_mode)["text"]
#             message.content.subtitle.color = self.get_theme_colors(page.theme_mode)[
#                 "text"
#             ]
#         page.update()

#     def navigate(self, page, index, response_output, chat_history):
#         # Handle navigation between different sections
#         if index == 0:
#             response_output.controls = [
#                 ft.Text("Welcome to the AI Librarian!", style="headlineSmall")
#             ] + chat_history
#         elif index == 1:
#             response_output.controls = [
#                 ft.Text(
#                     "Search through the library's collection here!",
#                     style="headlineSmall",
#                 )
#             ] + chat_history
#         elif index == 2:
#             response_output.controls = [
#                 ft.Text("Adjust your settings here.", style="headlineSmall")
#             ] + chat_history
#         page.update()

#     def main(self, page: ft.Page):
#         page.title = "V.S.B Engineering College - AI Librarian"
#         page.theme = ft.Theme(color_scheme_seed="#eeff00")
#         page.theme_mode = ft.ThemeMode.LIGHT

#         # Session-specific state
#         chat_history = []

#         # Setup theme switch button
#         theme_switcher = ft.IconButton(
#             icon=ft.icons.LIGHT_MODE,
#             on_click=lambda e: asyncio.create_task(
#                 self.theme_changer(page, chat_history)
#             ),
#             tooltip="Switch Theme Mode",
#         )

#         header = ft.Text("AI Librarian", style="headlineMedium", weight="bold")

#         # Text field for query input
#         query_input = ft.TextField(
#             label="Ask a question",
#             autofocus=True,
#             expand=True,
#             on_submit=lambda e: asyncio.create_task(
#                 self.on_query_submit(
#                     page,
#                     query_input,
#                     response_output,
#                     submit_button,
#                     progress_ring,
#                     chat_history,
#                 )
#             ),
#             border_radius=10,
#             filled=True,
#             prefix_icon=ft.icons.QUESTION_ANSWER,
#         )

#         # Submit button animation and function
#         async def on_submit_button_click(e):
#             submit_button.offset = ft.transform.Offset(0, 2)
#             await page.update_async()
#             await asyncio.sleep(0.1)
#             submit_button.offset = ft.transform.Offset(0, 0)
#             await page.update_async()

#             await self.on_query_submit(
#                 page,
#                 query_input,
#                 response_output,
#                 submit_button,
#                 progress_ring,
#                 chat_history,
#             )

#         submit_button = ft.ElevatedButton(
#             text="Send",
#             icon=ft.icons.SEND,
#             on_click=on_submit_button_click,
#             style=ft.ButtonStyle(
#                 shape=ft.RoundedRectangleBorder(radius=10),
#                 elevation={"pressed": 0, "": 5},
#                 animation_duration=500,
#                 color={"": ft.colors.WHITE},
#                 bgcolor={
#                     "": ft.colors.PURPLE,
#                     ft.MaterialState.HOVERED: ft.colors.PURPLE_500,
#                 },
#             ),
#             scale=ft.transform.Scale(scale=1),
#             offset=ft.transform.Offset(0, 0),
#             animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_CUBIC),
#             animate_offset=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
#         )

#         def on_submit_button_hover(e):
#             submit_button.scale = ft.transform.Scale(
#                 scale=1.1 if e.data == "true" else 1
#             )
#             submit_button.update()

#         submit_button.on_hover = on_submit_button_hover

#         # Progress ring for loading state
#         progress_ring = ft.ProgressRing(visible=False)

#         # Output area for chat responses
#         response_output = ft.Column(
#             scroll=ft.ScrollMode.AUTO,
#             expand=True,
#             spacing=10,
#         )

#         input_container = ft.Row(
#             [
#                 query_input,
#                 ft.Container(submit_button, padding=10),
#                 progress_ring,
#             ],
#             alignment=ft.MainAxisAlignment.SPACE_AROUND,
#             spacing=20,
#         )

#         content_container = ft.Column(
#             [
#                 header,
#                 response_output,
#                 ft.Divider(height=20, thickness=2),
#                 input_container,
#             ],
#             expand=True,
#             spacing=15,
#         )

#         # Bottom navigation bar
#         navigation_bar = ft.NavigationBar(
#             selected_index=0,
#             on_change=lambda e: self.navigate(
#                 page, e.control.selected_index, response_output, chat_history
#             ),
#             destinations=[
#                 ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
#                 ft.NavigationDestination(icon=ft.icons.SEARCH, label="Search"),
#                 ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
#             ],
#         )

#         # Set page layout
#         page.add(
#             ft.Column(
#                 [
#                     ft.Row(
#                         [
#                             ft.Icon(ft.icons.BOOKMARK, color="blue", size=40),
#                             ft.Container(theme_switcher, margin=10),
#                         ],
#                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                     ),
#                     ft.Divider(height=5, thickness=1),
#                     content_container,
#                     navigation_bar,
#                 ],
#                 expand=True,
#             )
#         )


# # Create an instance of the LibrarianApp and run it
# librarian_app = LibrarianApp()

# # Flet app entry point
# if __name__ == "__main__":
#     ft.app(target=librarian_app.main)
import logging
import flet as ft
import asyncio
import httpx

# from knowledge_navigator.logger._custom_handler import RichConsoleHandler


class LibrarianApp:
    def __init__(self):
        self.query_input = None
        self.response_output = None
        self.page = None
        self.chat_history = []
        self.progress_ring = None
        self.submit_button = None

        # Asynchronous HTTP client
        self._async_req = httpx.AsyncClient(timeout=None)

        # Set up logging
        # self.setup_logging()

    # def setup_logging(self):
    #     from knowledge_navigator.loggers import (
    #         httpx_logger,
    #         httpx_core_logger,
    #         app_logger,
    #         flet_core_logger,
    #         flet_logger,
    #     )
    #     from knowledge_navigator.logger import configure_present_loggers

    #     configure_present_loggers(
    #         loggers=[
    #             httpx_logger,
    #             httpx_core_logger,
    #             app_logger,
    #             flet_core_logger,
    #             flet_logger,
    #         ],
    #         handlers=[RichConsoleHandler(level=logging.DEBUG)],
    #     )

    async def fetch_data(self, query: str):
        url = "http://localhost:8000/chat/get_query"
        async with self._async_req.post(url, json={"query": query}) as response:
            result = await response.json()
            yield result["response"]

    def get_theme_colors(self):
        # Define theme colors based on the current mode
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            return {
                "user_bg": ft.colors.BLUE_50,
                "ai_bg": ft.colors.GREEN_50,
                "user_avatar_bg": ft.colors.BLUE,
                "ai_avatar_bg": ft.colors.GREEN,
                "text": ft.colors.BLACK,
            }
        else:
            return {
                "user_bg": ft.colors.BLUE_900,
                "ai_bg": ft.colors.GREEN_900,
                "user_avatar_bg": ft.colors.BLUE_400,
                "ai_avatar_bg": ft.colors.GREEN_400,
                "text": ft.colors.WHITE,
            }

    def create_message_container(self, is_user, avatar_text, name, message):
        # Create a message container for chat bubbles
        colors = self.get_theme_colors()
        bg_color = colors["user_bg"] if is_user else colors["ai_bg"]
        avatar_bg = colors["user_avatar_bg"] if is_user else colors["ai_avatar_bg"]

        return ft.Container(
            content=ft.ListTile(
                leading=ft.CircleAvatar(
                    content=ft.Text(avatar_text), bgcolor=avatar_bg
                ),
                title=ft.Text(name, weight=ft.FontWeight.BOLD, color=colors["text"]),
                subtitle=ft.Text(message, color=colors["text"], selectable=True),
            ),
            bgcolor=bg_color,
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.symmetric(vertical=5),
        )

    async def on_query_submit(self, _):
        query = self.query_input.value.strip()
        if query:
            # Display user's query immediately
            user_message = self.create_message_container(True, "U", "User", query)
            self.chat_history.append(user_message)
            self.response_output.controls.append(user_message)
            self.page.update()

            # Show progress ring while processing
            self.submit_button.visible = False
            self.progress_ring.visible = True
            self.page.update()

            # Set up container for AI response
            response_text = ft.Text(
                "", overflow=ft.TextOverflow.VISIBLE, selectable=True
            )
            ai_message = self.create_message_container(False, "AI", "AI Librarian", "")
            ai_message.content.subtitle = response_text
            self.chat_history.append(ai_message)
            self.response_output.controls.append(ai_message)

            # Fetch and display AI response in chunks
            async for response_chunk in self.fetch_data(query):
                response_text.value += response_chunk
                self.page.update()

            # Hide progress ring and reset input
            self.progress_ring.visible = False
            self.submit_button.visible = True
            self.query_input.value = ""
            self.page.update()

    async def theme_changer(self, e):
        # Toggle theme between light and dark
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.theme_switcher.icon = (
            ft.icons.LIGHT_MODE
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.icons.DARK_MODE
        )
        # Update chat bubbles with new theme colors
        for message in self.chat_history:
            is_user = message.content.title.value == "User"
            message.bgcolor = self.get_theme_colors()["user_bg" if is_user else "ai_bg"]
            message.content.leading.bgcolor = self.get_theme_colors()[
                "user_avatar_bg" if is_user else "ai_avatar_bg"
            ]
            message.content.title.color = self.get_theme_colors()["text"]
            message.content.subtitle.color = self.get_theme_colors()["text"]
        self.page.update()

    def navigate(self, index: int):
        # Handle navigation between different sections
        if index == 0:
            self.response_output.controls = [
                ft.Text("Welcome to the AI Librarian!", style="headlineSmall")
            ] + self.chat_history
        elif index == 1:
            self.response_output.controls = [
                ft.Text(
                    "Search through the library's collection here!",
                    style="headlineSmall",
                )
            ] + self.chat_history
        elif index == 2:
            self.response_output.controls = [
                ft.Text("Adjust your settings here.", style="headlineSmall")
            ] + self.chat_history
        self.page.update()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "V.S.B Engineering College - AI Librarian"
        page.theme = ft.Theme(color_scheme_seed="#eeff00")
        page.theme_mode = ft.ThemeMode.LIGHT

        # Setup theme switch button
        self.theme_switcher = ft.IconButton(
            icon=ft.icons.LIGHT_MODE,
            on_click=self.theme_changer,
            tooltip="Switch Theme Mode",
        )

        header = ft.Text("AI Librarian", style="headlineMedium", weight="bold")

        # Text field for query input
        self.query_input = ft.TextField(
            label="Ask a question",
            autofocus=True,
            expand=True,
            on_submit=self.on_query_submit,
            border_radius=10,
            filled=True,
            prefix_icon=ft.icons.QUESTION_ANSWER,
        )

        # Submit button animation and function
        async def on_submit_button_click(e):
            self.submit_button.offset = ft.transform.Offset(0, 2)
            await self.page.update_async()
            await asyncio.sleep(0.1)
            self.submit_button.offset = ft.transform.Offset(0, 0)
            await self.page.update_async()

            await self.on_query_submit(e)

        self.submit_button = ft.ElevatedButton(
            text="Send",
            icon=ft.icons.SEND,
            on_click=on_submit_button_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation={"pressed": 0, "": 5},
                animation_duration=500,
                color={"": ft.colors.WHITE},
                bgcolor={
                    "": ft.colors.PURPLE,
                    ft.MaterialState.HOVERED: ft.colors.PURPLE_500,
                },
            ),
            scale=ft.transform.Scale(scale=1),
            offset=ft.transform.Offset(0, 0),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_CUBIC),
            animate_offset=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
        )

        def on_submit_button_hover(e):
            self.submit_button.scale = ft.transform.Scale(
                scale=1.1 if e.data == "true" else 1
            )
            self.submit_button.update()

        self.submit_button.on_hover = on_submit_button_hover

        # Progress ring for loading state
        self.progress_ring = ft.ProgressRing(visible=False)

        # Output area for chat responses
        self.response_output = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10,
        )

        input_container = ft.Row(
            [
                self.query_input,
                ft.Container(self.submit_button, padding=10),
                self.progress_ring,
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20,
        )

        content_container = ft.Column(
            [
                header,
                self.theme_switcher,
                self.response_output,
                input_container,
            ],
            expand=True,
        )

        # Navigation
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.HOME,
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SEARCH,
                    label="Search",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.SETTINGS,
                    label="Settings",
                ),
            ],
            on_change=self.navigate,
        )

        page.add(
            ft.Column(
                [
                    self.navigation_bar,
                    content_container,
                ],
                expand=True,
            )
        )


# Run the app
if __name__ == "__main__":
    app = LibrarianApp()
    ft.app(target=app.main)
