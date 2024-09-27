class Video:
    def __init__(self, title, channel, date, views, id):
        self.title = title
        self.channel = channel
        self.date = date
        self.views = views
        self.id = id
        self.url = f'https://www.youtube.com/watch?v={id}'
        self.timestamps = []
        self.shorts = []

    def get_title(self):
        return self.title
    
    def get_channel(self):
        return self.channel
    
    def get_date(self):
        return self.date
    
    def get_views(self):
        return self.views
    
    def get_id(self):
        return self.id
    
    def get_url(self):
        return self.url
    
    def get_timestamps(self):
        return self.timestamps
    
    def get_shorts(self):
        return self.shorts
    
    def set_timestamps(self, timestamps):
        self.timestamps = timestamps
        self.shorts = self.gen_shorts()
        return self.timestamps


    def parse_time(self, time):
        parts = time.split(':')
        parts = [int(p) for p in parts]
        seconds = 0
        for part in parts:
            seconds = seconds * 60 + part
        return seconds


    def format_time(self, time):
        seconds = time
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hours:02}:{minutes:02}:{secs:02}'
    

    def gen_shorts(self):
        shorts = []
        for timestamp, count in self.timestamps:
            input_seconds = self.parse_time(timestamp)
            start = max(input_seconds - 15, 0)
            end = input_seconds + 15

            shorts.append( (self.format_time(start), self.format_time(end)) )
        return shorts
    


    
    def show_details(self):
        print('-' * 50)
        print(f"Title: {self.title}")
        print(f"Channel: {self.channel}")
        print(f"Published At: {self.date}")
        print(f"View Count: {self.views}")
        print(f"Video URL: {self.url}")
        print()
        print("Most mentioned timestamps in comments:")
        for timestamp, count in self.timestamps:
            print(f"{timestamp} mentioned {count} times")
        print('-' * 50)

