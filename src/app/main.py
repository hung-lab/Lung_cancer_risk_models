"""Main application entry point."""

import customtkinter as ctk
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController


def main() -> None:
    """Initialize and run the customtkinter application."""
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
    
    root = ctk.CTk()
    root.title("CustomTkinter App")
    root.geometry("800x600")
    
    # Set minimum window size
    root.minsize(400, 300)
    
    # Configure styles
    configure_styles(root)
    
    # Create MVC components
    controller = MainController(root)
    view = MainWindow(root, controller)
    
    # Start the application
    root.mainloop()


def configure_styles(root: ctk.CTk) -> None:
    """Configure application styles and themes."""
    # Configure customtkinter styles
    style = ctk.CTkStyle()
    
    # Custom styles
    style.configure("Title.TLabel", 
                   font=("Arial", 16, "bold"))
    
    style.configure("Header.TLabel",
                   font=("Arial", 12, "bold"))
    
    # Configure button hover effect
    style.configure("CTkButton",
                   corner_radius=8,
                   font=("Arial", 11, "bold"))
    
    # Configure entry widget
    style.configure("CTkEntry",
                   corner_radius=6,
                   font=("Arial", 11))


if __name__ == "__main__":
    main()
