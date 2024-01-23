import requests
import subprocess
import sys
from tqdm import tqdm


local_filename = "discord_linux.tar.gz"

def download():
    file_url = "https://discord.com/api/download?platform=linux&format=tar.gz"
    resp = requests.get(file_url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(local_filename, 'wb') as file, tqdm(
        desc=local_filename,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def unzip():
    try:
        subprocess.run(["sudo", "tar", "-xvzf", local_filename, "-C", "/opt"])
        print(f"Extracted {local_filename} to /opt successfully.")
    except Exception as e:
        print(f"Failed to extract {local_filename}: {e}")
        sys.exit(1)

def create_symbolic_link_to_usr_bin():
    try:
        subprocess.run(["sudo", "ln", "-sf", "-v", "/opt/Discord/Discord", "/usr/bin/Discord"])
        print("Created symbolic link to Discord.")
    except Exception as e:
        print(f"Failed to create symbolic link: {e}")
        sys.exit(1)

def create_desktop_icon():
    desktop_file_path = '/opt/Discord/discord.desktop'
    new_desktop_content = """[Desktop Entry]
Name=Discord
StartupWMClass=discord
Comment=All-in-one voice and text chat for gamers that's free, secure, and works on both your desktop and phone.
GenericName=Internet Messenger
Exec=/usr/bin/Discord
Icon=/opt/Discord/discord.png
Type=Application
Categories=Network;InstantMessaging;
Path=/usr/bin
"""
    try:
        with open(desktop_file_path, 'w') as file:
            file.write(new_desktop_content)
        subprocess.run(["sudo", "cp", "-r", "-v", "/opt/Discord/discord.desktop", "/usr/share/applications"])
        print("Copied discord.desktop to /usr/share/applications.")
    except Exception as e:
        print(f"Failed to create discord.desktop: {e}")
        sys.exit(1)

def clean_up():
    try:
        subprocess.run(["rm","-rf",local_filename])
    except Exception as e:
        print(f"Failed to clean up: {e}")
        sys.exit(1)



def main():
    download()
    unzip()
    create_symbolic_link_to_usr_bin()
    create_desktop_icon()
    clean_up()
    print("Discord has been successfully installed.")

if __name__ == "__main__":
    main()
