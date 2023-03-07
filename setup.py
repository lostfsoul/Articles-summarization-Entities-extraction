import subprocess

spacy_download_cmd = 'python -m spacy download en_core_web_trf'
subprocess.run(spacy_download_cmd, shell=True)