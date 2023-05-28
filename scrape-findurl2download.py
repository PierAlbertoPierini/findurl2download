import urllib.request
import os
from tqdm import tqdm

# Create a folder for downloaded files if it doesn't already exist
if not os.path.exists('downloaded_files'):
    os.makedirs('downloaded_files')

# Opens a text file in writing mode to save any errors during the download
error_file = open('download_errors.txt', 'w')

# Refresh the status bar
def update_progress_bar(blocknum, blocksize, totalsize, progress_bar):
    progress = blocknum * blocksize
    if totalsize > 0:
        progress_bar.total = totalsize
    progress_bar.update(progress - progress_bar.n)

# Open the text file in reading mode
with open('textfile2scrape.txt', 'r') as file:
    # Read the file line by line
    for line in file:
        # If the row contains a URL
        if 'http' in line:
            try:
                # Download the file from the URL
                url = line.strip()
                filename = line.split('/')[-1].rstrip() # Remove end-of-line characters from the file name
                filepath = 'downloaded_files/' + filename
                with tqdm(unit='B', unit_scale=True, miniters=1, desc=filename) as progress_bar:
                    urllib.request.urlretrieve(url, filepath, reporthook=lambda blocknum, blocksize, totalsize: update_progress_bar(blocknum, blocksize, totalsize, progress_bar))
            except Exception as e:
                # Handle any errors during download
                print('Impossibile scaricare il file dall\'URL:', url)
                print('Errore:', e)
                # Write the error to the text file
                error_file.write('Impossibile scaricare il file dall\'URL: ' + url + '\n')
                error_file.write('Errore: ' + str(e) + '\n\n')

# Close the error text file
error_file.close()
