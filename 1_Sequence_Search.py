import streamlit as st
from Bio import SeqIO
import requests
from io import BytesIO
import textwrap
from io import StringIO

st.set_page_config(
    page_title = "DevNeuro Lab"
)

# Dropbox URLs for FASTA files
fasta_urls = {
    "Intestine Transcriptome": "https://www.dropbox.com/scl/fi/m7e94xr6e8yf7z3ol126v/cuke2022.trinity.Trinity.fasta?rlkey=3v2p04r7oaiagu9aj8gxl16x8&dl=1",
    "RNC 2022 Transcriptome": "https://www.dropbox.com/scl/fi/y5m4vbdwlvqkr33oe8chj/cuke_rnc2022_ym.dammit.fasta?rlkey=l334noxchmf38ezq1coui371m&dl=1",
    "Long-read Genome Assembly v1.0": "https://www.dropbox.com/scl/fi/qltlrmb6gvi9a0ogngfx9/Hglab.hic.genome.2023.fa?rlkey=2xqkgrvvg34uww2uvp8cq9ycz&dl=1",
    "Draft Genome v2.2 (2021)": "https://www.dropbox.com/scl/fi/mxs4nc1tf2tjol44fxpql/Hglab.v2.2.genome.fa?rlkey=d10cz6gudx25ktd267gq1lidw&dl=1"
}

def download_file(url):
    st.info(f"Downloading FASTA file from url...")
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        return StringIO(r.content.decode('utf-8'))
    else:
        st.error("Failed to download file.")
        return None

# Function to wrap the sequence string
def wrap_string(s, width=80):
    return "\n".join(textwrap.wrap(s, width))

# Caching the indexing to avoid reloading for each session
@st.cache_resource
def load_fasta(fasta_stream):
    return SeqIO.to_dict(SeqIO.parse(fasta_stream, "fasta"))

def main():
    st.title("FASTA File Sequence Search from Dropbox URLs")

    # Dropdown to select FASTA file
    selected_fasta_label = st.selectbox("Select a FASTA file:", list(fasta_urls.keys()))

    # Load and index the selected FASTA file
    if selected_fasta_label:
        fasta_stream = download_file(fasta_urls[selected_fasta_label])
        if fasta_stream:
            with st.spinner('Indexing FASTA file... Please wait.'):
                fasta_index = load_fasta(fasta_stream)

            sequence_id = st.text_input("Enter Sequence ID:")

            if sequence_id and sequence_id in fasta_index:
                record = fasta_index[sequence_id]
                fasta_header = f">{record.id} {record.description}"
                fasta_sequence = wrap_string(str(record.seq))

                st.code(f"{fasta_header}\n{fasta_sequence}", language="plaintext")
            elif sequence_id:
                st.warning("Sequence ID not found in the file.")
        else:
            st.error("Failed to load the selected FASTA file.")

if __name__ == "__main__":
    main()
