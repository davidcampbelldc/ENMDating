import streamlit as st
from datetime import datetime, date
import logging
import time
from utils.supabase_client import supabase
from utils.auth import require_auth

# Require authentication for this page
require_auth()

def create_or_update_profile():
    # Initialize session state for managing profile updates and file uploader key
    if 'profile_updated' not in st.session_state:
        st.session_state.profile_updated = False
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    
    # Check if profile exists
    profile = supabase.table('profiles').select('*').eq('id', st.session_state.user.id).execute()
    
    # Get existing data if profile exists
    existing_data = profile.data[0] if profile.data else {}
    
    st.header("Your Profile")
    
    # Display existing photos if any
    if existing_data.get('photos'):
        st.subheader("Current Photos")
        photo_cols = st.columns(5)  # Create 5 columns for photos
        for idx, photo_url in enumerate(existing_data.get('photos', [])[:5]):  # Limit to 5 photos
            with photo_cols[idx]:
                st.image(photo_url, use_container_width=True)
    
    # Image upload section - with dynamic key
    st.subheader("Upload New Photos")
    uploaded_files = st.file_uploader(
        "Upload up to 5 photos", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key=f"photo_uploader_{st.session_state.uploader_key}"
    )
    
    if uploaded_files:
        st.subheader("Preview New Photos")
        preview_cols = st.columns(5)
        for idx, file in enumerate(uploaded_files[:5]):  # Limit to 5 photos
            with preview_cols[idx]:
                st.image(file, use_container_width=True)
    
    # Profile form
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=existing_data.get('name', ''))
            birth_date = st.date_input(
                "Birth Date",
                value=datetime.strptime(existing_data.get('birth_date', '2000-01-01'), '%Y-%m-%d').date() if existing_data.get('birth_date') else date(2000, 1, 1),
                min_value=date(1920, 1, 1),
                max_value=date.today()
            )
            gender = st.selectbox(
                "Gender",
                options=['', 'Male', 'Female', 'Non-binary', 'Other'],
                index=0 if not existing_data.get('gender') else 
                    ['', 'Male', 'Female', 'Non-binary', 'Other'].index(existing_data.get('gender'))
            )
        
        with col2:
            location = st.text_input("Location", value=existing_data.get('location', ''))
            bio = st.text_area("Bio", value=existing_data.get('bio', ''), height=133)
        
        submit = st.form_submit_button("Save Profile")
        
        if submit:
            try:
                # Get existing photos first
                existing_photos = existing_data.get('photos', [])
                
                # Handle photo upload
                photo_urls = []
                for file in uploaded_files[:5] if uploaded_files else []:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_ext = file.name.split('.')[-1]
                    user_id = st.session_state.user.id
                    filename = f"{user_id}/{timestamp}.{file_ext}"
                    
                    response = supabase.storage.from_('profile-photos').upload(
                        filename,
                        file.getvalue(),
                        file_options={"content-type": f"image/{file_ext}"}
                    )
                    
                    photo_url = supabase.storage.from_('profile-photos').get_public_url(filename)
                    photo_urls.append(photo_url)
                
                # Combine existing photos with new ones, respecting the 5 photo limit
                combined_photos = existing_photos + photo_urls
                if len(combined_photos) > 5:
                    combined_photos = combined_photos[-5:]  # Keep the 5 most recent photos
                
                # Prepare profile data
                profile_data = {
                    'id': st.session_state.user.id,
                    'name': name,
                    'birth_date': birth_date.isoformat(),
                    'gender': gender,
                    'location': location,
                    'bio': bio,
                    'photos': combined_photos  # Use the combined photo list
                }
                
                # Debug output
                logging.debug("Attempting to save profile with data:")
                logging.debug(profile_data)
                
                # Upsert profile data
                result = supabase.table('profiles').upsert(
                    profile_data,
                    returning='representation'
                ).execute()
                
                logging.debug("Supabase response:")
                logging.debug(result)
                
                if result.data:
                    st.success("Profile updated successfully!")
                    logging.debug("Profile saved successfully")
                    # Increment the uploader key to force a new instance
                    st.session_state.uploader_key += 1
                    st.session_state.profile_updated = True
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("No data returned from save operation")
                    logging.debug("No data returned from save")
                
            except Exception as e:
                logging.error(f"Error saving profile: {str(e)}")
                st.error(f"Error saving profile: {str(e)}")
    
    # After successful update, clear the flag
    if st.session_state.profile_updated:
        st.session_state.profile_updated = False

if __name__ == "__main__":
    create_or_update_profile()