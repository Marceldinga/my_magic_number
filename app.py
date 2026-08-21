import streamlit as st

st.set_page_config(
    page_title="My Magic Number",
    page_icon="✨",
    layout="centered"
)

st.title("✨ My Magic Number")
st.write("Enter your first and last name to discover your magic number!")


def name_magic(first_name, last_name):
    # Count the number of letters
    first = len(first_name.strip())
    last = len(last_name.strip())

    # Magic calculation
    magic = (first * 10) + last

    return magic


first_name = st.text_input(
    "First Name",
    placeholder="Enter your first name"
)

last_name = st.text_input(
    "Last Name",
    placeholder="Enter your last name"
)


if st.button("✨ Reveal My Magic Number"):

    if first_name.strip() == "" or last_name.strip() == "":
        st.warning("Please enter both your first and last name.")

    else:
        magic_number = name_magic(first_name, last_name)

        st.balloons()

        st.success(
            f"✨ {first_name} {last_name}, "
            f"your magic number is {magic_number}! ✨"
        )

        st.write("### 🪄 How the magic works")

        st.write(
            f"Your first name has **{len(first_name.strip())} letters**."
        )

        st.write(
            f"Your last name has **{len(last_name.strip())} letters**."
        )

        st.write(
            f"({len(first_name.strip())} × 10) "
            f"+ {len(last_name.strip())} "
            f"= **{magic_number}**"
        )
