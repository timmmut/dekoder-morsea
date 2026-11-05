from datetime import datetime
from lxml import etree
import streamlit as st

# Słownik
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', 'Ą': '.-.-', 'Ć': '-.-..', 'Ę': '..-..', 'Ł': '.-..-',
    'Ń': '--.--', 'Ó': '---.', 'Ś': '...-...', 'Ź': '--..-.', 'Ż': '--..-',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
}


def encode_to_morse(text: str):
    words = text.upper().split()
    encoded_words = []
    for word in words:
        letters = [MORSE_DICT[char] for char in word if char in MORSE_DICT]
        if letters:
            encoded_words.append(' '.join(letters))
    return ' / '.join(encoded_words), '    '.join(encoded_words)


def generate_and_validate_xml(sender: str, morse_content: str, xsd_path: str = 'morse.xsd'):
    xsi_ns = 'http://www.w3.org/2001/XMLSchema-instance'
    root = etree.Element(
        'morseMessage', nsmap={'xsi': xsi_ns},
        attrib={f'{{{xsi_ns}}}noNamespaceSchemaLocation': xsd_path},
    )
    etree.SubElement(root, 'sender').text = sender
    etree.SubElement(root, 'timestamp').text = datetime.now().isoformat(timespec='seconds')
    etree.SubElement(root, 'content').text = morse_content
    xml_bytes = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    schema = etree.XMLSchema(etree.parse(xsd_path))
    schema.assertValid(etree.fromstring(xml_bytes))
    return xml_bytes


def main():
    st.set_page_config(page_title="Koder Morse'a - Grupa A", page_icon='📡')
    st.title("📡 Koder kodu Morse'a (Grupa A)")
    sender_name = st.text_input('Nadawca:', value='Grupa A')
    input_text = st.text_area('Wpisz zdanie w języku naturalnym do zakodowania:', placeholder='Np. Ala ma kota')
    if st.button('Zakoduj i wygeneruj XML'):
        if not input_text.strip():
            st.warning('Wprowadź tekst przed zakodowaniem.')
        else:
            xml_morse, display_morse = encode_to_morse(input_text)
            if not xml_morse:
                st.error('Tekst nie zawiera obsługiwanych znaków alfanumerycznych.')
            else:
                st.subheader("Zakodowana wiadomość (widok bez ukośników):")
                st.code(display_morse, language=None)
                try:
                    xml_data = generate_and_validate_xml(sender_name, xml_morse)
                    st.success('Plik XML został poprawnie wygenerowany i zweryfikowany ze schematem XSD.')
                    with st.expander('Podgląd wygenerowanego pliku XML (z ukośnikami)'):
                        st.code(xml_data.decode('utf-8'), language='xml')
                    st.download_button(label='📥 Pobierz plik message.xml', data=xml_data,
                                       file_name='message.xml', mime='application/xml')
                except etree.DocumentInvalid as e:
                    st.error(f'Błąd walidacji XSD: {e}')
                except OSError:
                    st.error('Nie znaleziono pliku morse.xsd w katalogu z aplikacją.')


if __name__ == '__main__':
    main()