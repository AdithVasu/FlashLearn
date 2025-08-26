import streamlit as st
import os
import io
from datetime import datetime

# Import modules directly from the same directory
from transcriber import transcribe_youtube_video
from summarizer import summarize_text
from database import init_db, save_notes_to_db, get_all_notes_from_db, delete_notes_from_db
from styles import apply_custom_styles

# Initialize the database
init_db()

st.set_page_config(
    page_title="Academic YouTube Notes Summarizer",
    page_icon="📄",
    layout="wide"
)

# --- START OF CUSTOM CSS ---
custom_css = """
<style>
/* Remove emojis and make tabs look more professional */
.st-emotion-cache-1ft41h9.e1vs89f30 {
    font-size: 1.2rem;
}

/* Style the Streamlit slider tracks */
div.stSlider > div[data-baseweb="slider"] > div > div {
    background: #007BFF !important; /* Professional blue color */
}

/* Change the slider thumb color */
div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
    background-color: #0056b3 !important; /* A darker shade for the thumb */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# --- END OF CUSTOM CSS ---

# Apply custom styles from styles.py
apply_custom_styles()

# Initialize all session state variables at the beginning
if 'youtube_url' not in st.session_state: st.session_state.youtube_url = ""
if 'notes_title' not in st.session_state: st.session_state.notes_title = ""
if 'summary_level' not in st.session_state: st.session_state.summary_level = "moderate"
if 'summarized_notes' not in st.session_state: st.session_state.summarized_notes = ""
if 'transcript' not in st.session_state: st.session_state.transcript = ""
if 'page' not in st.session_state: st.session_state.page = "Summarize Video"

# Initialize all customization options in session state with defaults
if 'title_font_size' not in st.session_state: st.session_state.title_font_size = 40
if 'notes_font_size' not in st.session_state: st.session_state.notes_font_size = 16
if 'line_height' not in st.session_state: st.session_state.line_height = 1.6
if 'title_font_family' not in st.session_state: st.session_state.title_font_family = "Roboto, sans-serif"
if 'notes_font_style' not in st.session_state: st.session_state.notes_font_style = "Roboto, sans-serif"
if 'font_weight' not in st.session_state: st.session_state.font_weight = "normal"
if 'container_width' not in st.session_state: st.session_state.container_width = 90
if 'padding' not in st.session_state: st.session_state.padding = 25
if 'margin_bottom' not in st.session_state: st.session_state.margin_bottom = 15
if 'border_radius' not in st.session_state: st.session_state.border_radius = 10
if 'text_alignment' not in st.session_state: st.session_state.text_alignment = "left"
if 'title_alignment' not in st.session_state: st.session_state.title_alignment = "left"
if 'title_color' not in st.session_state: st.session_state.title_color = "#4CAF50"
if 'notes_color' not in st.session_state: st.session_state.notes_color = "#333333"
if 'background_color' not in st.session_state: st.session_state.background_color = "#fafafa"
if 'border_color' not in st.session_state: st.session_state.border_color = "#e0e0e0"
if 'accent_color' not in st.session_state: st.session_state.accent_color = "#FFE082"
if 'shadow_intensity' not in st.session_state: st.session_state.shadow_intensity = "light"

st.markdown("<h1 class='title-style'>YouTube Notes Summarizer</h1>", unsafe_allow_html=True)
st.markdown("<p>Easily generate notes from academic YouTube videos.</p>", unsafe_allow_html=True)

# --- NAVIGATION BUTTONS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("Summarize Video", use_container_width=True, key="nav_summarize"):
        st.session_state.page = "Summarize Video"
        st.rerun()
with col2:
    if st.button("View Saved Notes", use_container_width=True, key="nav_saved"):
        st.session_state.page = "View Saved Notes"
        st.rerun()

st.markdown("---")

# --- SUMMARIZE VIDEO PAGE ---
if st.session_state.page == "Summarize Video":
    with st.form(key='notes_form'):
        st.subheader("Video & Notes Details")
        youtube_url = st.text_input("YouTube Video Link", value=st.session_state.youtube_url, placeholder="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        notes_title = st.text_input("Notes Title (Optional)", value=st.session_state.notes_title, placeholder="e.g., Quantum Physics 101")
        
        summary_level = st.radio(
            "Select Summary Specificity",
            ["brief", "moderate", "deep"],
            index=["brief", "moderate", "deep"].index(st.session_state.summary_level),
            horizontal=True
        )

        st.markdown("---")
        
        # --- CUSTOMIZATION OPTIONS (ALWAYS VISIBLE) ---
        st.subheader("Customization Options")
        typography_tab, layout_tab, style_tab = st.tabs(["Typography", "Layout", "Style"])
        with typography_tab:
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.title_font_size = st.slider("Title Font Size (px)", 20, 80, st.session_state.title_font_size)
                st.session_state.notes_font_size = st.slider("Notes Font Size (px)", 10, 28, st.session_state.notes_font_size)
                st.session_state.line_height = st.slider("Line Height", 1.2, 2.5, st.session_state.line_height, 0.1)
            with col2:
                st.session_state.title_font_family = st.selectbox("Title Font", ["Roboto, sans-serif", "Georgia, serif", "Arial", "Times New Roman"], index=["Roboto, sans-serif", "Georgia, serif", "Arial", "Times New Roman"].index(st.session_state.title_font_family))
                st.session_state.notes_font_style = st.selectbox("Notes Font", ["Roboto, sans-serif", "Georgia, serif", "Arial", "Times New Roman"], index=["Roboto, sans-serif", "Georgia, serif", "Arial", "Times New Roman"].index(st.session_state.notes_font_style))
                st.session_state.font_weight = st.selectbox("Notes Font Weight", ["normal", "bold", "lighter", "300", "400", "500", "600", "700"], index=["normal", "bold", "lighter", "300", "400", "500", "600", "700"].index(st.session_state.font_weight))
        with layout_tab:
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.container_width = st.slider("Container Width (%)", 60, 100, st.session_state.container_width)
                st.session_state.padding = st.slider("Container Padding (px)", 10, 50, st.session_state.padding)
                st.session_state.margin_bottom = st.slider("Paragraph Spacing (px)", 5, 30, st.session_state.margin_bottom)
            with col2:
                st.session_state.border_radius = st.slider("Corner Roundness (px)", 0, 30, st.session_state.border_radius)
                st.session_state.text_alignment = st.selectbox("Text Alignment", ["left", "center", "right", "justify"], index=["left", "center", "right", "justify"].index(st.session_state.text_alignment))
                st.session_state.title_alignment = st.selectbox("Title Alignment", ["left", "center", "right"], index=["left", "center", "right"].index(st.session_state.title_alignment))
        with style_tab:
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.title_color = st.color_picker("Title Color", st.session_state.title_color)
                st.session_state.notes_color = st.color_picker("Notes Text Color", st.session_state.notes_color)
                st.session_state.background_color = st.color_picker("Background Color", st.session_state.background_color)
            with col2:
                st.session_state.border_color = st.color_picker("Border Color", st.session_state.border_color)
                st.session_state.accent_color = st.color_picker("Accent Color (for highlights)", st.session_state.accent_color)
                st.session_state.shadow_intensity = st.selectbox("Shadow Style", ["none", "light", "medium", "strong"], index=["none", "light", "medium", "strong"].index(st.session_state.shadow_intensity))

        submit_button = st.form_submit_button(label='Generate Notes')

    # Handle form submission
    if submit_button and youtube_url:
        st.session_state.youtube_url = youtube_url
        st.session_state.notes_title = notes_title if notes_title else "Untitled Notes"
        st.session_state.summary_level = summary_level
        
        with st.spinner("Transcribing video..."):
            transcript = transcribe_youtube_video(youtube_url)

        if transcript:
            st.session_state.transcript = transcript
            st.success("Transcription complete! Now summarizing notes...")
            with st.spinner("Summarizing notes with Gemini..."):
                summarized_notes = summarize_text(transcript, summary_level)
            
            if summarized_notes:
                st.session_state.summarized_notes = summarized_notes
            else:
                st.error("Failed to generate notes. Please check the API keys and try again.")
        else:
            st.error("Failed to transcribe the video. Please check the YouTube link or API keys.")

    if st.session_state.summarized_notes:
        st.markdown("<h2 class='notes-heading-style'>Generated Notes</h2>", unsafe_allow_html=True)
        
        # Use stored styling preferences
        title_font_size = st.session_state.title_font_size
        notes_font_size = st.session_state.notes_font_size
        notes_font_style = st.session_state.notes_font_style
        title_color = st.session_state.title_color
        notes_color = st.session_state.notes_color
        title_font_family = st.session_state.title_font_family
        line_height = st.session_state.line_height
        font_weight = st.session_state.font_weight
        container_width = st.session_state.container_width
        padding = st.session_state.padding
        margin_bottom = st.session_state.margin_bottom
        border_radius = st.session_state.border_radius
        text_alignment = st.session_state.text_alignment
        title_alignment = st.session_state.title_alignment
        background_color = st.session_state.background_color
        border_color = st.session_state.border_color
        accent_color = st.session_state.accent_color
        shadow_intensity = st.session_state.shadow_intensity
        
        # Process the title
        display_title = st.session_state.notes_title

        # Process the content
        content = st.session_state.summarized_notes
        
        # Set shadow based on intensity
        shadow_styles = {
            'none': 'none',
            'light': '0 2px 4px rgba(0,0,0,0.1)',
            'medium': '0 4px 8px rgba(0,0,0,0.15)',
            'strong': '0 8px 16px rgba(0,0,0,0.2)'
        }
        
        notes_html = f"""
        <style>
        .notes-container {{
            width: {container_width}%;
            margin: 20px auto;
            max-width: 1200px;
        }}
        .dynamic-notes-title {{
            font-family: {title_font_family};
            font-size: {title_font_size}px;
            color: {title_color};
            font-weight: bold;
            margin-bottom: 20px;
            margin-top: 10px;
            text-align: {title_alignment};
        }}
        .dynamic-notes-content {{
            font-family: {notes_font_style};
            font-size: {notes_font_size}px;
            color: {notes_color};
            line-height: {line_height};
            font-weight: {font_weight};
            text-align: {text_alignment};
        }}
        .dynamic-notes-content p {{
            margin-bottom: {margin_bottom}px;
        }}
        .main-notes-area {{
            background-color: {background_color};
            padding: {padding}px;
            border-radius: {border_radius}px;
            border: 1px solid {border_color};
            margin: 20px 0;
            box-shadow: {shadow_styles[shadow_intensity]};
        }}
        </style>
        <div class="notes-container">
            <div class="main-notes-area">
                <div class="dynamic-notes-title">{display_title}</div>
                <div class="dynamic-notes-content">
                    <p>{content}</p>
                </div>
            </div>
        </div>
        """
        st.markdown(notes_html, unsafe_allow_html=True)
        st.markdown("---")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button(
                label="Download Notes as .txt",
                data=st.session_state.summarized_notes,
                file_name=f"{st.session_state.notes_title.replace(' ', '_')}.txt",
                mime="text/plain"
            )
        with col2:
            if st.button("Save to Database", use_container_width=True):
                try:
                    save_notes_to_db(
                        st.session_state.notes_title, 
                        st.session_state.youtube_url, 
                        st.session_state.summary_level, 
                        st.session_state.summarized_notes
                    )
                    st.success("Notes saved to database!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving to database: {e}")

# --- VIEW SAVED NOTES PAGE ---
elif st.session_state.page == "View Saved Notes":
    st.markdown("<h1 class='notes-heading-style'>Saved Academic Notes</h1>", unsafe_allow_html=True)
    st.write("Browse and manage all your notes stored in the database.")
    
    notes_df = get_all_notes_from_db()
    
    if not notes_df.empty:
        for index, row in notes_df.iterrows():
            with st.container(border=True):
                st.markdown(f"<h3 style='color: #21618C; margin-top: 0;'>{row['title']}</h3>", unsafe_allow_html=True)
                st.markdown(f"**Created:** {row['created_at']}<br>**Summary Level:** {row['summary_level']}<br>**Video:** <a href='{row['youtube_url']}' target='_blank'>Watch on YouTube</a>", unsafe_allow_html=True)
                
                with st.expander("View Notes Content"):
                    st.markdown(row['notes_content'])
                
                st.download_button(
                    label="Download this note",
                    data=row['notes_content'],
                    file_name=f"{row['title'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    key=f"download_{row['id']}"
                )
        
        st.markdown("---")
        
        st.subheader("Delete Notes")
        note_options = []
        for index, row in notes_df.iterrows():
            created_date = row['created_at'][:10] if row['created_at'] else "Unknown date"
            note_options.append({
                'id': row['id'],
                'display': f"{row['title']} (Created: {created_date})"
            })
        
        selected_notes = st.multiselect(
            "Select notes to delete:",
            options=[note['id'] for note in note_options],
            format_func=lambda x: next(note['display'] for note in note_options if note['id'] == x),
            placeholder="Choose notes to delete..."
        )
        
        if selected_notes:
            st.warning(f"You are about to delete {len(selected_notes)} note(s). This action cannot be undone.")
            if st.button("Delete Selected Notes", type="secondary"):
                delete_notes_from_db(selected_notes)
                st.success(f"Successfully deleted {len(selected_notes)} note(s)!")
                st.rerun()
            
    else:
        st.info("You haven't saved any notes yet. Go to the 'Summarize Video' page to create some!")