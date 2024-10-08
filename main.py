# tuning fork
# author: anna maly
# date: 8.10.24


import streamlit as st
import numpy as np

# Frequencies of the 12 notes (A4 = 440Hz), based on the equal-tempered scale
note_frequencies = {
    "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23,
    "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88
}

# Function to generate a sine wave for a given frequency and duration
def generate_sine_wave(freq, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

# Function to generate frequencies for eighth-tones within 25 cents of a semitone
def generate_eighth_tones(base_freq):
    # Cents to frequency conversion: f_new = f_old * 2^(cents/1200)
    cents_steps = [-75, -50, -25, 0, 25, 50, 75]
    return [base_freq * 2**(step / 1200) for step in cents_steps]


# Initialize session state for base note and eighth tone if not set
if 'base_note' not in st.session_state:
    st.session_state.base_note = None

if 'eighth_tone' not in st.session_state:
    st.session_state.eighth_tone = None

# Streamlit App
st.title('Tuning Fork for Singers')

st.markdown("### Select the Base Note (One Octave)")

# Create a graphical claviature to select the base note
col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])

# Graphical Claviature with buttons for notes
if col1.button('C4'):
    st.session_state.base_note = "C4"
if col1.button('C#4'):
    st.session_state.base_note = "C#4"
if col2.button('D4'):
    st.session_state.base_note = "D4"
if col2.button('D#4'):
    st.session_state.base_note = "D#4"
if col3.button('E4'):
    st.session_state.base_note = "E4"
if col4.button('F4'):
    st.session_state.base_note = "F4"
if col4.button('F#4'):
    st.session_state.base_note = "F#4"
if col5.button('G4'):
    st.session_state.base_note = "G4"
if col5.button('G#4'):
    st.session_state.base_note = "G#4"
if col6.button('A4'):
    st.session_state.base_note = "A4"
if col6.button('A#4'):
    st.session_state.base_note = "A#4"
if col7.button('B4'):
    st.session_state.base_note = "B4"

# Once the base note is selected, generate eighth-tone frequencies
if st.session_state.base_note:
    base_note = st.session_state.base_note
    st.write(f"You selected {base_note}")
    base_freq = note_frequencies[base_note]
    eighth_tone_freqs = generate_eighth_tones(base_freq)
    
    st.markdown("### Select the Eighth-Tone")
    
    # Create columns for each option to display them horizontally
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    if col1.button('-75 cents'):
        st.session_state.eighth_tone = '-75 cents'
    if col2.button('-50 cents'):
        st.session_state.eighth_tone = '-50 cents'
    if col3.button('-25 cents'):
        st.session_state.eighth_tone = '-25 cents'
    if col4.button('0 cents'):
        st.session_state.eighth_tone = '0 cents'
    if col5.button('+25 cents'):
        st.session_state.eighth_tone = '+25 cents'
    if col6.button('+50 cents'):
        st.session_state.eighth_tone = '+50 cents'
    if col7.button('+75 cents'):
        st.session_state.eighth_tone = '+75 cents'
    
    # Check if the eighth tone has been selected
    if st.session_state.eighth_tone:
        eighth_tone = st.session_state.eighth_tone
        st.write(f"Selected fine tuning: {eighth_tone}")
        
        # Map the selected fine tuning to the appropriate frequency
        cents_to_index = {
            '-75 cents': 0,
            '-50 cents': 1,
            '-25 cents': 2,
            '0 cents': 3,
            '+25 cents': 4,
            '+50 cents': 5,
            '+75 cents': 6
        }
        selected_freq = eighth_tone_freqs[cents_to_index[eighth_tone]]
        st.write(f"The frequency for {base_note} with {eighth_tone} is {selected_freq:.2f} Hz")

        # Generate and play the sine wave
        wave = generate_sine_wave(selected_freq, duration=6.0)
        st.audio(wave, sample_rate=44100)


    
