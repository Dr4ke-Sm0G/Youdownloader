import os
import sys
from pytube import YouTube
from colorama import Fore, Style
from datetime import timedelta
import ffmpeg


def print_intro():
    print(Fore.CYAN + Style.BRIGHT + "█▄█ █▀█ █░█ ▀█▀ █░█ █▄▄ █▀▀")
    print("░█░ █▄█ █▄█ ░█░ █▄█ █▄█ ██▄")
    print(Style.RESET_ALL)


def print_video_info(yt):
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Title: {yt.title}{Style.RESET_ALL}")

    duration = str(timedelta(seconds=yt.length))
    print(f"{Fore.GREEN}Duration: {duration}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Published on: {yt.publish_date}{Style.RESET_ALL}")


def download_video(url, format_choice):
    try:
        yt = YouTube(url, on_progress_callback=download_progress)

        if format_choice == 'mp4':
            video_stream = choose_video_quality(
                yt.streams.filter(file_extension='mp4'))
            if video_stream:
                print_video_info(yt)
                print(f"\n{Fore.GREEN}Downloading: {yt.title}{Style.RESET_ALL}")
                video_stream.download()
                print(f"{Fore.GREEN}Download complete!{Style.RESET_ALL}")

        elif format_choice == 'mp3':
            audio_stream = yt.streams.get_audio_only()  # changed this line
            if audio_stream:
                print_video_info(yt)
                print(f"\n{Fore.GREEN}Downloading: {yt.title}{Style.RESET_ALL}")
                audio_stream.download()

                audio_filename = audio_stream.default_filename  # changed this line
                base, ext = os.path.splitext(
                    audio_filename)  # changed this line
                mp3_filename = os.path.basename(base).replace(
                    " ", "_").replace("?", "") + ".mp3"  # changed this line

                ffmpeg.input(audio_filename).output(mp3_filename, acodec='libmp3lame').run(
                    overwrite_output=True, quiet=True)  # changed this line

                os.remove(audio_filename)

                print(f"{Fore.GREEN}Download complete!{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}Error: Invalid format choice. Please choose 'mp4' or 'mp3'.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")


def choose_video_quality(streams):
    print(f"{Fore.YELLOW}Available video qualities:{Style.RESET_ALL}")
    for i, stream in enumerate(streams):
        print(f"{i+1}. {stream.resolution}")

    choice = int(input(
        f"{Fore.MAGENTA}Choose a video quality (enter the number): {Style.RESET_ALL}"))
    return streams[choice - 1] if 0 < choice <= len(streams) else None


def download_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = (bytes_downloaded / total_size) * 100
    sys.stdout.write("\r%s[%-50s] %3.1f%%" %
                     (Fore.BLUE, '=' * int(50 * progress / 100), progress))
    sys.stdout.flush()


if __name__ == "__main__":
    print_intro()
    video_url = input(
        f"{Fore.MAGENTA}Enter the YouTube video URL: {Style.RESET_ALL}")
    format_choice = input(
        f"{Fore.MAGENTA}Enter 'mp4' to download as video or 'mp3' to download as audio: {Style.RESET_ALL}")

    try:
        download_video(video_url, format_choice)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\nDownload interrupted by the user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
