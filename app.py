from fetch import *
from download import *

def main ():
    # Choose country Region and number of videos you want.
    # Ex: ('US', 10) --> this will return the top 10 trending videos in the United States
    request = create_request('US', 3)
    videos = get_videos(request)

    for i in range(len(videos)):
        comments = find_comments(videos[i].id)
        timestamps = get_timestamps(comments)

        videos[i].set_timestamps(timestamps)
        possible_shorts = videos[i].get_shorts()

        make_shorts(videos[i], i + 1)
        videos[i].show_details()
        
main()