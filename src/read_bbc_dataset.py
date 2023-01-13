import os.path

genres = ['business', 'entertainment', 'politics', 'sport', 'tech']
news_number = '1'.zfill(3)

class BbcNews():
    def __init__(self, genre, dir, news_number=0) -> None:
        self.news_number = news_number
        self.genre = genre
        self.dir = dir
    
    def get_filename(self):
        return str(self.news_number).zfill(3)

    def __next__(self):
        self.news_number += 1
        filepath = f'{self.dir}/bbc/{self.genre}/{self.get_filename()}.txt'

        if os.path.isfile(filepath):
            return filepath
        else:
            raise StopIteration

    def read_news(self):
        try:
            with open(self.__next__()) as file:
                title = file.__next__().strip()

                content = ""
                for line in file:
                    content += line.replace('\n', '').replace('\\', '').replace("\'", '')
                content.strip()

                return (title, content)
        except StopIteration:
            return ()

def get_genre_iterators(dir):
    iterators = []
    for genre in genres:
        iterators.append(BbcNews(genre, dir))

    return iterators