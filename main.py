import streamlit as st
import numpy as np
import io

# Constants
A4_FREQ = 440.0  # Frequency of A4
SAMPLE_RATE = 44100  # Audio sample rate
DURATION = 6  # Duration of each tone in seconds

# Define note names and semitone distance from A4
NOTES = [
    ("C", -9), ("C#", -8), ("D", -7), ("D#", -6), ("E", -5), 
    ("F", -4), ("F#", -3), ("G", -2), ("G#", -1), ("A", 0), 
    ("A#", 1), ("B", 2)
]

# Function to generate frequency based on semitone and cent offset
def generate_frequency(semitone, cent_offset):
    base_freq = A4_FREQ * 2 ** (semitone / 12.0)
    return base_freq * 2 ** (cent_offset / 1200.0)

# Function to generate a sine wave for a given frequency
def generate_sine_wave(freq, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.1 * np.sin(2 * np.pi * freq * t)  # 0.5 to reduce volume
    return tone

# Function to convert a NumPy array to a WAV byte buffer
def array_to_wav_bytes(data, sample_rate):
    # Normalize the data to 16-bit PCM format
    scaled = np.int16(data / np.max(np.abs(data)) * 32767)
    # Create a WAV byte buffer
    buf = io.BytesIO()
    # Write the data using the WAV format: format 1 (PCM), 1 channel, 16-bit samples
    wav_header = (b"RIFF" +
                  (36 + len(scaled) * 2).to_bytes(4, 'little') +
                  b"WAVEfmt " +
                  (16).to_bytes(4, 'little') +  # Subchunk1Size (PCM)
                  (1).to_bytes(2, 'little') +   # AudioFormat (PCM = 1)
                  (1).to_bytes(2, 'little') +   # NumChannels (Mono = 1)
                  sample_rate.to_bytes(4, 'little') +  # SampleRate
                  (sample_rate * 2).to_bytes(4, 'little') +  # ByteRate (SampleRate * NumChannels * BitsPerSample/8)
                  (2).to_bytes(2, 'little') +   # BlockAlign (NumChannels * BitsPerSample/8)
                  (16).to_bytes(2, 'little') +  # BitsPerSample (16 bits)
                  b"data" +
                  (len(scaled) * 2).to_bytes(4, 'little'))  # Subchunk2Size (NumSamples * NumChannels * BitsPerSample/8)
    buf.write(wav_header)
    buf.write(scaled.tobytes())
    return buf.getvalue()

# Streamlit UI
#st.title("Tuning Fork App")
#st.write("Click a button to play the corresponding frequency:")

# Variable to store the selected audio for playback
selected_audio = None

# Arrange buttons in a claviature-like layout
cols = st.columns(12)
for idx, (note, semitone) in enumerate(NOTES):
    with cols[idx]:
        st.write(f"**{note}**")
        for cents in [0, 25, 50, 75]:
            if st.button(f"{cents}", key=f"{note}_{cents}"):
                # Generate the sine wave for the selected frequency
                freq = generate_frequency(semitone, cents)
                tone = generate_sine_wave(freq, DURATION, SAMPLE_RATE)
                selected_audio = array_to_wav_bytes(tone, SAMPLE_RATE)

# Play the selected audio outside the columns (below all buttons)
if selected_audio:
    st.audio(selected_audio, format='audio/wav')


# import streamlit as st
# import numpy as np
# import soundfile as sf
# import os

# # Constants
# A4_FREQ = 440.0  # Frequency of A4
# SAMPLE_RATE = 44100  # Audio sample rate
# DURATION = 6#1.5  # Duration of each tone in seconds

# # Define note names and semitone distance from A4
# NOTES = [
#     ("C", -9), ("C#", -8), ("D", -7), ("D#", -6), ("E", -5), 
#     ("F", -4), ("F#", -3), ("G", -2), ("G#", -1), ("A", 0), 
#     ("A#", 1), ("B", 2)
# ]

# # Function to generate frequency based on semitone and cent offset
# def generate_frequency(semitone, cent_offset):
#     base_freq = A4_FREQ * 2 ** (semitone / 12.0)
#     return base_freq * 2 ** (cent_offset / 1200.0)

# # Function to generate a sine wave for a given frequency
# def generate_sine_wave(freq, duration, sample_rate):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     tone = 0.5 * np.sin(2 * np.pi * freq * t)  # 0.5 to reduce volume
#     return tone

# # Function to save the sine wave as a WAV file
# def save_wav(filename, data, sample_rate):
#     sf.write(filename, data, sample_rate)

# # Function to generate and save all frequencies
# def generate_all_frequencies():
#     frequencies = {}
#     for note, semitone in NOTES:
#         for cents in [0, 25, 50, 75]:
#             freq = generate_frequency(semitone, cents)
#             filename = f"{note}_{cents}.wav"
#             tone = generate_sine_wave(freq, DURATION, SAMPLE_RATE)
#             save_wav(filename, tone, SAMPLE_RATE)
#             frequencies[f"{note}_{cents}"] = filename
#     return frequencies

# # Generate all frequencies and save them as .wav files
# frequencies = generate_all_frequencies()

# # Streamlit UI
# #st.title("Tuning Fork App")
# #st.write("Click a button to play the corresponding frequency:")

# # Variable to store the selected file for playback
# selected_file = None

# # Arrange buttons in a claviature-like layout
# cols = st.columns(12)
# for idx, (note, _) in enumerate(NOTES):
#     with cols[idx]:
#         st.write(f"**{note}**")
#         for cents in [0, 25, 50, 75]:
#             if st.button(f"{cents}", key=f"{note}_{cents}"):
#                 selected_file = frequencies[f"{note}_{cents}"]

# # Play the selected file outside the columns (below all buttons)
# if selected_file:
#     st.audio(selected_file)

# # Remove the generated wav files after the app is stopped
# if 'cleaned_up' not in st.session_state:
#     for file in frequencies.values():
#         if os.path.exists(file):
#             os.remove(file)
#     st.session_state['cleaned_up'] = True




# # tuning fork
# # author: anna maly
# # date: 8.10.24
# import streamlit as st
# import numpy as np
# import soundfile as sf
# import io

# # Frequencies of the 12 notes (A4 = 440Hz), based on the equal-tempered scale
# note_frequencies = {
#     "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23,
#     "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88
# }

# # Function to generate a sine wave for a given frequency and duration
# def generate_sine_wave(freq, duration=6.0, sample_rate=44100):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     wave = 0.5 * np.sin(2 * np.pi * freq * t)
#     return wave

# # Pre-calculate frequencies for eighth-tones for each base note
# def calculate_frequencies(note_frequencies):
#     freq_map = {}
#     cents_steps = [-50, -25, 0, 25, 50]  # Cents steps
#     for note, base_freq in note_frequencies.items():
#         freq_map[note] = [base_freq * 2**(step / 1200) for step in cents_steps]
#     return freq_map

# # Function to convert numpy audio data to bytes for use with st.audio
# def audio_to_bytes(wave, sample_rate=44100):
#     virtual_file = io.BytesIO()
#     sf.write(virtual_file, wave, sample_rate, format='wav')
#     return virtual_file.getvalue()

# # Get pre-calculated frequencies
# precalculated_frequencies = calculate_frequencies(note_frequencies)

# # Streamlit App
# st.title('Tuning Fork for Singers - Claviature')

# st.markdown("### Click to play the corresponding note")

# # Display buttons for each note and its variants (-50, -25, +0, +25, +50 cents)
# note_keys = list(note_frequencies.keys())

# # Create columns for each set of notes
# cols = st.columns(len(note_keys))

# for i, note in enumerate(note_keys):
#     with cols[i]:
#         st.markdown(f"**{note}**")
        
#         # Display buttons for each eighth-tone (5 buttons per note)
#         for j, cents_step in enumerate([-50, -25, 0, 25, 50]):
#             button_label = f"{note} {'+' if cents_step > 0 else ''}{cents_step} cents"
#             freq = precalculated_frequencies[note][j]
            
#             # Generate sine wave for the note
#             wave = generate_sine_wave(freq, duration=6.0)
            
#             # Convert to bytes for st.audio
#             audio_bytes = audio_to_bytes(wave)

#             # Display play button with st.audio
#             st.audio(audio_bytes, format='audio/wav')

# import os
# import numpy as np
# import soundfile as sf

# # Define the base frequencies of the 12 notes (A4 = 440Hz) based on the equal-tempered scale
# note_frequencies = {
#     "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23,
#     "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88
# }

# # Function to generate a sine wave for a given frequency and duration
# def generate_sine_wave(freq, duration=6.0, sample_rate=44100):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     wave = 0.5 * np.sin(2 * np.pi * freq * t)
#     return wave

# # Pre-calculate frequencies for eighth-tones for each base note
# def calculate_frequencies(note_frequencies):
#     freq_map = {}
#     cents_steps = [-50, -25, 0, 25, 50]  # Cents steps
#     for note, base_freq in note_frequencies.items():
#         freq_map[note] = [base_freq * 2**(step / 1200) for step in cents_steps]
#     return freq_map

# # Create the 'sounds' folder if it doesn't exist
# output_folder = "sounds"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # Generate and save the .wav files for each note and its eighth-tone variations
# def generate_wav_files(precalculated_frequencies):
#     for note, frequencies in precalculated_frequencies.items():
#         for i, freq in enumerate(frequencies):
#             cents_steps = [-50, -25, 0, 25, 50]  # Cents steps
#             cents_label = f"{cents_steps[i]}".replace("-", "minus").replace("+", "plus")  # Avoid special chars in filenames
#             filename = f"{note}{cents_label}.wav"
#             wave = generate_sine_wave(freq, duration=6.0)
#             sf.write(os.path.join(output_folder, filename), wave, 44100)
#             print(f"Generated {filename} with frequency {freq:.2f} Hz")

# # Pre-calculate frequencies
# precalculated_frequencies = calculate_frequencies(note_frequencies)

# # Generate the wav files
# generate_wav_files(precalculated_frequencies)

# print(f"WAV files generated in the '{output_folder}' folder.")




# import streamlit as st
# import numpy as np

# # Frequencies of the 12 notes (A4 = 440Hz), based on the equal-tempered scale
# note_frequencies = {
#     "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13, "E4": 329.63, "F4": 349.23,
#     "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88
# }

# # Function to generate a sine wave for a given frequency and duration
# def generate_sine_wave(freq, duration=1.0, sample_rate=44100):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     wave = 0.5 * np.sin(2 * np.pi * freq * t)
#     return wave

# # Function to generate frequencies for eighth-tones within 25 cents of a semitone
# def generate_eighth_tones(base_freq):
#     # Cents to frequency conversion: f_new = f_old * 2^(cents/1200)
#     cents_steps = [-75, -50, -25, 0, 25, 50, 75]
#     return [base_freq * 2**(step / 1200) for step in cents_steps]


# # Initialize session state for base note and eighth tone if not set
# if 'base_note' not in st.session_state:
#     st.session_state.base_note = None

# if 'eighth_tone' not in st.session_state:
#     st.session_state.eighth_tone = None

# # Streamlit App
# st.title('Tuning Fork for Singers')

# st.markdown("### Select the Base Note (One Octave)")

# # Create a graphical claviature to select the base note
# col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])

# # Graphical Claviature with buttons for notes
# if col1.button('C4'):
#     st.session_state.base_note = "C4"
# if col1.button('C#4'):
#     st.session_state.base_note = "C#4"
# if col2.button('D4'):
#     st.session_state.base_note = "D4"
# if col2.button('D#4'):
#     st.session_state.base_note = "D#4"
# if col3.button('E4'):
#     st.session_state.base_note = "E4"
# if col4.button('F4'):
#     st.session_state.base_note = "F4"
# if col4.button('F#4'):
#     st.session_state.base_note = "F#4"
# if col5.button('G4'):
#     st.session_state.base_note = "G4"
# if col5.button('G#4'):
#     st.session_state.base_note = "G#4"
# if col6.button('A4'):
#     st.session_state.base_note = "A4"
# if col6.button('A#4'):
#     st.session_state.base_note = "A#4"
# if col7.button('B4'):
#     st.session_state.base_note = "B4"

# # Once the base note is selected, generate eighth-tone frequencies
# if st.session_state.base_note:
#     base_note = st.session_state.base_note
#     st.write(f"You selected {base_note}")
#     base_freq = note_frequencies[base_note]
#     eighth_tone_freqs = generate_eighth_tones(base_freq)
    
#     st.markdown("### Select the Eighth-Tone")
    
#     # Create columns for each option to display them horizontally
#     col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

#     if col1.button('-75 cents'):
#         st.session_state.eighth_tone = '-75 cents'
#     if col2.button('-50 cents'):
#         st.session_state.eighth_tone = '-50 cents'
#     if col3.button('-25 cents'):
#         st.session_state.eighth_tone = '-25 cents'
#     if col4.button('0 cents'):
#         st.session_state.eighth_tone = '0 cents'
#     if col5.button('+25 cents'):
#         st.session_state.eighth_tone = '+25 cents'
#     if col6.button('+50 cents'):
#         st.session_state.eighth_tone = '+50 cents'
#     if col7.button('+75 cents'):
#         st.session_state.eighth_tone = '+75 cents'
    
#     # Check if the eighth tone has been selected
#     if st.session_state.eighth_tone:
#         eighth_tone = st.session_state.eighth_tone
#         st.write(f"Selected fine tuning: {eighth_tone}")
        
#         # Map the selected fine tuning to the appropriate frequency
#         cents_to_index = {
#             '-75 cents': 0,
#             '-50 cents': 1,
#             '-25 cents': 2,
#             '0 cents': 3,
#             '+25 cents': 4,
#             '+50 cents': 5,
#             '+75 cents': 6
#         }
#         selected_freq = eighth_tone_freqs[cents_to_index[eighth_tone]]
#         st.write(f"The frequency for {base_note} with {eighth_tone} is {selected_freq:.2f} Hz")

#         # Generate and play the sine wave
#         wave = generate_sine_wave(selected_freq, duration=6.0)
#         st.audio(wave, sample_rate=44100)


    
